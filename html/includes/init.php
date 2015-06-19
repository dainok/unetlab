<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/init.php
 *
 * Initialization file for UNetLab.
 *
 * This file include all needed files and variables to run UNetLab. Don't
 * edit this file, it will be overwritten when updating. Create a new file
 * named 'config.php' under /opt/unetlab/html/includes and set some of all
 * the following parameters:
 *
 * define('DATABASE', '/opt/unetlab/data/database.sdb');
 * define('FORCE_VM', 'auto');
 * define('SESSION', '3600');
 * define('THEME', 'default');
 * define('TIMEZONE', 'Europe/Rome');
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
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with UNetLab. If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2015 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20150525
 */

// Include custom configuration
if (file_exists('includes/config.php')) {
	require_once('includes/config.php');
}

if (!defined('DATABASE')) define('DATABASE', '/opt/unetlab/data/database.sdb');
if (!defined('FORCE_VM')) define('FORCE_VM', 'auto');
if (!defined('MODE')) define('MODE', 'multi-user');
if (!defined('SESSION')) define('SESSION', '3600');
if (!defined('THEME')) define('THEME', 'default');
if (!defined('TIMEZONE')) define('TIMEZONE', 'Europe/Rome');

if (!isset($node_templates)) {
	$node_templates = Array(
		'a10'			=>	'A10 vThunder',
		'clearpass'		=>	'Aruba ClearPass',
		'timos'			=>	'Alcatel 7750 SR',
		'veos'			=>	'Arista vEOS',
		'brocadevadx' 	=>	'Brocade vADX',
		'cpsg'			=>	'CheckPoint Security Gateway VE',
		'asa'			=>	'Cisco ASA',
		'asav'			=>	'Cisco ASAv',
		'csr1000v'		=>	'Cisco CSR 1000V',
		'cips'			=>	'Cisco IPS',
		'c1710'			=>	'Cisco IOS 1710 (Dynamips)',
		'c3725'			=>	'Cisco IOS 3725 (Dynamips)',
		'c7200'			=>	'Cisco IOS 7206VXR (Dynamips)',
		'iol'			=>	'Cisco IOL',
		'titanium'		=>	'Cisco NX-OSv (Titanium)',
		'vios'			=>	'Cisco vIOS',
		'viosl2'		=>	'Cisco vIOS L2',
		'vwlc'			=>	'Cisco vWLC',
		//'vwaas'		=>	'Cisco vWAAS',
		'coeus'			=>	'Cisco Web Security Appliance',
		'xrv'			=>	'Cisco XRv',
		'nsvpx'			=>	'Citrix Netscaler',
		'extremexos'	=>	'ExtremeXOS',
		'bigip'			=>	'F5 BIG-IP LTM VE',
		'fortinet'		=>	'Fortinet FortiGate',
		'hpvsr'			=>	'HP VSR1000',
		'olive'			=>	'Juniper Olive',
		'vmx'			=>	'Juniper vMX',
		'vsrx'			=>	'Juniper vSRX',
		'paloalto'		=>	'Palo Alto VM-100 Firewall',
		'vyos'			=>	'VyOS',
		'esxi'			=>	'VMware ESXi',
		'win'			=>	'Windows'
	);
}

// Define parameters
define('VERSION', 'development');
define('BASE_DIR', '/opt/unetlab');
define('BASE_LAB', BASE_DIR.'/labs');
define('BASE_TMP', BASE_DIR.'/tmp');
define('BASE_THEME', '/themes/'.THEME);

// Setting timezone
date_default_timezone_set(TIMEZONE);

// Include classes and functions
require_once(BASE_DIR.'/html/includes/__interfc.php');
require_once(BASE_DIR.'/html/includes/__lab.php');
require_once(BASE_DIR.'/html/includes/__network.php');
require_once(BASE_DIR.'/html/includes/__node.php');
require_once(BASE_DIR.'/html/includes/__picture.php');
require_once(BASE_DIR.'/html/includes/functions.php');
require_once(BASE_DIR.'/html/includes/messages_en.php');

// Include CLI specific functions
if (php_sapi_name() === 'cli') {
	// CLI User
	require_once(BASE_DIR.'/html/includes/cli.php');
} else {
	// Web User
	//session_start();
}
?>
