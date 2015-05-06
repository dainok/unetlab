// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/includes/cmd.c
 *
 * CMD line functions for wrappers.
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

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "params.h"

extern int device_id;
extern int tenant_id;

// CMD: add a single command to the CMD line
void cmd_add(char **cmd_line, const char *cmd) {
    if ((int) strnlen(*cmd_line, sizeof(*cmd_line)) + (int) strnlen(cmd, sizeof(*cmd)) + 1 > sysconf(_SC_ARG_MAX)) {
        // String too long
        printf("ERR: cannot add command '%s' (string too long).\n", cmd);
        exit(1);
    }
    strncat(*cmd_line, cmd, strlen(cmd));
}

// CMD: start a subprocess
int cmd_start(const char *cmd) {
    int rc = -1;
    rc = system(cmd);
    return rc;
}
