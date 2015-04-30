<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_status.php
 *
 * Various system status commands for REST APIs.
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
 * @version 20150428
 */

/*
 * Function to get CPU usage percentage.
 *
 * @return  int                         CPU usage (percentage) or -1 if not valid
 */
function apiGetCPUUsage() {
	// Checking CPU usage
	$cmd = 'top -b -n1 -p1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return 100 - round(preg_replace('/^.+, ([0-9\.]+) id,.+/', '$1', $o[2]));
	} else {
		return -1;
	}
}

/*
 * Function to get disk usage percentage.
 *
 * @return  int                         Disk usage (percentage) or -1 if not valid
 */
function apiGetDiskUsage() {
	// Checking disk usage
	$cmd = 'df -h /';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return preg_replace('/^.+ ([0-9]+)% .+/', '$1', $o[1]);
	} else {
		return -1;
	}
}

/*
 * Function to get disk usage percentage.
 *
 * @return  Array                       RAM usage (percentage) as cache and data or -1 if not valid
 */
function apiGetMemUsage() {
	// Checking RAM usage
	$cmd = 'free';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		$total = preg_replace('/^Mem:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$1', $o[1]);
		$used = preg_replace('/^Mem:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$2', $o[1]);
		$cached = preg_replace('/^Mem:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$6', $o[1]);
		return Array(round($cached / $total * 100), round(($used - $cached) / $total * 100));
	} else {
		return Array(-1, -1);
	}
}

/*
 * Function to running wrapper for IOL, Dynamips and QEMU.
 *
 * @return  Array                       Running IOL/Dynamips/QEMU wrappers or -1 if not valid
 */
function apiGetRunningWrappers() {
	// Checking running wrappers
	$cmd = 'pgrep iol_wrapper';
	exec($cmd, $o_iol, $rc);
	$cmd = 'pgrep dynamips_wrapper';
	exec($cmd, $o_dynamips, $rc);
	$cmd = 'pgrep qemu_wrapper';
	exec($cmd, $o_qemu, $rc);
	return Array((int) current($o_iol), (int) current($o_dynamips), (int) current($o_qemu));
}

/*
 * Function to get swap usage percentage.
 *
 * @return  int                         Swap usage (percentage) or -1 if not valid
 */
function apiGetSwapUsage() {
	// Checking swap usage
	$cmd = 'free';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		$total = preg_replace('/^Swap:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$1', $o[3]);
		$used = preg_replace('/^Swap:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$3', $o[3]);
		return 100 - round($used / $total * 100);
	} else {
		return -1;
	}
}
?>
