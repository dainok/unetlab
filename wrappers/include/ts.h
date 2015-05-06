/**
 * wrappers/includes/ts.h
 *
 * Terminal server functions for wrappers.
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

// Terminal Server: listen
int ts_listen(int port, int *server_socket);

// Terminal Server: accept new connection
int ts_accept(fd_set *fd_set, int server_socket, char *xtitle, int *client_socket);

// Terminal Server: broadcast a char to all clients
void ts_broadcast(char c, fd_set *fd_set, int *client_socket);

// Terminal Server: receive a char from a client
int ts_receive(char *c, fd_set *fd_read, fd_set *fd_active, int *client_socket);
