// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/iol_functions.c
 *
 * Functions for iol_wrapper.
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
