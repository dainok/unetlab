// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/iol_functions.c
 *
 * Functions for iol_wrapper.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <unistd.h>
#include "include/functions.h"

// Linux API
#include <linux/if.h>
#include <linux/if_tun.h>

#include "include/afsocket.h"
#include "include/cmd.h"
#include "include/functions.h"
#include "include/serial2udp.h"
#include "include/tap.h"
#include "include/ts.h"
#include "include/log.h"

#include "include/params.h"

extern int device_id;
extern int child_eth;
extern int child_ser;
extern int tenant_id;
extern int tsclients_socket[];

// Print usage
void usage(const char *bin) {
    printf("Usage: %s <standard options> <specific options>\n", bin);
    printf("Standard Options:\n");
    printf("-T <n>    *Tenant ID\n");
    printf("-D <n>    *Device ID\n");
    printf("-d <n>     Delayed start in seconds (default 0)\n");
    printf("-t <desc>  Window (xterm) title\n");
    printf("Specific Options:\n");
    printf("-F <n>    *IOL Image\n");
    printf("-r <n>     Size of RAM (default 256)\n");
    printf("-o <n>     Size of ROM (default 4)\n");
    printf("-n <n>     Size of NVRAM (default 128)\n");
    printf("-e <n>     Number of Ethernet portgroups (default 2, max 16 included serials)\n");
    printf("-s <n>     Number of Serial portgroups (default 2, max 16 included ethernets)\n");
    printf("-l <n>     Ethernet/Serial link end-point (g.e. 0:0:tap:vunl0_6_0)\n");
    printf("-c <name>  Startup configuration file name\n");
    printf("* Mandatory option\n");
    printf("WARNING: use the above parameter order!\n");
    exit(1);
}

