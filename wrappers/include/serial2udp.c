// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/include/serial2udp.c
 *
 * Serial to UDP converter for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "log.h"

#include "params.h"

extern int device_id;
extern int tenant_id;

// Serial to UDP Converter: listen
int serial2udp_listen(int port, int *server_socket) {
    int rc = -1;
    struct addrinfo testing_addr;   // remote_addr used inside getaddrinfo()
    memset((char *) &testing_addr, 0, sizeof(testing_addr));
    struct sockaddr_in6 server_addr;
    memset((char *) &server_addr, 0, sizeof(server_addr));

    // Opening sock
    *server_socket = socket(AF_INET6, SOCK_DGRAM, 0);
    if (*server_socket < 0) {
        rc = 1;
        UNLLog(LLERROR, "Error while listening for serial2udp wrapper. ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }

    // Setting options
    server_addr.sin6_family = AF_INET6;
    server_addr.sin6_addr = in6addr_any;
    server_addr.sin6_port = htons(port);

    // Binding (checking if address is already in use)
    if (bind(*server_socket, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0) {
        rc = 2;
        UNLLog(LLERROR, "Error while binding for serial2udp wrapper. ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }
    return 0;
}

// Serial to UDP Converter: add end-point
int serial2udp_add(int *remote_socket, int *remote_id, int *remote_if, char *serial2udp_map) {
    int i = 0;
    char tmp_srcif[10];
    memset((char *) &tmp_srcif, 0, sizeof(tmp_srcif));
    char tmp_dst[100];
    memset((char *) &tmp_dst, 0, sizeof(tmp_dst));
    char tmp_dstid[100];
    memset((char *) &tmp_dstid, 0, sizeof(tmp_dstid));
    char tmp_dstif[10];
    memset((char *) &tmp_dstif, 0, sizeof(tmp_dstif));
    char tmp_dstport[10];
    int rc = -1;
    struct addrinfo *result_addr;   // remote_addr saved as output of getaddrinfo()
    memset((char *) &result_addr, 0, sizeof(result_addr));
    struct addrinfo *remote_addr;   // remote_addr after getaddrinfo()
    memset((char *) &remote_addr, 0, sizeof(remote_addr));
    struct addrinfo testing_addr;   // remote_addr used inside getaddrinfo()
    memset((char *) &testing_addr, 0, sizeof(testing_addr));

    // Setting options
    testing_addr.ai_family = AF_UNSPEC;            // Allow IPv4 or IPv6
    testing_addr.ai_socktype = SOCK_DGRAM;

    // Looking for source interface
    for (; serial2udp_map[i] != ':'; i++) {
        if (serial2udp_map[i] == '\0') {
            rc = 3;
            UNLLog(LLERROR, "Invalid map (%s).\n", serial2udp_map);
            return 3;
        }
        strncat(tmp_srcif, &serial2udp_map[i], 1);
    }
    // Looking for detination hostname
    for (++i; serial2udp_map[i] != ':'; i++) {
        if (serial2udp_map[i] == '\0') {
            rc = 3;
            UNLLog(LLERROR, "Invalid map (%s).\n", serial2udp_map);
            return 3;
        }
        strncat(tmp_dst, &serial2udp_map[i], 1);
    }
    // Looking for destination ID
    for (++i; serial2udp_map[i] != ':'; i++) {
        if (serial2udp_map[i] == '\0') {
            rc = 3;
            UNLLog(LLERROR, "Invalid map (%s).\n", serial2udp_map);
            return 3;
        }
        strncat(tmp_dstid, &serial2udp_map[i], 1);
    }
    // Looking for destination interface
    for (++i; serial2udp_map[i] != ',' && serial2udp_map[i] != 0; i++) {
        if (serial2udp_map[i] == ':') {
            rc = 3;
            UNLLog(LLERROR, "Invalid map (%s).\n", serial2udp_map);
            return 3;
        }
        strncat(tmp_dstif, &serial2udp_map[i], 1);
    }
    // Setting the destination UDP port
    sprintf(tmp_dstport, "%i", 32768 + 128 * tenant_id + atoi(tmp_dstid));

    UNLLog(LLINFO, "Creating UDP MAP (src: %i:%s, dst: %s:%s, dst_id %s:%s).\n", device_id, tmp_srcif, tmp_dst, tmp_dstport, tmp_dstid, tmp_dstif);

    // Looking for an IPv4 or IPv6 address
    if ((rc = getaddrinfo(tmp_dst, tmp_dstport, &testing_addr, &result_addr)) != 0) {
        // Failed to get address
        rc = 4;
        UNLLog(LLERROR, "Failed to create UDP map (getaddrinfo). ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }
    for (remote_addr = result_addr; remote_addr != NULL; remote_addr = remote_addr -> ai_next) {
        remote_socket[atoi(tmp_srcif)] = socket(remote_addr -> ai_family, remote_addr -> ai_socktype, remote_addr -> ai_protocol);
        if (remote_socket[atoi(tmp_srcif)] == -1) {
            // Wrong address/AF_FAMILY
            continue;
        }
        if (connect(remote_socket[atoi(tmp_srcif)], remote_addr -> ai_addr, remote_addr -> ai_addrlen) != -1) {
            // Working address/AF_FAMILY -> Exiting
            break;
        }
        close(remote_socket[atoi(tmp_srcif)]);
    }
    if (remote_addr == NULL) {
        // Failed to get address
        rc = 5;
        UNLLog(LLERROR, "Failed to create UDP map (cannot find a working address). ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }

    // We need to store remote device ID and remote interface ID also
    remote_id[atoi(tmp_srcif)] = atoi(tmp_dstid);
    remote_if[atoi(tmp_srcif)] = atoi(tmp_dstif);

    freeaddrinfo(result_addr);  // Nod needed anymore

    UNLLog(LLINFO, "Configured serial2udp wrapper (s=%i, int=%i, remote_id=%i, remote_if=%i.\n", remote_socket[atoi(tmp_srcif)], atoi(tmp_srcif), remote_id[atoi(tmp_srcif)], remote_if[atoi(tmp_srcif)]);
    return 0;
}

// Serial to UDP Converter: receive
int serial2udp_receive(void *c, int server_socket, int bytesToRead) {
    int length = 0;
    //memset(c, 0, sizeof(*c)); // useless memset

    if ((length = read(server_socket, c, bytesToRead)) <= 0) {
        // Read error
        UNLLog(LLERROR, "Failed to receive data from UDP (s=%i, l=%i). ERR: %s (%i).\n", server_socket, length, strerror(errno), length);
        return length;
    }
    UNLLog(LLVERBOSE, "Received data from UDP (s=%i, l=%i).\n", server_socket, length);
    return length;
}
