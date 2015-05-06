// vim: syntax=c tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/dynamips_functions.c
 *
 * Functions for dynamips_wrapper.
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

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <unistd.h>

#include "include/afsocket.h"
#include "include/cmd.h"
#include "include/functions.h"
#include "include/serial2udp.h"
#include "include/tap.h"
#include "include/ts.h"

#include "include/params.h"

extern int device_id;
extern int tenant_id;
extern int tsclients_socket[];

// Print usage
void usage(const char *bin) {
	printf("Usage: %s <standard options> <specific options>\n", bin);
	printf("Standard Options:\n");
	printf("-T <n>	*Tenant ID\n");
	printf("-D <n>	*Device ID\n");
	printf("-d <n>	 Delayed start in seconds (default 0)\n");
	printf("-t <desc>  Window (xterm) title\n");
	printf("Specific Options:\n");
	printf("-p <n>	*Router Platform (g.e. 2620)\n");
	printf("-r <n>	 Size of RAM (default 256)\n");
	printf("-o <n>	 Size of ROM (default 4)\n");
	printf("-n <n>	 Size of NVRAM (default 128)\n");
	printf("-i <n>	 Idle-PC value\n");
	printf("-m <n>	 Additional module (g.e. 1:PA-2FE-TX)\n");
	printf("-e <n>	 Active Ethernet interface (n = x/y -> n = 16 * x + y)\n");
	printf("-l <n>	 Ethernet/Serial link end-point (g.e. 0:0:tap:vunl0_6_0)\n");
	printf("-c <name>  Startup configuration file name\n");
	printf("-F <n>	*IOS Image\n");
	printf("* Mandatory option\n");
	printf("WARNING: use the above parameter order!\n");
	exit(1);
}

// Check if router platform is valid
int is_platform(char **family, const char *platform) {
	if (
		// 1700
			strcmp(platform, "1710") == 0 ||
			strcmp(platform, "1720") == 0 ||
			strcmp(platform, "1721") == 0 ||
			strcmp(platform, "1750") == 0 ||
			strcmp(platform, "1751") == 0 ||
			strcmp(platform, "1760") == 0) {
		*family = "1700";
		 return 0;
	} else if (
		// 2600
			strcmp(platform, "2610") == 0 || 
			strcmp(platform, "2611") == 0 || 
			strcmp(platform, "2620") == 0 || 
			strcmp(platform, "2621") == 0 || 
			strcmp(platform, "2610XM") == 0 || 
			strcmp(platform, "2650XM") == 0) {
		*family = "2600";
		return 0;
	} else if (
		// 2691
			strcmp(platform, "2691") == 0) {
		*family = "2691";
		return 0;
	} else if (
		// 3600
			strcmp(platform, "3620") == 0 ||
			strcmp(platform, "3640") == 0 ||
			strcmp(platform, "3660") == 0) {
		*family = "3600";
		return 0;
	} else if (
		// 3725
			strcmp(platform, "3725") == 0) {
		*family = "3725";
		return 0;
	} else if (
		// 3745
			strcmp(platform, "3745") == 0) {
		*family = "3745";
		return 0;
	} else if (
		// 7200
			strcmp(platform, "npe-100") == 0 ||
			strcmp(platform, "npe-150") == 0 ||
			strcmp(platform, "npe-175") == 0 ||
			strcmp(platform, "npe-200") == 0 ||
			strcmp(platform, "npe-225") == 0 ||
			strcmp(platform, "npe-300") == 0 ||
			strcmp(platform, "npe-400") == 0) {
		*family = "7200";
	}
	return -1;
}

// Check if module is valid
int is_module(const char *module, const int length) {
	int rc = -1;
	char *tmp = strdup(module);
	char *slot = strtok(tmp, ":");	  // Must be numeric
	char *model = strtok(NULL, ":");	// Must be a valid model
	char *final = strtok(NULL, ":");	// Must be NULL (no traling chars)

	if (is_numeric(slot) != 0 || is_string(model) != 0 || is_string(final) == 0 || module[length - 1] == ':') {
		// Not a string or leading ':' found
		rc = -1;
	} else if (
		// 1700 specific
			strcmp(model, "C1700-MB-1ETH") == 0 ||
			strcmp(model, "C1710-MB-1FE-1E") == 0 ||
		// 2600 specific
			strcmp(model, "CISCO2600-MB-1E") == 0 ||
			strcmp(model, "CISCO2600-MB-2E") == 0 ||
			strcmp(model, "CISCO2600-MB-1FE") == 0 ||
			strcmp(model, "CISCO2600-MB-2FE") == 0 ||
		// 7200 specific
			strcmp(model, "NPE-G2") == 0 ||
			strcmp(model, "C7200-IO-FE") == 0 ||
			strcmp(model, "PA-FE-TX") == 0 ||
			strcmp(model, "PA-4E") == 0 ||
			strcmp(model, "PA-8E") == 0 ||
			strcmp(model, "PA-4T+") == 0 ||
			strcmp(model, "PA-8T") == 0 ||
			strcmp(model, "PA-A1") == 0 ||
			strcmp(model, "PA-POS-OC3") == 0 ||
			strcmp(model, "C7200-JC-PA") == 0 ||
		// Various
			strcmp(model, "NM-1E") == 0 ||
			strcmp(model, "NM-4E") == 0 ||
			strcmp(model, "NM-1FE-TX") == 0 ||
			strcmp(model, "NM-16ESW") == 0 ||
			strcmp(model, "GT96100-FE") == 0 ||
			strcmp(model, "NM-4T") == 0 ||
			strcmp(model, "Leopard-2FE") == 0 ||
			strcmp(model, "NM-16ESW") == 0 ||
			strcmp(model, "WIC-1T") == 0 ||
			strcmp(model, "WIC-2T") == 0) {
		rc = 0;
	}
	free(tmp);
	return rc;
}

// Check if link is valid
int is_link(const char *link, const int length) {
	// TODO
	/*
	char *tmp = strdup(link);
	char *slot = strtok(tmp, ":");		  // Must be numeric
	char *port = strtok(NULL, ":");		  // Must be numeric
	char *type = strtok(NULL, ":");		  // Must be 'tap' or 'unix'
	char *interface = strtok(NULL, ":");	// Must be a valid interface
	char *local = strtok(NULL, ":");		// Must be a file inside an existent dir
	char *remote = strtok(NULL, ":");	   // Must be a file inside an existent dir
	char *final = strtok(NULL, ":");		// Must be NULL (no traling chars)
	int rc = -1;
	*/
	return 0;
}

// Check if is Ethernet link
int is_ethlink(const char *link, const int length) {
	int rc = -1;
	char *tmp = strdup(link);
	char *token = strtok(tmp, ":");
	while (token != NULL) {
		if (strcmp(token, "tap") == 0) {
			// Bound to TAP interface (Ethernet)
			rc = 0;
			break;
		}
		token = strtok(NULL, ":");
	}
	free(token);
	return rc;
}
