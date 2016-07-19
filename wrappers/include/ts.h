/**
 * wrappers/include/ts.h
 *
 * Terminal server functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <sys/types.h>

// Terminal Server: listen
int ts_listen(int port, int *server_socket);

// Terminal Server: accept new connection
int ts_accept(fd_set *fd_set, int server_socket, char *xtitle, int *client_socket, int sendHeader);

// Terminal Server: broadcast a char to all clients
void ts_broadcast_string(char * string, fd_set *fd_set, int *client_socket);
void ts_broadcast(char c, fd_set *fd_set, int *client_socket);

// Terminal Server: receive a char from a client
int ts_receive(unsigned char *c, fd_set *fd_read, fd_set *fd_active, int *client_socket);
