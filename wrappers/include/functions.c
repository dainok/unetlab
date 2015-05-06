// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/includes/functions.c
 *
 * Functions for wrappers.
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
            if (DEBUG > 0) printf("DEBUG: Caught SIGHUP, closing clients.\n");
            for (i = tsclients_socket[0]; i > 0; i++) {
                if (DEBUG > 1) printf("DEBUG: closing client (%i).\n", tsclients_socket[i]);
                close(tsclients_socket[i]);
            }
            break;
        case SIGINT:
            // Signal 2
            if (DEBUG > 0) printf("DEBUG: Caught SIGINT, killing child.\n");
            break;
        case SIGTERM:
            // Signal 15
            if (DEBUG > 0) printf("DEBUG: Caught SIGTERM, killing child.\n");
            break;
        default:
            if (DEBUG > 0) printf("DEBUG: caught wrong signal (%d).\n", signal);
            break;
    }
}

// Print version
void version() {
    printf("%s\n", VERSION);
}
