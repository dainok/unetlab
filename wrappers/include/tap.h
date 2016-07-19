/**
 * wrappers/include/tap.h
 *
 * TAP functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <sys/types.h>

// TAP interface: listen
int tap_listen(char *tap_name, int *tap_fd);

// TAP interface: receive
int tap_receive(void *c, int server_socket, int bytesToRead);
