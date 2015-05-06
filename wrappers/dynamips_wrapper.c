// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/dynamips_wrapper.c
 *
 * Wrapper for Dynamips.
 *
 * LICENSE:
 *
 * This file is part of UNetLab (Unified Networking Lab).
 *
 * UNetLab is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * UNetLab is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with UNetLab.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2015 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20150422
 */


/*
 * # tunctl -b -t vunl0_6_0
# ip link set up vunl0_6_0
# dynamips -P 7200 -t npe-400 -l /opt/unetlab/tmp/0/TestLab/R6.log -i 1 -r 256 -o 4 -n 128 -c 0x2102 -X -s 0:0:tap:vunl0_6_0 --idle-pc 0x62f09f78 -p 1:PA-2FE-TX -p 2:PA-2FE-TX -p 3:PA-8T -s 3:0:unix:/opt/unetlab/tmp/0/TestLab/6/6:/opt/unetlab/tmp/0/TestLab/6/518 /opt/unetlab/addons/dynamips/ios/c7200-adventerprisek9-mz.152-4.S2.bin

# -s must be after -p

# dynamips -P 2600 -t 2621 -l /opt/unetlab/tmp/0/TestLab/6/R6.log -i 1 -r 128 -o 4 -n 128 -c 0x2102 -X -s 0:0:tap:vunl0_6_0  /opt/unetlab/addons/dynamips/ios/c2600-adventerprisek9-mz.124-25d.bin


Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        unassigned      YES unset  administratively down down
FastEthernet1/0        unassigned      YES unset  administratively down down
FastEthernet1/1        unassigned      YES unset  administratively down down
FastEthernet2/0        unassigned      YES unset  administratively down down
FastEthernet2/1        unassigned      YES unset  administratively down down
Serial3/0              unassigned      YES unset  administratively down down
Serial3/1              unassigned      YES unset  administratively down down
Serial3/2              unassigned      YES unset  administratively down down
Serial3/3              unassigned      YES unset  administratively down down
Serial3/4              unassigned      YES unset  administratively down down
Serial3/5              unassigned      YES unset  administratively down down
Serial3/6              unassigned      YES unset  administratively down down
Serial3/7              unassigned      YES unset  administratively down down


# ovs-vsctl add-port br-test $TAP
# dynamips -P 2600 -t 2621 -l dynamips_log.txt -i 1 -r 128 -o 4 -n 128 -c 0x2102 -X -s 0:0:tap:$TAP c2600-adventerprisek9-mz.124-25d.bin
# ovs-vsctl add-port br-test tap0

A
              unix:<local_sock>:<remote_sock>
                     Use  unix  sockets  for  local  communication.  <local_sock> is created and represents the local NIC.  <remote_sock> is the file used by the other
                     interface.  (ex. "/tmp/local:/tmp/remote")
:
*/

#include <ctype.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/select.h>
#include <sys/wait.h>
#include <unistd.h>

#include "include/afsocket.h"
#include "include/cmd.h"
#include "include/functions.h"
#include "include/serial2udp.h"
#include "include/tap.h"
#include "include/ts.h"
#include "dynamips_functions.h"

#include "include/params.h"

int device_id = -1;                         // Device ID
int tenant_id = -1;                         // Tenant ID
int tsclients_socket[FD_SETSIZE];           // Telnet active clients (socket), tsclients_socket[0] is the index

