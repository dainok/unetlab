/**
 * wrappers/include/tap.c
 *
 * TAP functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
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
#include "log.h"
#include "params.h"


extern int sLogLevel;

// TAP interface: listen
int tap_listen(char *tap_name, int *tap_fd) {
    char tmp[200];
    char *tun_dev = "/dev/net/tun";
    int rc = -1;
    int tap_socket = -1;
    struct ifreq ifr;
    memset(&ifr,0,sizeof(ifr));
    ifr.ifr_flags = IFF_TAP;                    // We want TAP interface (not TUN)
    ifr.ifr_flags |= IFF_NO_PI;                 // Do not add 4 bytes preamble (we want to send RAW packets)
    strncpy(ifr.ifr_name, tap_name, IFNAMSIZ);  // Setting device name

    // Checking TAP interface
    sprintf(tmp, "/sys/class/net/%s/dev_id", tap_name);
    if (is_file(tmp) != 0) {
        rc = 1;
        UNLLog(LLVERBOSE, "Skipping non existent TAP interface (%s).\n", tap_name);
        return rc;
    }

    // Open the clone device
    if ((*tap_fd = open(tun_dev, O_RDWR)) < 0) {
        rc = 2;
        UNLLog(LLERROR, "Error while calling open TUN (%s). ERR: %s (%i)\n", tap_name, strerror(errno), rc);
        return rc;
    }

    // Creating TAP interface
    if (ioctl(*tap_fd, TUNSETIFF, (void *)&ifr) < 0) {
        rc = 3;
        UNLLog(LLINFO, "Skipping TAP (%s), maybe it's not used (%s).\n", tap_name, strerror(errno));
        return rc;
    }

    // Activate interface
    if ((tap_socket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        rc = 4;
        UNLLog(LLERROR, "Error while activating TAP interface (%s). ERR: %s (%i).\n", tap_name, strerror(errno), rc);
        return rc;
    }

    // Put the inteface "up" 
    ifr.ifr_flags |= IFF_UP;
    if (ioctl(tap_socket, SIOCSIFFLAGS, &ifr) < 0) {
        rc = 5;
        UNLLog(LLVERBOSE, "Error while putting TAP interface up (%s). ERR: %s (%i). Is interface already up?\n", tap_name, strerror(errno), rc);
        // unl_wrapper will bring the interface in up state
        //return rc;
    }
    UNLLog(LLINFO, "TAP interface configured (s=%i, n=%s).\n", *tap_fd, tap_name);
    return 0;
}

// TAP interface: receive
int tap_receive(void *c, int server_socket, int bytesToRead) {
    int length = 0;
    //memset(c, 0, sizeof(*c));

    if ((length = read(server_socket, c, bytesToRead)) <= 0) {
        // Read error
        UNLLog(LLERROR, "Failed to receive data from TAP (s=%i, l=%i). ERR: %s (%i).\n", server_socket, length, strerror(errno), length);
        return length;
    }
    if ( sLogLevel >= LLVERBOSE ) { // In order to avoid excessive hash calculation 
        UNLLog(LLVERBOSE, "Received data from TAP (s=%i, l=%i) Hash = %i\n", server_socket, length, hash((const char*)c, length));
    }
    return length;
}
