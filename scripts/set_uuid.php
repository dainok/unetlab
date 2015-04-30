#!/usr/bin/php
<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * scripts/set_uuid.php
 *
 * Scripts to create lab UUID and rename tmp folder for UNetLab.
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
 * @version 20150423
 */


if (php_sapi_name() !== 'cli') {
	// Must be executed from CLI
	exit(1);
}

require_once('/opt/unetlab/html/includes/init.php');

if (!isset($argv[1])) {
	// File does not exists or not set
	error_log('ERROR: Must need a lab file as argument.');
	exit(1);
}

if (!is_file($argv[1])) {
	// File does not exists
	error_log('ERROR: File does not exist.');
	exit(2);
}

try {
	$lab = new Lab($argv[1], 0);
	if (is_dir(BASE_TMP.'/0/'.$lab -> getId()) && is_dir(BASE_TMP.'/0/'.$lab -> getName())) {
		// Source dir and destinaion dir both exists
		error_log('ERROR: Destination folder already exists.');
		error_log('Cannot migrate "'.$argv[1].'", manually delete directory and loose data to migrate the old configs:');
		error_log('rm -rf "'.BASE_TMP.'/0/'.$lab -> getId().'"');
		error_log($argv[0].' '.$argv[1]);
		error_log('Or remove the old directory if not needed anymore:');
		error_log('rm -rf "'.BASE_TMP.'/0/'.$lab -> getName().'"');
		exit(3);
	} else if (!is_dir(BASE_TMP.'/0/'.$lab -> getId()) && is_dir(BASE_TMP.'/0/'.$lab -> getName())) {
		if (rename(BASE_TMP.'/0/'.$lab -> getName(), BASE_TMP.'/0/'.$lab -> getId())) {
			// Mark as configured all nodes
			$cmd = 'find /opt/unetlab/tmp/0/'.$lab -> getId().'/[0-9]* -type d -exec touch {}/.configured \;';
			exec($cmd, $o, $rc);
		} else {
			// Old dir exists, new one does not, and rename is failed
			error_log('ERROR: File is not a valid lab.');
			exit(4);
		}
	}

	exit(0);
} catch(Exception $e) {
	// Lab file is invalid
	error_log('ERROR: File is not a valid lab.');
	exit(5);
}
?>
