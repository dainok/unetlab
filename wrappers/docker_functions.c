// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/docker_functions.c
 *
 * Functions for docker_wrapper.
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
    printf("Usage: %s <standard options> -- attach <Docker ID>\n", bin);
    printf("Standard Options:\n");
    printf("-T <n>    *Tenant ID\n");
    printf("-D <n>    *Device ID\n");
    printf("-t <desc>  Window (xterm) title\n");
    printf("-F <n>    *Docker executable\n");
    printf("* Mandatory option\n");
    exit(1);
}
