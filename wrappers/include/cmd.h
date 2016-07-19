// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/include/cmd.h
 *
 * CMD line functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license https://opensource.org/licenses/BSD-3-Clause
 * @link http://www.unetlab.com/
 * @version 20160126
 */

#include <sys/types.h>

// CMD: add a single command to the CMD line
void cmd_add(char **cmd_line, char *cmd);

// CMD: start a subprocess
int cmd_start(const char *cmd);

