// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/qemu_functions.c
 *
 * Functions for qemu_wrapper.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <stdio.h>
#include <stdlib.h>

// Print usage
void usage(const char *bin) {
    printf("Usage: %s <standard options> -- <QEMU options>\n", bin);
    printf("Standard Options:\n");
    printf("-T <n>    *Tenant ID\n");
    printf("-D <n>    *Device ID\n");
    printf("-d <n>     Delayed start in seconds (default 0)\n");
    printf("-t <desc>  Window (xterm) title\n");
    printf("-F <n>    *QEMU executable\n");
    printf("-x         Enable VNC console\n");
    printf("* Mandatory option\n");
    exit(1);
}
