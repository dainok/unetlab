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

define('BASE_DIR', '/opt/unetlab');

// Include custom configuration
if (file_exists('includes/config.php')) {
	require_once('includes/config.php');
}

// Preview Code UIlegacy
$UIlegacy = 1 ;

// new format yml setting import
/*
 *  Load  templates
 *  This will overwrite previous tezmplates
 */
if (file_exists('/opt/unetlab/html/includes/custom_templates.yml') &&  !isset($custom_template)) {
	$custom_templates_yml=yaml_parse_file('/opt/unetlab/html/includes/custom_templates.yml');
	$custom_templates = Array();
	foreach ( $custom_templates_yml['custom_templates']  as $template ) {
			$custom_templates[$template['name']] = $template['listname'];
	}
}


/*
 *  Load  settings
 *  This will NOT overwrite previous ettings
 */
if (file_exists('/opt/unetlab/html/includes/config.yml')) {
	$config_yml = yaml_parse_file('/opt/unetlab/html/includes/config.yml');
	if (!defined('RADIUS_SERVER_IP')  && isset($config_yml['radius'][0]['server']) )  define('RADIUS_SERVER_IP', $config_yml['radius'][0]['server']);
	if (!defined('RADIUS_SERVER_PORT') && isset($config_yml['radius'][0]['port'])  )  define('RADIUS_SERVER_PORT', $config_yml['radius'][0]['port']);
	if (!defined('RADIUS_SERVER_SECRET') && isset($config_yml['radius'][0]['secret'])  )  define('RADIUS_SERVER_SECRET', $config_yml['radius'][0]['secret']);
	if (!defined('RADIUS_SERVER_IP_2') && isset($config_yml['radius'][1]['server']) ) define('RADIUS_SERVER_IP_2', $config_yml['radius'][1]['server']);
	if (!defined('RADIUS_SERVER_PORT_2') && isset($config_yml['radius'][1]['port']) ) define('RADIUS_SERVER_PORT_2', $config_yml['radius'][1]['port']);
	if (!defined('RADIUS_SERVER_SECRET_2') && isset($config_yml['radius'][1]['secret']) ) define('RADIUS_SERVER_SECRET_2', $config_yml['radius'][1]['secret']);
	if (!defined('PROXY_SERVER') && isset($config_yml['proxy'][0]['server']) )  define('PROXY_SERVER',$config_yml['proxy'][0]['server']);
	if (!defined('PROXY_PORT') && isset($config_yml['proxy'][0]['port']) ) define('PROXY_PORT',$config_yml['proxy'][0]['port']);
	if (!defined('MINDISK') && isset($config_yml['mindisk']) ) define('MINDISK',$config_yml['mindisk']);
	if (!defined('TEMPLATE_DISABLED') && isset($config_yml['template_disabled']) ) DEFINE('TEMPLATE_DISABLED', '.'.$config_yml['template_disabled']) ;
}

$kvm_family = file_get_contents("/opt/unetlab/platform");
$hypervisor = file_get_contents("/opt/unetlab/hypervisor");
if ( $hypervisor == "none\n" ) {
	$hypervisor = "bare" ;
} else {
	$hypervisor = "vm" ;
}
$platform = "intel" ;
if ( $kvm_family == "svm" )  $platform = "amd" ;

if (!defined('DATABASE')) define('DATABASE', '/opt/unetlab/data/database.sdb');
if (!defined('FORCE_VM')) define('FORCE_VM', 'auto');
if (!defined('MODE')) define('MODE', 'multi-user');
if (!defined('SESSION')) define('SESSION', '3600');
if (!defined('THEME')) define('THEME', 'default');
if (!defined('TIMEOUT')) define('TIMEOUT', 25);
if (!defined('TIMEZONE')) define('TIMEZONE', 'Europe/Rome');
if (!defined('TEMPLATE_DISABLED')) define('TEMPLATE_DISABLED', '.missing');
if (!defined('TPL_DIR')) define ('TPL_DIR','templates/'.$platform);
if (!defined('HYPERVISOR')) define ('HYPERVISOR', $hypervisor );

// Create template array
$node_templates = Array();
$node_config = Array();
$node_prep = Array();
$node_cstart = Array();
$node_init = Array();
foreach ( scandir(BASE_DIR.'/html/'.TPL_DIR) as $element ) {
	if (is_file(BASE_DIR.'/html/'.TPL_DIR.'/'.$element) && preg_match('/^.+\.yml$/', $element)) {
		$cur_name = preg_replace('/.yml/','',$element ) ;
		$cur_templ = yaml_parse_file(BASE_DIR.'/html/'.TPL_DIR.'/'.$element);
		if ( isset($cur_templ['description']) ) {
				$node_templates[$cur_name] =  $cur_templ['description'] ;
		}
		if ( isset($cur_templ['config_script']) ) {
				$node_config[$cur_name] =  $cur_templ['config_script'] ;
		}
		if ( isset($cur_templ['prep']) ) {
				$node_prep[$cur_name] =  $cur_templ['prep'] ;
		}
		if ( isset($cur_templ['cstart']) ) {
				$node_cstart[$cur_name] =  $cur_templ['cstart'] ;
		}
		if ( isset($cur_templ['init']) ) {
				$node_init[$cur_name] =  $cur_templ['init'] ;
		}
	}
}

$qemudir = scandir("/opt/unetlab/addons/qemu/");
$ioldir=scandir("/opt/unetlab/addons/iol/bin/");
$dyndir=scandir("/opt/unetlab/addons/dynamips/");
//MOD by @cianfa72
$dockerdir=scandir("/opt/unetlab/addons/docker/");

if (isset($custom_templates)) {
	$node_templates = array_merge ( $node_templates , $custom_templates );
}
natcasesort(  $node_templates ) ;

foreach ( $node_templates as $templ => $desc ) {
	$found = 0 ;
	if ( $templ == "iol" ) {
		foreach ( $ioldir as $dir ) {
			if ( preg_match ( "/\.bin/",$dir )  ==  1 ) {
				$found = 1 ;
			}
		}
	}
	if ( $templ == "c1710" || $templ == "c3725" || $templ == "c7200" ) {
		foreach ( $dyndir as $dir ) {
			if ( preg_match ( "/".$templ."/",$dir )  ==  1 ) {
				$found = 1 ;
			}
		}
	}
	if ( $templ == "vpcs" ) {
		$found = 1 ;
	}
	
	foreach ( $qemudir as $dir ) {
		if ( preg_match ( "/".$templ."-.*/",$dir )  ==  1 ) {
			$found = 1 ;
		}
	}
	
	//MOD by @cianfa72
	foreach ( $dockerdir as $dir ) {
		if ( preg_match ( "/".$templ."-.*/",$dir )  ==  1 ) {
			$found = 1 ;
		}
	}
	
	if ( $found == 0 ) {
		//$node_templates[$templ] = $desc.'.missing'  ;
		$node_templates[$templ] = $desc.TEMPLATE_DISABLED  ;
	}
}

// Define parameters
$eve_ver = file_get_contents("/opt/unetlab/html/themes/adminLTE/VERSION");
define('VERSION', $eve_ver);
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
if (php_sapi_name() ==	'cli') {
	// CLI User
	require_once(BASE_DIR.'/html/includes/cli.php');
} else {
	// Web User
	//session_start();
}
?>