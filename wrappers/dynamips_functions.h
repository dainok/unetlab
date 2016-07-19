// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/dynamips_functions.h
 *
 * Functions for dynamips_wrapper.
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

// Check if router platform is valid
int is_platform(char **family, char *platform);

// Check if module is valid
int is_module(const char *module, const int size);

// Check if link is valid
int is_link(const char *link, const int length);

// Check if is Ethernet link
int is_ethlink(const char *link, const int length);
