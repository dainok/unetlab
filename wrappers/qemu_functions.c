// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/qemu_functions.c
 *
 * Functions for qemu_wrapper.
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
