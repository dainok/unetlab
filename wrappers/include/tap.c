/**
 * wrappers/includes/tap.c
 *
 * TAP functions for wrappers.
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
#include <errno.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/un.h>
#include <unistd.h>

// Linux API
#include <linux/if.h>
#include <linux/if_tun.h>

#include "functions.h"

#include "params.h"

extern int device_id;
extern int tenant_id;

// TAP interface: listen
int tap_listen(char *tap_name, int *tap_fd) {
    char tmp[200];
    char *tun_dev = "/dev/net/tun";
    int rc = -1;
    int tap_socket = -1;
    struct ifreq ifr;

    ifr.ifr_flags = IFF_TAP;                    // We want TAP interface (not TUN)
    ifr.ifr_flags |= IFF_NO_PI;                 // Do not add 4 bytes preamble (we want to send RAW packets)
    strncpy(ifr.ifr_name, tap_name, IFNAMSIZ);  // Setting device name

    // Checking TAP interface
    sprintf(tmp, "/sys/class/net/%s/dev_id", tap_name);
    if (is_file(tmp) != 0) {
        rc = 1;
        if (DEBUG > 0) printf("DEBUG: skipping non existent TAP interface (%s).\n", tap_name);
        return rc;
    }

    // Open the clone device
    if ((*tap_fd = open(tun_dev, O_RDWR)) < 0) {
        rc = 2;
        if (DEBUG > 0) printf("DEBUG: error while calling open TUN (%s).\n", tap_name);
        printf("%u:%u ERR: %s (%i).\n", tenant_id, device_id, strerror(errno), rc);
        return rc;
    }

    // Creating TAP interface
    if (ioctl(*tap_fd, TUNSETIFF, (void *)&ifr) < 0) {
        rc = 3;
        if (DEBUG > 0) printf("DEBUG: skipping TAP (%s), maybe it's not used (%s).\n", tap_name, strerror(errno));
        return rc;
    }

    // Activate interface
    if ((tap_socket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        rc = 4;
        if (DEBUG > 0) printf("DEBUG: error while activating TAP interface (%s).\n", tap_name);
        printf("%u:%u ERR: %s (%i).\n", tenant_id, device_id, strerror(errno), rc);
        return rc;
    }

    // Put the inteface "up" 
    ifr.ifr_flags |= IFF_UP;
    if (ioctl(tap_socket, SIOCSIFFLAGS, &ifr) < 0) {
        rc = 5;
        if (DEBUG > 0) printf("DEBUG: error while putting TAP interface up (%s).\n", tap_name);
        printf("%u:%u ERR: %s (%i).\n", tenant_id, device_id, strerror(errno), rc);
        // unl_wrapper will bring the interface in up state
        //return rc;
    }
    if (DEBUG > 1) printf("DEBUG: TAP interface configured (s=%i, n=%s).\n", *tap_fd, tap_name);
    return 0;
}

// TAP interface: receive
int tap_receive(char **c, int server_socket) {
    int length = 0;
    memset(c, 0, sizeof(*c));

    if ((length = read(server_socket, c, BUFFER)) <= 0) {
        // Read error
        if (DEBUG > 0) printf("DEBUG: failed to receive data from TAP (s=%i, l=%i).\n", server_socket, length);
        printf("%u:%u ERR: %s (%i).\n", tenant_id, device_id, strerror(errno), length);
        return length;
    }
    if (DEBUG > 1) printf("DEBUG: received data from TAP (s=%i, l=%i).\n", server_socket, length);
    return length;
}
