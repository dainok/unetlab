// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/include/cmd.c
 *
 * CMD line functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "log.h"

#include "params.h"

extern int device_id;
extern int tenant_id;

// CMD: add a single command to the CMD line
void cmd_add(char **cmd_line, const char *cmd) {
    if ((int) strnlen(*cmd_line, sizeof(*cmd_line)) + (int) strnlen(cmd, sizeof(*cmd)) + 1 > sysconf(_SC_ARG_MAX)) {
        // String too long
        UNLLog(LLERROR, "Cannot add command '%s' (string too long).\n", cmd);
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
