<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_status.php
 *
 * Various system status commands for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/*
 * Function to get CPU usage percentage.
 *
 * @return  int                         CPU usage (percentage) or -1 if not valid
 */
function apiGetCPUUsage() {
	// Checking CPU usage
	$cmd = 'top -b -n2 -p1 -d1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return 100 - (int) round(preg_replace('/^.+ni[, ]+([0-9\.]+) id,.+/', '$1', $o[11]));
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
		return (int) preg_replace('/^.+ ([0-9]+)% .+/', '$1', $o[1]);
	} else {
		return -1;
	}
}

/*
 * Function to get mem usage percentage.
 *
 * @return  Array                       RAM usage (percentage) as cache and data or -1 if not valid
 */
function apiGetMemUsage() {
	// Checking RAM usage
	$cmd = 'free';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		$total = (int) preg_replace('/^Mem:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$1', $o[1]);
		$used = (int) preg_replace('/^Mem:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$2', $o[1]);
		$cached = (int) preg_replace('/^Mem:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$6', $o[1]);
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
	$cmd = 'pgrep -f -c -P 1 iol_wrapper';
	exec($cmd, $o_iol, $rc);
	$cmd = 'pgrep -f -c -P 1 dynamips_wrapper';
	exec($cmd, $o_dynamips, $rc);
	$cmd = 'pgrep -f -c -P 1 qemu_wrapper';
	exec($cmd, $o_qemu, $rc);
	$cmd= 'docker -H=tcp://127.0.0.1:4243 ps -q | wc -l';
	exec($cmd, $o_docker, $rc);
	$cmd = 'pgrep -f -c -P 1 vpcs';
	exec($cmd, $o_vpcs, $rc);
	return Array((int) current($o_iol), (int) current($o_dynamips), (int) current($o_qemu), (int) current($o_docker), (int) current($o_vpcs));
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
		$total = (int) preg_replace('/^Swap:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$1', $o[3]);
		$used = (int) preg_replace('/^Swap:\ +([0-9\.]+)\ +([0-9\.]+)\ +([0-9\.]+)$/', '$3', $o[3]);
		return 100 - round($used / $total * 100);
	} else {
		return -1;
	}
}
?>
