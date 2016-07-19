// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/include/afsocket.h
 *
 * Socket functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <sys/types.h>

// AF_UNIX socket: listen
int afsocket_listen(char *server_socketfile, char *remote_socketfile, int *server_socket, int *remote_socket);

// AF_UNIX socket: receive
int afsocket_receive(void *c, int server_socket, int bytesToRead);