int main (int argc, char *argv[]) {
    // Child's CMD line
    int m = sysconf(_SC_ARG_MAX);           // Maximum CMD line length
    char *cmd;                              // Store child's CMD line
    cmd = (char *) calloc(m, sizeof(char));

    // Child's parameters
    int *child_delay = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *child_delay = 0;                       // Delay before starting (shared between parent and child)
    int child_pid = -1;                     // PID after the fork()
    int child_status = -1;                  // Used during waitpid()
    char *child_file = NULL;                // Binary file

    // Telnet server
    int ts_port = -1;                       // TCP (console) and UDP (serial converter) port
    char *xtitle = "Terminal Server";       // Title for telnet clients

    // Select parameters
    int *infd = calloc(2, sizeof(int));     // Array of integers [0] is for reading, [1] is for writing
    int *outfd = calloc(2, sizeof(int));    // Array of integers [0] is for reading, [1] is for writing
    fd_set active_fd_set;                   // Contains active FD using in select()
    FD_ZERO(&active_fd_set);
    fd_set read_fd_set;                     // Contains FD selected in current loop
    FD_ZERO(&read_fd_set);

    // Other parameters
    int i = -1;                             // Counter
    int j = -1;                             // Counter
    int opt = NULL;                         // Store CMD options
    int rc = -1;                            // Generic return code
    char *tmp = NULL;                       // Generic char string
    struct sigaction sa;                    // Manage signals (SIGHUP, SIGTERM...)

    // Wrapper parameters
    int child_afsocket[100];                // Store AF_UNIX child sockets
    memset(&child_afsocket, 0, sizeof(child_afsocket));
    int ser_remoteid[64];                   // Store Remote Device ID (used for UDP communication)
    memset(&ser_remoteid, 0, sizeof(ser_remoteid));
    int ser_remoteif[64];                   // Store Remote Interface ID (used for UDP communication)
    memset(&ser_remoteif, 0, sizeof(ser_remoteif));
    int udpserver_socket = -1;              // UDP socket for serial communications
    int wrapper_afsocket[100];              // Store AF_UNIX wrapper sockets
    memset(&wrapper_afsocket, 0, sizeof(wrapper_afsocket));

    // Parsing options
    while ((opt = getopt(argc, argv, ":vT:D:d:t:F:x")) != -1) {
        switch (opt) {
            default:
                usage(argv[0]);
                exit(1);
            // Begin standard parameters
            case 'v':
                printf("%s\n", VERSION);
                exit(0);
            case 'T':
                // Mandatory: Tenant ID
                tenant_id = atoi(optarg);
                if (tenant_id < 0) {
                    printf("ERR: tenant_id must be integer.\n");
                    exit(1);
                }
                break;
            case 'D':
                // Mandatory: Device ID
                device_id = atoi(optarg);
                if (tenant_id < 0) {
                    printf("ERR: device_id must be integer.\n");
                    exit(1);
                }
                break;
            case 'F':
                // Mandatory: IOS
                child_file = optarg;
                if (is_file(child_file) != 0) {
                    printf("ERR: file '%s' does not exist.\n", child_file);
                    exit(1);
                }
                break;
            case 'd':
                // Optional: child's startup delay (default 0)
                *child_delay = atoi(optarg);
                if (child_delay < 0) {
                    printf("ERR: delay must be integer.\n");
                    exit(1);
                }
                break;
            case 't':
                // Optional: telnet window title (default "Terminal Server")
                xtitle = optarg;
                break;
        }
    }

    // Checking if tenant_id is set
    if (tenant_id < 0) {
        printf("ERR: tenant ID not set.\n");
        exit(1);
    }

    // Checking if device_id is set
    if (device_id < 0) {
        printf("ERR: device ID not set.\n");
        exit(1);
    }

    // Checking if child_file is set
    if (child_file == NULL) {
        printf("%u:%u ERR: subprocess executable not set.\n", tenant_id, device_id);
        exit(1);
    }

    // Building the CMD line
    ts_port = 32768 + 128 * tenant_id + device_id;
    tmp = (char *) malloc(m * sizeof(char));
    sprintf(tmp, "/usr/bin/dynamips -N '%s' -T %i", xtitle, ts_port);
    cmd_add(&cmd, tmp);
    free(tmp);

    // Adding parameters after "--"
    j = 0;
    for (i = 1; i < argc; i++) {
        if (j == 1) {
            // Adding parameter given after "--"
            cmd_add(&cmd, " ");
            cmd_add(&cmd, argv[i]);
        }
        if (strcmp(argv[i], "--") == 0) {
            // Found "--"
            j = 1;
        }
    }

    // Adding the IOS filename
    cmd_add(&cmd, " ");
    cmd_add(&cmd, child_file);

    // Creating PIPEs for select()
    if ((pipe(infd)) < 0 || pipe(outfd) < 0) {
         printf("%u:%u ERR: failed to create PIPEs (%s).\n", tenant_id, device_id, strerror(errno));
         exit(1);
    }

    // Forking
    if ((rc = fork()) == 0) {
        // Child: stating subprocess
        if (DEBUG > 0) printf("DEBUG: starting child (%s).\n", cmd);
        if (child_delay > 0) {
            // Delay is set, waiting
            for (; *child_delay > 0;) {
                rc = write(outfd[1], ".", 1);
                *child_delay = *child_delay - 1;
                sleep(1);
            }
            rc = write(outfd[1], "\n", 1);
        }
        close(STDIN_FILENO);            // Closing child's stdin
        close(STDOUT_FILENO);           // Closing child's stdout
        dup2(infd[0], STDIN_FILENO);    // Linking stdin to PIPE
        dup2(outfd[1], STDOUT_FILENO);  // Linking stdout to PIPE
        dup2(outfd[1], STDERR_FILENO);  // Redirect child's stderr to child's stdout
        close(infd[0]);
        close(infd[1]);
        close(outfd[0]);
        close(outfd[1]);
        // Start process
        rc = cmd_start(cmd);
        // Subprocess terminated, killing the parent
        printf("%u:%u ERR: child terminated (%i).\n", tenant_id, device_id, rc);
    } else if (rc > 0) {
        // Parent
        close(infd[0]);                     // Used by the child
        close(outfd[1]);                    // Used by the child

        // Handling Signals
        signal(SIGPIPE,SIG_IGN);            // Ignoring SIGPIPE when a client terminates
        sa.sa_handler = &signal_handler;    // Setup the sighub handler
        sa.sa_flags = SA_RESTART;           // Restart the system call, if at all possible
        sigemptyset(&sa.sa_mask);           // Signals blocked during the execution of the handler
        sigaddset(&sa.sa_mask, SIGHUP);     // Signal 1
        sigaddset(&sa.sa_mask, SIGINT);     // Signal 2
        sigaddset(&sa.sa_mask, SIGTERM);    // Signal 15
        sigfillset(&sa.sa_mask);

        // Intercept SIGHUP, SIGINT, SIGUSR1 and SIGTERM
        if (sigaction(SIGHUP, &sa, NULL) == -1) {
            printf("%u:%u ERR: cannot handle SIGHUP (%s).\n", tenant_id, device_id, strerror(errno));
        }
        if (sigaction(SIGINT, &sa, NULL) == -1) {
            printf("%u:%u ERR: cannot handle SIGINT (%s).\n", tenant_id, device_id, strerror(errno));
        }
        if (sigaction(SIGTERM, &sa, NULL) == -1) {
            printf("%u:%u ERR: cannot handle SIGTERM (%s).\n", tenant_id, device_id, strerror(errno));
        }

        // Preparing select()
        FD_ZERO(&active_fd_set);
        FD_ZERO(&read_fd_set);
        if (udpserver_socket > 0) {
            FD_SET(udpserver_socket, &active_fd_set); // Adding UDP socket
        }

        // While subprocess is running, check IO from subprocess, telnet clients, socket and network
        waitpid(child_pid, &child_status, 0);
        // Child is no more running
        printf("%u:%u ERR: child is no more running.\n", tenant_id, device_id);
    } else {
        printf("%u:%u ERR: failed to fork (%s).\n", tenant_id, device_id, strerror(errno));
        exit(1);
    }
    exit(0);
}