// Creating NETMAP
int mk_netmap() {
    FILE *f_iol_netmap;
    int d = 0;
    int iol_id = device_id;
    int rc = 0;
    int wrapper_id = iol_id + 512;
    if (access("NETMAP", F_OK) != -1 && remove("NETMAP") != 0) {
        rc = 1;
        UNLLog(LLERROR, "Cannot create NETMAP file (access). ERR: %s (%i)\n", strerror(errno), rc);
        return rc;
    }
    f_iol_netmap = fopen("NETMAP", "a");
    if (f_iol_netmap == NULL) {
        rc = 2;
        UNLLog(LLERROR, "Cannot create NETMAP file (fopen). ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }
    for (d = 0; d < 64; d++) {
        fprintf(f_iol_netmap, "%u:%u %u:%u\n", iol_id, d, wrapper_id, d);
    }
    fclose(f_iol_netmap);
    UNLLog(LLINFO, "NETMAP file created.\n");
    return 0;
}

// Creating AF sockets for child communication
int mk_afsocket(int *wrapper_socket, int *iol_socket) {
    char iol_socketfile[100];                   // Store AF_UNIX socket
    memset(&iol_socketfile, 0, sizeof(iol_socketfile));
    char wrapper_socketfile[100];               // Store AF_UNIX socket filename
    memset(&wrapper_socketfile, 0, sizeof(wrapper_socketfile));
    char tmp_netio[100];
    memset(&tmp_netio, 0, sizeof(tmp_netio));
    char tmp[100];
    memset(&tmp, 0, sizeof(tmp));
    int iol_id = device_id;
    int wrapper_id = iol_id + 512;
    int rc = -1;

    // Creating netio directory
    strncpy(tmp_netio, "/tmp/netio", sizeof(tmp_netio));
    sprintf(tmp, "%u", getuid());
    strcat(tmp_netio, tmp);
    strncat(tmp_netio, "\0", sizeof(*tmp_netio));
    mkdir(tmp_netio, S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH);

    // Setting  AF_UNIX (wrapper) socket and lock
    strncpy(wrapper_socketfile, tmp_netio, sizeof(wrapper_socketfile));
    strncat(wrapper_socketfile, "/", sizeof(*wrapper_socketfile));
    sprintf(tmp, "%u", wrapper_id);
    strcat(wrapper_socketfile, tmp);

    if ( *wrapper_socket != -1 ) {
      close(*wrapper_socket);
      *wrapper_socket = -1;
    }

    if (access(wrapper_socketfile, F_OK) != -1 && remove(wrapper_socketfile) != 0) {
        rc = 1;
        UNLLog(LLERROR, "Cannot access AF_UNIX (%s). ERR: %s (%i).\n", tmp,  strerror(errno), rc);
        return rc;
    }

    // Setting AF_UNIX (child) socket
    strncpy(iol_socketfile, tmp_netio, sizeof(iol_socketfile));
    strncat(iol_socketfile, "/", sizeof(*iol_socketfile));
    sprintf(tmp, "%u", iol_id);
    strcat(iol_socketfile, tmp);
    strncat(iol_socketfile, "\0", sizeof(*iol_socketfile));

    // Creating sockets
    if ((rc = afsocket_listen(wrapper_socketfile, iol_socketfile, wrapper_socket, iol_socket)) != 0) {
        UNLLog(LLERROR, "Cannot listen at AF_UNIX (%s). ERR: Cannot open AF_UNIX sockets (%i).\n", tmp, rc);
        return 2;
    }

    return 0;
}

// Creating TAP interfaces
int mk_tap(int child_eth, int *iol_tap) {
    char tap_name[20];
    memset(&tap_name, 0, sizeof(tap_name));
    int i = 0;
    int j = 0;
    int rc = -1;
    int tap_fd = -1;

    // Create all interfaces
    for (i = 0; i < child_eth; i++) {
        for (j = 0; j <= 3; j++) {
            sprintf(tap_name, "vunl%u_%u_%u", tenant_id, device_id, i + 16 * j);
            if ((rc = tap_listen(tap_name, &tap_fd)) != 0) {
                rc = 1;
                UNLLog(LLVERBOSE, "Skipping TAP (%s) interface (%i).\n", tap_name, rc);
            } else {
                // Add TAP interface to the active ethernet list
                iol_tap[i + 16 * j] = tap_fd;
            }
        }
    }
    return 0;
}

// Check if a given interface is ethernet (0) or serial (1)
int is_eth(int i) {
    // i = x/y -> i = x + y * 16 -> x = i - y * 16 = i % 16
    if (i % 16 < child_eth) {
        return 0;
    } else {
        return 1;
    }
}

// Receiving packet from AF_UNIX
int packet_af(int af_socket, int *iol_fd, int *udp_fd, int *remote_id, int *remote_if) {
  
//    char *iol_frame;
//    char eth_frame[1518];
//    memset(&eth_frame, 0, sizeof(eth_frame));
//    char ser_frame[1526];
//    memset(&ser_frame, 0, sizeof(ser_frame));
  
    char tmp_frame[BUFFER];
    memset(&tmp_frame, 0, sizeof(tmp_frame));
  
    int iol_ifid = -1;
    int length = -1;
    int rc = -1;

    /* 
     * IOL 64 bit header:
     * - 16 bits for the destination IOL ID
     * - 16 bits for the source IOL ID
     * - 8 bits for the destination interface (z = x/y -> z = x + 3 * 16)
     * - 8 bits for the source interface (z = x/y -> z = x + y * 16)
     * - 16 bits equals to 0x0100
     * Destination TAP interface is: vunlT_U_Z (T = tenant_id, U = device_id, Z = interface_id)
     */

    /* 
     * UNL 64 bit header:
     * - 8 bits for the destination Tenant ID
     * - 8 bits for the source Tenant ID
     * - 16 bits for the destination Device ID
     * - 16 bits for the source Device ID
     * - 8 bits for the destination interface
     * - 8 bits for the source interface
     */

    if ((length = afsocket_receive(&tmp_frame, af_socket,sizeof(tmp_frame))) <= 0) {
        // Read error
        rc = 1;
        UNLLog(LLERROR, "Failed to receive packet from AF_UNIX (%i). ERR: %s (%i). \n", length, strerror(errno), rc);
        return rc;
    } else {
        //memcpy(tmp_frame, &iol_frame, length);
        iol_ifid = (int) tmp_frame[5];
        if (is_eth(iol_ifid) == 0) {
            // Ethernet: packet to TAP
            //memcpy(eth_frame, &tmp_frame[8], length - 8);
            if (iol_fd[iol_ifid] != 0 && write(iol_fd[iol_ifid], &tmp_frame[8], length - 8) < 0) {
                // If TAP interface is configured, send packet through it
                rc = 3;
                UNLLog(LLERROR, "Failed to send a packet to TAP (src: vunl%u_%u_%u). ERR: %s (%i).\n", tenant_id, device_id, iol_ifid, strerror(errno), rc);
                return rc;
            }
            UNLLog(LLVERBOSE, "Sent TAP frame (dst: %02x%02x.%02x%02x.%02x%02x, src: %02x%02x.%02x%02x.%02x%02x, length: %i) to vunl%u_%u_%u.\n",
                     tmp_frame[8] & 0xff, tmp_frame[9] & 0xff, tmp_frame[10] & 0xff, tmp_frame[11] & 0xff, tmp_frame[12] & 0xff, tmp_frame[13] & 0xff,
                     tmp_frame[14] & 0xff, tmp_frame[15] & 0xff, tmp_frame[16] & 0xff, tmp_frame[17] & 0xff, tmp_frame[18] & 0xff, tmp_frame[19] & 0xff,
                     length - 8,
                     tenant_id, device_id, iol_ifid);
            return 0;
        } else {
            if (udp_fd[iol_ifid] == 0) {
                UNLLog(LLERROR, "Failed to send a packet to unconfigured UDP (src: vunl%u_%u_%u).\n", tenant_id, device_id, iol_ifid);
                return 0;
            }
            // Now send packet via UDP
            // TODO: Intra Tenant Link
            int dst_tenant_id = tenant_id;
            //memcpy(ser_frame, &tmp_frame, length);      // size(header(IOL)) == size(header(UNETLAB))
            tmp_frame[0] = dst_tenant_id;               // Destination Tenant ID (TODO Intra Tenant Link)
            tmp_frame[1] = tenant_id;                   // Source Tenant ID
            tmp_frame[2] = remote_id[iol_ifid] >> 8;    // Destination Device ID (TODO)
            tmp_frame[3] = remote_id[iol_ifid] & 255;
            tmp_frame[4] = device_id >> 8;              // Source Device ID
            tmp_frame[5] = device_id & 255;
            tmp_frame[6] = remote_if[iol_ifid];         // Destination Interface ID
            tmp_frame[7] = iol_ifid;                    // Source Interface ID (TODO)
            UNLLog(LLVERBOSE, "Received IOL packet from device %u:%u:%u to device %u:%u:%u\n", tenant_id, device_id, iol_ifid, dst_tenant_id, remote_id[iol_ifid], remote_if[iol_ifid]);

            if (write(udp_fd[iol_ifid], tmp_frame, length) < 0) {
                // Sometimes packets cannot be delivered if end point is not active (Connection refused)
                UNLLog(LLERROR, "Failed to send a packet to UDP (src: vunl%u_%u_%u).\n", tenant_id, device_id, iol_ifid);
                return 0;
            }
            UNLLog(LLVERBOSE, "Sent UDP (s=%i, l=%i)\n", udp_fd[iol_ifid], length);
            return 0;
        }
    }
}

// Receiving packet from TAP
int packet_tap(int tap_socket, int af_socket, int iol_ifid) {
    int iol_id = device_id;
    int length = -1;
    int rc = -1;
    int wrapper_id = iol_id + 512;
  
//    char *eth_frame;
//    char iol_frame[1522];
//    memset(&iol_frame, 0, sizeof(iol_frame));
  
    char tmp_frame[BUFFER];
    memset(&tmp_frame, 0, sizeof(tmp_frame));

    /* 
     * IOL 64 bit header:
     * - 16 bits for the destination IOL ID
     * - 16 bits for the source IOL ID
     * - 8 bits for the destination interface (z = x/y -> z = x + 3 * 16)
     * - 8 bits for the source interface (z = x/y -> z = x + y * 16)
     * - 16 bits equals to 0x0100
     * Destination TAP interface is: vunlT_U_Z (T = tenant_id, U = device_id, Z = interface_id)
     */

    if ((length = tap_receive(&tmp_frame[8], tap_socket,sizeof(tmp_frame)-8)) <= 0) {
        // Read error
        rc = 1;
        UNLLog(LLERROR, "Failed to receive packet from TAP (%i, %i). ERR: %s (%i).\n", tap_socket, length, strerror(errno), rc);
        return rc;
    } else if (length > 1514) {
        UNLLog(LLWARNING, "Ignoring frame from TAP (%i) because too long (%i).\n", tap_socket, length);
        return 0; // The wrapper will continue to work
    } else {
        //memcpy(tmp_frame, &eth_frame, length);
        // Now send packet to AF_UNIX
        tmp_frame[0] = iol_id >> 8;         // IOL device ID
        tmp_frame[1] = iol_id & 255;
        tmp_frame[2] = wrapper_id >> 8;     // WRAPPER device ID
        tmp_frame[3] = wrapper_id & 255;
        tmp_frame[4] = iol_ifid;            // IOL device ID
        tmp_frame[5] = iol_ifid;            // WRAPPER device ID
        tmp_frame[6] = 1;
        tmp_frame[7] = 0;
        //memcpy(&iol_frame[8], &tmp_frame, length);
        if ((write(af_socket, tmp_frame, length + 8)) < 0) {
            rc = 3;
            UNLLog(LLERROR, "Failed forwarding data to AF_UNIX (%i) socket. ERR: %s (%i).\n", af_socket, strerror(errno), rc);
            return rc;
        } else {
            UNLLog(LLVERBOSE, "Sent eth frame (dst: %02x%02x.%02x%02x.%02x%02x, src: %02x%02x.%02x%02x.%02x%02x, length: %i) to AF_UNIX\n",
                    tmp_frame[8] & 0xff, tmp_frame[9] & 0xff, tmp_frame[10] & 0xff, tmp_frame[11] & 0xff, tmp_frame[12] & 0xff, tmp_frame[13] & 0xff,
                    tmp_frame[14] & 0xff, tmp_frame[15] & 0xff, tmp_frame[16] & 0xff, tmp_frame[17] & 0xff, tmp_frame[18] & 0xff, tmp_frame[19] & 0xff,
                    length);
            UNLLog(LLVERBOSE, "Sent eth frame to AF_UNIX (dst: %u:%u, src: %u:%u\n",
                    256 * (int) tmp_frame[0] + (int) tmp_frame[1], (int) tmp_frame[4],
                    256 * (int) tmp_frame[2] + (int) tmp_frame[3], (int) tmp_frame[5]);
            return 0;
        }
    }
    return 1; // Dummy return for stupid gcc
}

// Receiving packet from UDP
int packet_udp(int udp_socket, int af_socket) {
    int iol_id = device_id;
    int length = -1;
    int rc = -1;
    int wrapper_id = iol_id + 512;
  
    char ser_frame[BUFFER];
    memset(ser_frame, 0, sizeof(ser_frame));
  
    int dst_tenant_id = 0;
    int dst_device_id = 0;
    int dst_device_if = 0;
    int src_tenant_id = 0;
    int src_device_id = 0;
    int src_device_if = 0;

    /* 
     * IOL 64 bit header:
     * - 16 bits for the destination IOL ID
     * - 16 bits for the source IOL ID
     * - 8 bits for the destination interface (z = x/y -> z = x + 3 * 16)
     * - 8 bits for the source interface (z = x/y -> z = x + y * 16)
     * - 16 bits equals to 0x0100
     * Destination TAP interface is: vunlT_U_Z (T = tenant_id, U = device_id, Z = interface_id)
     */

	/*
	 * UNL 64 bit header:
	 * - 8 bits for the destination Tenant ID (TT)
	 * - 8 bits for the source Tenant ID (tt)
	 * - 16 bits for the destination Device ID (DDDD)
	 * - 16 bits for the source Device ID (dddd)
	 * - 8 bits for the destination interface (II)
	 * - 8 bits for the source interface (ii)
	 * # tcpdump -i lo -X -nn udp
	 * 14:20:37.096862 IP6 ::1.37773 > ::1.32770: UDP, length 309
	 *         0x0000:  6000 0000 013d 1140 0000 0000 0000 0000  `....=.@........
	 *         0x0010:  0000 0000 0000 0001 0000 0000 0000 0000  ................
	 *         0x0020:  0000 0000 0000 0001 938d 8002 013d 12e7  .............=..
	 *         0x0030:  TTtt DDDD dddd IIii 8f00 2000 02b4 151c  ................
	 * [...]
	 */

    if ((length = serial2udp_receive(ser_frame, udp_socket, sizeof(ser_frame))) <= 0) {
        // Read error
        rc = 1;
        UNLLog(LLERROR, "Failed to receive packet from UDP (%i). ERR: %s (%i).\n", length, strerror(errno), rc);
        return rc;
    } else if (length > 1522) {
        UNLLog(LLERROR, "Ignoring frame from UDP because too long (%i).\n", length);
        return 0;
    } else if (length < 8) {
        UNLLog(LLERROR, "Ignoring frame from UDP because too short (%i).\n", length);
        return 0;
    } else {
        dst_tenant_id = ser_frame[0];
        src_tenant_id = ser_frame[1];
        dst_device_id = (ser_frame[2] << 8) + ser_frame[3];
        src_device_id = (ser_frame[4] << 8) + ser_frame[5];
        dst_device_if = ser_frame[6];
        src_device_if = ser_frame[7];
        if (dst_tenant_id != tenant_id) {
            UNLLog(LLERROR, "Ignoring frame from UDP because wrong tenant_id (%i).\n", dst_tenant_id);
            return 0;
        }
        if (dst_device_id != device_id) {
            UNLLog(LLERROR, "Ignoring frame from UDP because wrong device_id (%i).\n", dst_device_id);
            return 0;
        }
        // Now send packet to AF_UNIX
        ser_frame[0] = dst_device_id >> 8;  // IOL device ID
        ser_frame[1] = dst_device_id & 255;
        ser_frame[2] = wrapper_id >> 8;     // WRAPPER device ID
        ser_frame[3] = wrapper_id & 255;
        ser_frame[4] = dst_device_if;       // IOL device ID
        ser_frame[5] = dst_device_if;       // WRAPPER device ID
        ser_frame[6] = 1;
        ser_frame[7] = 0;
        UNLLog(LLVERBOSE, "Received UDP packet from device %u:%u:%u to device %u:%u:%u\n", src_tenant_id, src_device_id, src_device_if, dst_tenant_id, dst_device_id, dst_device_if);
        if ((write(af_socket, ser_frame, length)) < 0) {
            rc = 3;
            UNLLog(LLERROR, "Failed forwarding data to AF_UNIX (%i) socket.  ERR: %s (%i). \n", af_socket, strerror(errno), rc);
            return rc;
        } else {
            UNLLog(LLVERBOSE, "Sent ser frame to AF_UNIX (dst: %u:%u, src: %u:%u)\n",
                    256 * (int) ser_frame[0] + (int) ser_frame[1], (int) ser_frame[4],
                    256 * (int) ser_frame[2] + (int) ser_frame[3], (int) ser_frame[5]);
            return 0;
        }
        return 0;
    }
}
