// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/iol_wrapper.c
 *
 * Wrapper for IOL.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
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
#include <stdarg.h>

#include "include/afsocket.h"
#include "include/cmd.h"
#include "include/functions.h"
#include "include/serial2udp.h"
#include "include/tap.h"
#include "include/ts.h"
#include "iol_functions.h"
#include "include/log.h"
#include "include/params.h"

int device_id = -1;                         // Device ID
int tenant_id = -1;                         // Tenant ID
int tsclients_socket[FD_SETSIZE];           // Telnet active clients (socket), tsclients_socket[0] is the index
int child_eth = 2;                          // Ethernet porgroups
int child_ser = 2;                          // Serial portgroups

int main (int argc, char *argv[]) {
    CheckLogLevelFileTrigger("/tmp/unl_ll_debug",LLDEBUG);
    CheckLogLevelFileTrigger("/tmp/unl_ll_verbose",LLVERBOSE);

    setpgrp();  // Become the leader of its group.

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
    int ts_socket = -1;                     // Telnet server socket
    char child_output = '\0';               // Store single char from child
    unsigned char client_input = '\0';               // Store single char from client
    char *xtitle = "Terminal Server";       // Title for telnet clients

    // Select parameters
    int *infd = calloc(2, sizeof(int));     // Array of integers [0] is for reading, [1] is for writing
    int *outfd = calloc(2, sizeof(int));    // Array of integers [0] is for reading, [1] is for writing
    int active_fd = -1;                     // Contains current active FD
    fd_set active_fd_set;                   // Contains active FD using in select()
    FD_ZERO(&active_fd_set);
    fd_set read_fd_set;                     // Contains FD selected in current loop
    FD_ZERO(&read_fd_set);

    // Wrapper parameters
    int child_afsocket = -1;                // Store AF_UNIX child socket
    int *eth_socket = calloc(64, sizeof(int));  // Store FD of ethernet intefaces
    int *ser_remoteid = calloc(64, sizeof(int));// Store Remote Device ID (used for UDP communication)
    int *ser_remoteif = calloc(64, sizeof(int));// Store Remote Interface ID (used for UDP communication)
    int *ser_socket = calloc(64, sizeof(int));  // Store FD of serial intefaces
    int udpserver_socket = -1;              // UDP socket for serial communications
    int wrapper_afsocket = -1;              // Store AF_UNIX wrapper socket

    // Other parameters
    int af_ready = 0;                       // 1 = AF_UNIX files are configured (needed if IOL is delayed)
    int i = -1;                             // Counter
    int j = -1;                             // Counter
    int opt = NULL;                         // Store CMD options
    int rc = -1;                            // Generic return code
    char *tmp = NULL;                       // Generic char string
    struct sigaction sa;                    // Manage signals (SIGHUP, SIGTERM...)

    // Check for iourc file
    tmp = (char *) malloc(m * sizeof(char));
    sprintf(tmp, "iourc");
    if (is_file(tmp) != 0) {
        UNLLog( LLERROR, "File '%s' does not exist.\n", tmp);
        exit(1);
    }
    free(tmp);

    // Adding options to child's CMD line
    while ((opt = getopt(argc, argv, ":vT:D:d:t:F:e:s:l:")) != -1) {
        switch (opt) {
            default:
                usage(argv[0]);
                exit(1);
            // Begin standard parameters
            case 'v':
                version();
                exit(0);
            case 'T':
                // Mandatory: Tenant ID
                tenant_id = atoi(optarg);
                if (tenant_id < 0) {
                    UNLLog( LLERROR, "Tenant_id must be integer.\n");
                    exit(1);
                }
                UNLLog(LLINFO, "Tennant_id = %i\n", tenant_id);
                break;
            case 'D':
                // Mandatory: Device ID
                device_id = atoi(optarg);
                if (tenant_id < 0) {
                    UNLLog( LLERROR, "Device_id must be integer.\n");
                    exit(1);
                }
                UNLLog(LLINFO, "Device_id = %i\n", device_id);
                break;
            case 'F':
                child_file = optarg;
                if (is_file(child_file) != 0) {
                    UNLLog( LLERROR, "File '%s' does not exist.\n", child_file);
                    exit(1);
                }
                break;
            case 'd':
                // Optional: child's startup delay (default 0)
                *child_delay = atoi(optarg);
                if (*child_delay < 0) {
                    UNLLog( LLERROR, "Delay must be integer.\n");
                    exit(1);
                }
                break;
            case 't':
                // Optional: telnet window title (default "Terminal Server")
                xtitle = optarg;
                break;
            // End standard parameters
            // Optional: number of Ethernet progroups (default: 2)
            case 'e':
                child_eth = atoi(optarg);
                if (child_eth < 0) {
                    UNLLog( LLERROR, "Ethernet portgroup must be integer.\n");
                    exit(1);
                }
                break;
            // Optional: number of Serial progroups (default: 2)
            case 's':
                child_ser = atoi(optarg);
                if (child_ser < 0) {
                    UNLLog( LLERROR, "Serial portgroup must be numeric.\n");
                    exit(1);
                }
                break;
            // Optional: Serial link end-point (no default)
            case 'l':
                if ((tenant_id == -1) && (device_id == -1)) {
                  UNLLog( LLERROR, "Flag '-l' must be after '-T' and '-D'.\n");
                  exit(1);
                }
                if (udpserver_socket == -1) {
                  // First Serial2UDP definition, must listen()
                  if ((rc = serial2udp_listen(32768 + 128 * tenant_id + device_id, &udpserver_socket)) != 0) {
                    UNLLog( LLERROR, "Failed to open UDP socket (%i).\n", rc);
                    exit(1);
                  }
                }
                if ((rc = serial2udp_add(ser_socket, ser_remoteid, ser_remoteif, optarg)) != 0) {
                  UNLLog( LLERROR, "Failed to add serial end-point (%i).\n", rc);
                  exit(1);
                }
                break;
        }
    }

    // Checking if tenant_id is set
    if (tenant_id < 0) {
        UNLLog( LLERROR, "Tenant ID not set.\n");
        exit(1);
    }

    // Checking if device_id is set
    if (device_id < 0) {
        UNLLog( LLERROR, "Device ID not set.\n");
        exit(1);
    }

    // Checking if child_file is set
    if (child_file == NULL) {
        UNLLog( LLERROR, "Subprocess executable not set.\n");
        exit(1);
    }

    // Checking total interfaces
    if (child_eth + child_ser > 16) {
        UNLLog( LLERROR, "Ethernet + Serial portgroups must lower equal than 16.\n");
        exit(1);
    }

    // Building the CMD line
    cmd_add(&cmd, "LD_LIBRARY_PATH=/opt/unetlab/addons/iol/lib ");
    cmd_add(&cmd, child_file);

    // Adding interfaces
    tmp = (char *) malloc(m * sizeof(char));
    sprintf(tmp, " -e %i -s %i", child_eth, child_ser);
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

    // Adding device_id as last
    tmp = (char *) malloc(m * sizeof(char));
    sprintf(tmp, "%i", device_id);
    cmd_add(&cmd, " ");
    cmd_add(&cmd, tmp);
    free(tmp);

    // Creating NETMAP
    if ((rc = mk_netmap()) != 0) {
        UNLLog( LLERROR, "Failed to create NETMAP file (%i).\n", rc);
        exit(1);
    }

    // Creating PIPEs for select()
    if ((pipe(infd)) < 0 || pipe(outfd) < 0) {
         UNLLog( LLERROR, "Failed to create PIPEs (%s).\n", strerror(errno));
         exit(1);
    }

    // Telnet listen
    ts_port = 32768 + 128 * tenant_id + device_id;
    tsclients_socket[0] = 0;
    if ((rc = ts_listen(ts_port, &ts_socket)) != 0) {
        UNLLog( LLERROR, "Failed to open TCP socket (%i).\n", rc);
        exit(1);
    }

    // Creating TAP interfaces
    if ((rc = mk_tap(child_eth, eth_socket)) != 0) {
        UNLLog( LLERROR, "Failed to create TAP interfaces (%i).\n", rc);
        kill(0, SIGTERM);
        exit(1);
    }

    // Forking
    if ((rc = fork()) == 0) {
        // Child: starting subprocess
        UNLLog( LLINFO, "Starting child (%s).\n", cmd);
        if (*child_delay > 0) {
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
        UNLLog( LLERROR, "Child terminated (%i).\n", rc);
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
            UNLLog( LLERROR, "Cannot handle SIGHUP (%s).\n", strerror(errno));
        }
        if (sigaction(SIGINT, &sa, NULL) == -1) {
            UNLLog( LLERROR, "Cannot handle SIGINT (%s).\n", strerror(errno));
        }
        if (sigaction(SIGTERM, &sa, NULL) == -1) {
            UNLLog( LLERROR, "Cannot handle SIGTERM (%s).\n", strerror(errno));
        }

        // Preparing select()
        FD_ZERO(&active_fd_set);
        FD_ZERO(&read_fd_set);
        UNLLog( LLINFO, "Adding subprocess stdout descriptor (%i).\n", outfd[0]);
        FD_SET(outfd[0], &active_fd_set);         // Adding subprocess stdout
        UNLLog( LLINFO, "Adding telnet socket descriptor (%i).\n", ts_socket);
        FD_SET(ts_socket, &active_fd_set);        // Adding telnet socket
        if (udpserver_socket > 0) {
            UNLLog( LLINFO, "Adding UDP socket descriptor (%i).\n", udpserver_socket);
            FD_SET(udpserver_socket, &active_fd_set); // Adding UDP socket
        }

        // Adding TAP interfaces for select()
        for (i = 0; i <= 63; i++) {
            if (eth_socket[i] > 0) {
                UNLLog( LLINFO, "Adding TAP interface descriptor (%i).\n", eth_socket[i]);
                FD_SET(eth_socket[i], &active_fd_set);
            }
        }

        // While subprocess is running, check IO from subprocess, telnet clients, socket and network
        //int rrc = 0;
        while ( waitpid(child_pid, &child_status, WNOHANG|WUNTRACED) == 0) {
            // Creating AF communication from child
            if (af_ready == 0 && *child_delay == 0) {
                // wait 3 seconds for AF_UNIX
                sleep(3);
                if ((rc = mk_afsocket(&wrapper_afsocket, &child_afsocket)) != 0) {;
                    UNLLog(LLERROR, "Failed to create AF_UNIX socket file (%i).\n", rc);
                    kill(0, SIGTERM);
                    break;
                }
                af_ready = 1;
                UNLLog(LLINFO, "Adding wrapper socket descriptor (%i).\n", wrapper_afsocket);
                FD_SET(wrapper_afsocket, &active_fd_set);   // Adding subprocess AF_UNIX socket
            }

            // Check if select() is valid
            read_fd_set = active_fd_set;
            if ((active_fd = select(FD_SETSIZE, &read_fd_set, NULL, NULL, NULL)) <= 0) {
                UNLLog(LLERROR, "Failed to select().Error: %s\n",strerror(errno));
                kill(0, SIGTERM);
                break;
            }
            UNLLog(LLVERBOSE, "Data from select descriptor (%i).\n", active_fd);

            // Check if output from child
            if (FD_ISSET(outfd[0], &read_fd_set)) {
                if (read(outfd[0], &child_output, 1) <= 0) {
                    UNLLog(LLERROR, "Error while reading data from the subprocess, killing it.\n");
                    kill(0, SIGTERM);
                    break;
                }
                // Writing to all telnet clients
                ts_broadcast(child_output, &active_fd_set, tsclients_socket);
            }

            // Check if new client is coming
            if (FD_ISSET(ts_socket, &read_fd_set)) {
                if ((rc = ts_accept(&active_fd_set, ts_socket, xtitle, tsclients_socket,1)) != 0) {
                    UNLLog(LLERROR, "Failed to accept a new client (%i).\n", rc);
                }
            }

            // Check for output from all telnet clients
            if (ts_receive(&client_input, &read_fd_set, &active_fd_set, tsclients_socket) == 0) {
                // Write to child
                rc = write(infd[1], &client_input, 1);
                if (rc < 0) {
                    UNLLog(LLERROR, "Error writing to the subprocess, closing.\n");
                    kill(0, SIGTERM);
                    break;
                }
            }

            // If AF, UDP and TAP sockets are configured, check for packets
            if (af_ready == 1) {
                // Check for packets from subprocess
                if (FD_ISSET(wrapper_afsocket, &read_fd_set)) {
                    if ((rc = packet_af(wrapper_afsocket, eth_socket, ser_socket, ser_remoteid, ser_remoteif)) != 0) {
                        UNLLog(LLERROR, "Error forwarding packet from AF_UNIX socket to TAP/UDP (%i).\n", rc);
                        kill(0, SIGTERM);
                        break;
                    }
                }

                // Check for packets from TAP interfaces
                for (i = 0; i <= 63; i++) {
                    if (eth_socket[i] > 0 && FD_ISSET(eth_socket[i], &read_fd_set)) {
                        if ((rc = packet_tap(eth_socket[i], child_afsocket, i)) != 0) {
                            if (rc == 3) {
                              af_ready = 0;
                              UNLLog(LLERROR, "Failed to forward TAP => AF_UNIX. Will try to recreate it later...\n");
                            } else {
                              UNLLog(LLERROR, "Error forwarding packet from TAP to AF_UNIX socket (%i).\n", rc);
                              kill(0, SIGTERM);
                              break;
                            }
                        }
                    }
                }

                // Check for incoming serial (UDP) packets
                if (udpserver_socket > 0) {
                    if (FD_ISSET(udpserver_socket, &read_fd_set)) {
                        if ((rc = packet_udp(udpserver_socket, child_afsocket)) != 0) {
                            if (rc == 3) {
                                af_ready = 0;
                                UNLLog(LLERROR, "Failed to forward UDP => AF_UNIX. Will try to recreate it later...\n");
                            } else {
                                UNLLog(LLERROR, "Error forwarding packet from UDP to AF_UNIX (%i).\n", rc);
                                kill(0, SIGTERM);
                                break;
                            }
                        }
                    }
                }
            }

            // We should not have other active dscriptor
        }

        // Child is no more running
        UNLLog(LLINFO, "Child is no more running.\n");
        //printf("rrc = %i\n",rrc);
        //exit(1);
    } else {
        UNLLog(LLERROR, "Failed to fork.\n");
        exit(1);
    }
    close(ts_socket);
    close(wrapper_afsocket);
    exit(0);
}
