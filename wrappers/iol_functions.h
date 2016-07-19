// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/iol_functions.h
 *
 * Functions for iol_wrapper.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <sys/types.h>

// Print usage
void usage(char *bin);

// Handling Signals
void signal_handler(int signal);

// Creating NETMAP
int mk_netmap();

// Creating AF sockets for IOL communication
int mk_afsocket(int *wrapper_socket, int *iol_socket);

// Creating TAP interfaces
int mk_tap(int iol_eth, int *iol_tap);

// Check if a given interface is ethernet (0) or serial (1)
int is_eth(int i);

// Receiving packet from AF_UNIX
int packet_af(int af_socket, int *iol_fd, int *udp_fd, int *remote_id, int *remote_if);

// Receiving packet from TAP
int packet_tap(int tap_socket, int af_socket, int iol_ifid);

// Receiving packet from UDP
int packet_udp(int udp_socket, int ah_socket);
