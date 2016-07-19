// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/include/functions.c
 *
 * Functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <arpa/inet.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <unistd.h>

#include "params.h"
#include "log.h"

extern int device_id;
extern int tenant_id;
extern int tsclients_socket[];

// Check if a string is valid (not empty, not null)
int is_string(char *s) {
    if (s == NULL || *s == '\0') {
        return -1;
    } else {
        return 0;
    }
}

// Check if a string is numeric
int is_numeric(char *s) {
    if (is_string(s) == 0 && isdigit(*s) != 0) {
        return 0;
    } else {
        return -1;
    }
}

// Check if a string is hexadecimal
int is_hex(char *s) {
    int rc = -1;
    if ((rc = (int) strtol(s, NULL, 0)) == 0 || rc == -1) {
        return -1;
    } else {
        return 0;
    }
}

// Check if a file exists
int is_file(char *s) {
    if (access(s, F_OK) == -1) {
        return -1;
    } else {
        return 0;
    }
}

// Handling Signals
void signal_handler(int signal) {
    int i = 0;
    // Find out which signal we're handling
    switch (signal) {
        case SIGHUP:
            // Signal 1
            UNLLog(LLINFO, "Caught SIGHUP, closing clients.\n");
            for (i = tsclients_socket[0]; i > 0; i++) {
                UNLLog(LLINFO, "Closing client (%i).\n", tsclients_socket[i]);
                close(tsclients_socket[i]);
            }
            break;
        case SIGINT:
            // Signal 2
            UNLLog(LLINFO, "Caught SIGINT, killing child.\n");
            break;
        case SIGTERM:
            // Signal 15
            UNLLog(LLINFO, "Caught SIGTERM, killing child.\n");
            break;
        default:
            UNLLog(LLWARNING, "Caught wrong signal (%d).\n", signal);
            break;
    }
}

// Print version
void version() {
    printf("%s\n", VERSION);
}

unsigned hash(const char * data, int nLength) {
   int A = 54059; /* a prime */
   int B = 76963; /* another prime */
   unsigned h = 31; // prime
   while (nLength-- > 0) {
     h = (h * A) ^ (data[0] * B);
     data++;
   }
   return h; // or return h % C;
}
