/**
 * wrappers/includes/serial2udp.h
 *
 * Serial to UDP converter for wrappers.
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

// Serial to UDP Converter: listen
int serial2udp_listen(int port, int *server_socket);

// Serial to UDP Converter: add end-point
int serial2udp_add(int *remote_socket, int *remote_id, int *remote_if, char *serial2udp_map);

// Serial to UDP Converter: receive
int serial2udp_receive(char **c, int server_socket);
