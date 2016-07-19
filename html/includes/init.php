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
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
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
if (!defined('TIMEOUT')) define('TIMEOUT', 25);
if (!defined('TIMEZONE')) define('TIMEZONE', 'Europe/Rome');

if (!isset($node_config)) {
	$node_config = Array(
		'iol'			=>	'embedded',
		'c1710'			=>	'embedded',
		'c3725'			=>	'embedded',
		'c7200'			=>	'embedded',
		'vpcs'			=>	'embedded',
		'asa'			=>	'config_asa.py',
		'asav'			=>	'config_asav.py',
		'csr1000v'		=>	'config_csr1000v.py',
		'docker'		=>	'config_docker.py',
		'titanium'		=>	'config_titanium.py',
		'veos'			=>	'config_veos.py',
		'viosl2'		=>	'config_viosl2.py',
		'vios'			=>	'config_vios.py',
		'vsrx'			=>	'config_vsrx.py',
		'vsrxng'		=>	'config_vsrxng.py',
		'vmx'			=>	'config_vmx.py',
		'xrv'			=>	'config_xrv.py',
		//'xrv9k'		=>	'config_xrv9k.py',
		'pfsense'		=>	'config_pfsense.py'
	);
}

if (!isset($node_templates)) {
	$node_templates = Array(
		'a10'			=>	'A10 vThunder',
		'clearpass'		=>	'Aruba ClearPass',
		'timos'			=>	'Alcatel 7750 SR',
		'veos'			=>	'Arista vEOS',
		'brocadevadx'		=>	'Brocade vADX',
		'cpsg'			=>	'CheckPoint Security Gateway VE',
		'docker'		=>	'Docker.io',
		'acs'			=>	'Cisco ACS',
		'asa'			=>	'Cisco ASA',
		'asav'			=>	'Cisco ASAv',
		'cda'			=>	'Cisco Context Directory Agent',
		'csr1000v'		=>	'Cisco CSR 1000V',
		'cips'			=>	'Cisco IPS',
		'ise'			=>	'Cisco ISE',
		'c1710'			=>	'Cisco IOS 1710 (Dynamips)',
		'c3725'			=>	'Cisco IOS 3725 (Dynamips)',
		'c7200'			=>	'Cisco IOS 7206VXR (Dynamips)',
		'iol'			=>	'Cisco IOL',
		'titanium'		=>	'Cisco NX-OSv (Titanium)',
		'firepower'		=>	'Cisco FirePower',
		'ucspe'			=>	'Cisco UCS-PE',
		'vios'			=>	'Cisco vIOS',
		'viosl2'		=>	'Cisco vIOS L2',
		'vnam'			=>	'Cisco vNAM',
		'vwlc'			=>	'Cisco vWLC',
		'vwaas'			=>	'Cisco vWAAS',
		'phoebe'		=>	'Cisco Email Security Appliance (ESA)',
		'coeus'			=>	'Cisco Web Security Appliance (WSA)',
		'xrv'			=>	'Cisco XRv',
		'xrv9k'	                =>      'Cisco XRv 9000',
		'nsvpx'			=>	'Citrix Netscaler',
		'sonicwall'            	=>      'Dell SonicWall',
		'cumulus'		=>	'Cumulus VX',
		'extremexos'		=>	'ExtremeXOS',
		'bigip'			=>	'F5 BIG-IP LTM VE',
		'fortinet'		=>	'Fortinet FortiGate',
		//'radware'		=>	'Radware Alteon',
		'hpvsr'			=>	'HP VSR1000',
		'olive'			=>	'Juniper Olive',
		'vmx'			=>	'Juniper vMX',
		'vsrx'			=>	'Juniper vSRX',
		'vsrxng'		=>	'Juniper vSRX NextGen',
		'linux'			=>	'Linux',
		'mikrotik'		=>	'MikroTik RouterOS',
		'ostinato'		=>	'Ostinato',
		'paloalto'		=>	'Palo Alto VM-100 Firewall',
		'pfsense'		=>	'pfSense Firewall',
		//'riverbed'		=>	'Riverbed',
		'sterra'		=>	'S-Terra',
		'vyos'			=>	'VyOS',
		//'esxi'		=>	'VMware ESXi',
		'win'			=>	'Windows',
		'vpcs'			=>	'Virtual PC (VPCS)'
	);
}

// Define parameters
define('VERSION', '1.0.0-11-git');
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
require_once(BASE_DIR.'/html/includes/__textobject.php');
require_once(BASE_DIR.'/html/includes/__picture.php');
require_once(BASE_DIR.'/html/includes/functions.php');
require_once(BASE_DIR.'/html/includes/messages_en.php');
require_once(BASE_DIR.'/html/includes/Parsedown.php');
if (defined('LOCALE') && is_file(BASE_DIR.'/html/includes/messages_'.LOCALE.'.php')) {
	// Load a custom language
	require_once(BASE_DIR.'/html/includes/messages_'.LOCALE.'.php');
}

// Include CLI specific functions
if (php_sapi_name() === 'cli') {
	// CLI User
	require_once(BASE_DIR.'/html/includes/cli.php');
} else {
	// Web User
	//session_start();
}
?>
