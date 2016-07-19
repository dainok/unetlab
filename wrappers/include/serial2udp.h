/**
 * wrappers/include/serial2udp.h
 *
 * Serial to UDP converter for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <sys/types.h>

// Serial to UDP Converter: listen
int serial2udp_listen(int port, int *server_socket);

// Serial to UDP Converter: add end-point
int serial2udp_add(int *remote_socket, int *remote_id, int *remote_if, char *serial2udp_map);

// Serial to UDP Converter: receive
int serial2udp_receive(void *c, int server_socket, int bytesToRead);
