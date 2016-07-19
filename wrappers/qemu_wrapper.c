// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/qemu_wrapper.c
 *
 * Wrapper for QEMU.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/*
 * Example:
 *  /opt/unetlab/wrappers/qemu_wrapper -T 3 -D 0 -t "vIOS" -d 0 -F /usr/bin/qemu-system-i386 -- -machine type=pc-1.0,accel=kvm:tcg -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc -no-shutdown -boot order=c -smp 1 -m 384 -device e1000,netdev=net0,mac=52:54:00:03:00:00 -netdev tap,id=net0,ifname=vunl3_0_0,script=no -device e1000,netdev=net1,mac=52:54:00:03:00:01 -netdev tap,id=net1,ifname=vunl3_0_1,script=no -device e1000,netdev=net2,mac=52:54:00:03:00:02 -netdev tap,id=net2,ifname=vunl3_0_2,script=no -device e1000,netdev=net3,mac=52:54:00:03:00:03 -netdev tap,id=net3,ifname=vunl3_0_3,script=no
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/select.h>
#include <sys/wait.h>
#include <unistd.h>

#include "include/cmd.h"
#include "include/functions.h"
#include "include/ts.h"
#include "include/log.h"
#include "qemu_functions.h"

#include "include/params.h"

int device_id = -1;                         // Device ID
int tenant_id = -1;                         // Tenant ID
int tsclients_socket[FD_SETSIZE];           // Telnet active clients (socket), tsclients_socket[0] is the index

int main (int argc, char *argv[]) {
    setpgrp();  // Become the leader of its group.
    // Child's CMD line
    int m = sysconf(_SC_ARG_MAX);           // Maximum CMD line length
    char *cmd;                              // Store child's CMD line
    cmd = (char *) calloc(m, sizeof(char));

    // Child's parameters
    int *child_delay = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *child_delay = 0;                       // Delay before starting (shared between parent and child)
    char *child_file = NULL;                // Binary file
    int child_pid = -1;                     // PID after the fork()
    int child_status = -1;                  // Used during waitpid()

    // Telnet server
    int ts_socket = -1;                     // Telnet server socket
    int ts_port = -1;                       // TCP (console) and UDP (serial converter) port
    char child_output = '\0';               // Store single char from child
    unsigned char client_input = '\0';               // Store single char from client
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
    int vnc = 0;                            // If 1, enable VNC console
    struct sigaction sa;                    // Manage signals (SIGHUP, SIGTERM...)

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
                    UNLLog(LLERROR,"Tenant_id must be integer.\n");
                    exit(1);
                }
                UNLLog(LLINFO, "Tennant_id = %i\n", tenant_id);
                break;
            case 'D':
                // Mandatory: Device ID
                device_id = atoi(optarg);
                if (device_id < 0) {
                    UNLLog(LLERROR,"Device_id must be integer.\n");
                    exit(1);
                }
                UNLLog(LLINFO, "Device_id = %i\n", device_id);
                break;
            case 'F':
                // Mandatory: subprocess executable
                child_file = optarg;
                if (is_file(child_file) != 0) {
                    UNLLog(LLERROR,"File '%s' does not exist.\n", child_file);
                    exit(1);
                }
                break;
            case 'd':
                // Optional: child's startup delay (default 0)
                *child_delay = atoi(optarg);
                if (*child_delay < 0) {
                    UNLLog(LLERROR,"Delay must be integer.\n");
                    exit(1);
                }
                break;
            case 't':
                // Optional: telnet window title (default "Terminal Server")
                xtitle = optarg;
                break;
            case 'x':
                // Optiona: disable STD output (serial console) and enable VNC console
                vnc = 1;
                break;
        }
    }

    // Checking if tenant_id is set
    if (tenant_id < 0) {
        UNLLog(LLERROR, "Tenant ID not set.\n");
        exit(1);
    }

    // Checking if device_id is set
    if (device_id < 0) {
        UNLLog(LLERROR, "Device ID not set.\n");
        exit(1);
    }

    // Checking if child_file is set
    if (child_file == NULL) {
        UNLLog(LLERROR, "Subprocess executable not set.\n");
        exit(1);
    }

    // Building the CMD line
    cmd_add(&cmd, child_file);

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

    // Creating PIPEs for select()
    if ((pipe(infd)) < 0 || pipe(outfd) < 0) {
         UNLLog(LLERROR, "Failed to create PIPEs (%s).\n", strerror(errno));
         exit(1);
    }

    // Telnet listen
    if (vnc != 1) {
        ts_port = 32768 + 128 * tenant_id + device_id;
        tsclients_socket[0] = 0;
        if ((rc = ts_listen(ts_port, &ts_socket)) != 0) {
            UNLLog(LLERROR, "Failed to open TCP socket (%i).\n", rc);
            exit(1);
        }
    }

    // Forking
    if ((rc = fork()) == 0) {
        // Child: stating subprocess
        UNLLog(LLINFO, "Starting child (%s).\n", cmd);
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
        UNLLog(LLERROR, "Child terminated (%i).\n", rc);
    } else if (rc > 0) {
        // Parent
        close(infd[0]);     // Used by the child
        close(outfd[1]);    // Used by the child

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
            UNLLog(LLERROR, "Cannot handle SIGHUP (%s).\n", strerror(errno));
        }
        if (sigaction(SIGINT, &sa, NULL) == -1) {
            UNLLog(LLERROR, "Cannot handle SIGINT (%s).\n", strerror(errno));
        }
        if (sigaction(SIGTERM, &sa, NULL) == -1) {
            UNLLog(LLERROR, "Cannot handle SIGTERM (%s).\n", strerror(errno));
        }

        // Preparing select()
        if (vnc != 1) {
            FD_ZERO(&active_fd_set);
            FD_ZERO(&read_fd_set);
            FD_SET(outfd[0], &active_fd_set);         // Adding subprocess stdout
            FD_SET(ts_socket, &active_fd_set);        // Adding telnet socket

            // While subprocess is running, check IO from subprocess, telnet clients, socket and network
            while (waitpid(child_pid, &child_status, WNOHANG|WUNTRACED) == 0) {
                // Check if select() is valid
                read_fd_set = active_fd_set;
                if (select(FD_SETSIZE, &read_fd_set, NULL, NULL, NULL) <= 0) {
                    UNLLog(LLERROR, "Failed to select().\n");
                    kill(0, SIGTERM);
                    break;
                }

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
            }
        } else {
            waitpid(child_pid, &child_status, 0);
            // Child is no more running
            UNLLog(LLERROR, "Child is no more running.\n");
        }
    } else {
        UNLLog(LLERROR, "Failed to fork.\n" );
        exit(1);
    }
    close(ts_socket);
    exit(0);
}
