// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/include/functions.h
 *
 * Functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <sys/types.h>

// Check if a string is valid (not empty, not null)
int is_string(char *s);

// Check if a string is numeric
int is_numeric(char *s);

// Check if a string is hexadecimal
int is_hex(char *s);

// Check if a file exists
int is_file(char *s);

// Handling Signals
void signal_handler(int signal);

// Print version
void version();

// Just simple hash
unsigned hash(const char * data, int nLength);
