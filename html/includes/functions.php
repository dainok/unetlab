<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/functions.php
 *
 * Various functions for UNetLab.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/**
 * Function to check if database is availalble.
 *
 * @return	PDO							PDO object if valid, or False if invalid
 */
function checkDatabase() {
	// Database connection
	try {
		$db = new PDO('sqlite:'.DATABASE);
		$db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		return $db;
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90003]);
		error_log(date('M d H:i:s ').(string) $e);
		return False;
	}
}

/**
 * Function to check if a string is valid as folder_path.
 *
 * @param	string	$s					Parameter
 * @return	int							0 is valid and exists, 1 is valid and does not exists, 2 is invalid
 */
function checkFolder($s) {
	if (preg_match('/^\/[\/A-Za-z0-9_\\s-]*$/', $s) && is_dir($s)) {
		return 0;
	} else if (preg_match('/^\/[\/A-Za-z0-9_\\s-]*$/', $s)) {
		return 1;
	} else {
		return 2;
	}
}

/**
 * Function to check if a string is valid as interface_type.
 *
 * @param	string	$s					Parameter
 * @return	bool						True if valid
 */
function checkInterfcType($s) {
	if (in_array($s, Array('ethernet', 'serial'))) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as lab_filename.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkLabFilename($s) {
	if (preg_match('/^[A-Za-z0-9_\\s-]+\.unl$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as lab_name.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkLabName($s) {
	if (preg_match('/^[A-Za-z0-9_\\s-]+$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as lab_path.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkLabPath($s) {
	if (preg_match('/^\/[\/A-Za-z0-9_\\s-]*$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as network_type.
 *
 * @param	string	$s					Parameter
 * @return	bool						True if valid
 */
function checkNetworkType($s) {
	if (in_array($s, listNetworkTypes())) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_config.
 *
 * @param	string	$s					Parameter
 * @return	bool						True if valid
 */
function checkNodeConfig($s) {
	if (in_array($s, Array('0', '1')) || in_array($s, listNodeConfigTemplates())) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_console.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkNodeConsole($s) {
	if (in_array($s, Array('telnet', 'vnc'))) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_icon.
 *
 * @param	string	$s					Parameter
 * @return	bool						True if valid
 */
function checkNodeIcon($s) {
	if (preg_match('/^[A-Za-z0-9_+\\s-]*\.png$/', $s) && is_file(BASE_DIR.'/html/images/icons/'.$s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_idlepc.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkNodeIdlepc($s) {
	if (preg_match('/^0x[0-9a-f]+$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_image.
 *
 * @param	string	$s					String to check
 * @param	string	$s					Node type
 * @param	string	$s					Node template
 * @return	bool						True if valid
 */
function checkNodeImage($s, $t, $p) {
	if (in_array($s, listNodeImages($t, $p))) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_name.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkNodeName($s) {
	if (preg_match('/^[A-Za-z0-9-_]+$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_type.
 *
 * @param	string	$s					Parameter
 * @return	bool						True if valid
 */
function checkNodeType($s) {
	if (in_array($s, listNodeTypes())) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as object_name.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkTextObjectName($s) {
	return True;
}

/**
 * Function to check if a string is valid as object_type.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkTextObjectType($s) {
	if (preg_match('/^[a-z0-9]+$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as a picture_map.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkPictureMap($s) {
	// TODO
	return True;
}

/**
 * Function to check if a string is valid as a picture_type. Currently only
 * PNG and JPEG images are supported.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkPictureType($s) {
	if (in_array($s, Array('image/png', 'image/jpeg'))) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as a position.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkPosition($s) {
	if (preg_match('/^[0-9]+$/', $s) && $s >= 0) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check user expiration.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	string	$username			Username
 * @return	bool						True if valid
 */
function checkUserExpiration($db, $username) {
	$now = time() + SESSION;
	try {
		$query = 'SELECT COUNT(*) AS rows FROM users WHERE username = :username AND (expiration < 0 OR expiration >= :expiration);';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':expiration', $now, PDO::PARAM_INT);
		$statement -> bindParam(':username', $username, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();
		if ($result['rows'] == 1) {
			return True;
		} else {
			return False;
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90024]);
		error_log(date('M d H:i:s ').(string) $e);
		return False;
	}
}

/**
 * Function to check if a string is valid as UUID.
 *
 * @param	string	$s					String to check
 * @return	bool						True if valid
 */
function checkUuid($s) {
	if (preg_match('/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to configure a POD for a user.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	string	$username			Username
 * @return	int							0 means ok
 */
function configureUserPod($db, $username) {
	// Check if a POD is already been assigned
	try {
		$query = 'SELECT COUNT(*) AS rows FROM pods LEFT JOIN users ON pods.username = users.username WHERE users.username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $username, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();
		if ($result['rows'] > 1) {
			// We expect one or none rows
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90015]);
			return 90015;
		} else if ($result['rows'] == 1) {
			// POD already assigned
			return 0;
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90027]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90027;
	}
			
	try {
		// List assigned PODS
		$query = 'SELECT id, username FROM pods;';	// List also expired lab, because they are not cleared yet
		$statement = $db -> prepare($query);
		$statement -> execute();
		$result = $statement -> fetchAll(PDO::FETCH_KEY_PAIR|PDO::FETCH_GROUP);
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90025]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90025;
	}

	// Find the first available POD
	$pod = 0;
	while (True) {
		if (!isset($result[$pod])) {
			break;
		}
		$pod = $pod + 1;
	}

	if ($pod >= 256) {
		// No free POD available
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90022]);
		return 90022;
	} else {
		// Assign the POD
		try {
			$query = 'INSERT INTO pods (id, username) VALUES(:pod_id, :username);';
			$statement = $db -> prepare($query);
			$statement -> bindParam(':pod_id', $pod, PDO::PARAM_INT);
			$statement -> bindParam(':username', $username, PDO::PARAM_STR);
			$statement -> execute();
		} catch (Exception $e) {
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90023]);
			error_log(date('M d H:i:s ').(string) $e);
			return 90023;
		}
	}
	return 0;
}

/**
 * Function to delete expired sessions.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	string	$username			Username
 * @return  int							0 means ok
 */
function deleteSessions($db) {
	$now = time();
	try {
		// List expired PODS
		$query = 'SELECT id FROM pods WHERE expiration > -1 AND expiration < :expiration;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':expiration', $now, PDO::PARAM_INT);
		$statement -> execute();
		$result = $statement -> fetch();
		// TODO should delete each POD
		// foreach $result... delete $result['tenant_id']
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90020]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90020;
	}

	try {
		// Delete expired PODS from database
		$query = 'DELETE FROM pods WHERE expiration > -1 AND expiration < :expiration;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':expiration', $now, PDO::PARAM_INT);
		$statement -> execute();
		$result = $statement -> fetch();
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90021]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90021;
	}

	return 0;
}

/**
 * Function to get username by cookie
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	string	$cookie				Session cookie
 * @return	bool						True if valid
 */
function getUserByCookie($db, $cookie) {
	$now = time();
	try {
		$query = 'SELECT users.role AS role, users.email AS email, users.name AS name, pods.id AS pod, users.username AS username, users.folder AS folder, pods.lab_id AS lab FROM users LEFT JOIN pods ON users.username = pods.username WHERE cookie = :cookie AND users.session >= :session AND (users.expiration < 0 OR users.expiration >= :user_expiration) AND (pods.expiration < 0 OR pods.expiration > :pod_expiration);';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':cookie', $cookie, PDO::PARAM_STR);
		$statement -> bindParam(':session', $now, PDO::PARAM_INT);
		$statement -> bindParam(':user_expiration', $now, PDO::PARAM_INT);
		$statement -> bindParam(':pod_expiration', $now, PDO::PARAM_INT);
		$statement -> execute();
		$result = $statement -> fetch();
		// TODO should check number of rows == 1, if not database corrupted

		if (isset($result['username'])) {
			return Array(
				'email' => $result['email'],
				'folder' => $result['folder'],
				'lab' => $result['lab'],
				'lang' => 'en',	// TODO: must deal with multiple lang
				'name' => $result['name'],
				'role' => $result['role'],
				'tenant' => $result['pod'],
				'username' => $result['username']
			);
		} else {
			return Array();
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90026]);
		error_log(date('M d H:i:s ').(string) $e);
		return Array();;
	}
}

/**
 * Function to generate a v4 UUID.
 *
 * @return	string						The generated UUID
 */
function genUuid() {
	return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
		// 32 bits for "time_low"
		mt_rand(0, 0xffff), mt_rand(0, 0xffff),

		// 16 bits for "time_mid"
		mt_rand(0, 0xffff),

		// 16 bits for "time_hi_and_version",
		// four most significant bits holds version number 4
		mt_rand(0, 0x0fff) | 0x4000,

		// 16 bits, 8 bits for "clk_seq_hi_res",
		// 8 bits for "clk_seq_low",
		// two most significant bits holds zero and one for variant DCE1.1
		mt_rand(0, 0x3fff) | 0x8000,

		// 48 bits for "node"
		mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
	);
}


/**
 * Function to check if mac address format is valid
 *
 * @return   int (Bool)   
 */

function IsValidMac($mac)
{
  return (preg_match('/([a-fA-F0-9]{2}[:]?){6}/', $mac) == 1);
}
/** 
  * Function to Increment mac address
  *
  * @return string  Next Mac
  */

function incMac($mac,$n)
{
        $nmac=substr("000000000000".dechex(hexdec(str_replace(":", '', $mac))+$n),-12);
        $fmac=trim((preg_replace('/../','$0:',$nmac)),":");
	return $fmac;
}

/**
 * Function to check if UNetLab is running as a VM.
 *
 * @return	bool						True is is a VM
 */
function isVirtual() {
	switch (FORCE_VM) {
		default:
			// Auto or non valid setting
			$cmd = 'sudo /opt/unetlab/wrappers/unl_wrapper -a platform';
			exec($cmd, $o, $rc);
			switch (implode('', $o)) {
				default:
					return False;
				case 'VMware Virtual Platform':
					return True;
				case 'VirtualBox':
					return True;
				case 'KVM':
					// QEMU (KVM)
					return True;
				case 'Bochs':
					// QEMU (emulated)
					return True;
				case 'Virtual Machine':
					// Microsoft VirtualPC
					return True;
				case 'Xen':
					// HVM domU
					return True;
			}
		case 'on':
			return True;
		case 'off':
			return False;
	}
}

/**
 * Function to list all available cloud interfaces (pnet*).
 *
 * @return	Array						The list of pnet interfaces
 */
function listClouds() {
	$results = Array();
	foreach (scandir('/sys/devices/virtual/net') as $interface) {
		if (preg_match('/^pnet[0-9]+$/', $interface)) {
			$results[$interface] = $interface;
		}
	}
	return $results;
}

/**
 * Function to list all roles
 *
 * @return	Array						The list of roles
 */
function listRoles() {
	$results = Array();
	$results['admin'] = 'Administrator';
	$results['editor'] = 'Editor';
	$results['user'] = 'User';
	return $results;
}

/**
 * Function to list all available network types.
 *
 * @return	Array						The list of network types
 */
function listNetworkTypes() {
	$results = Array();
	$results['bridge'] = 'bridge';
	$results['ovs'] = 'ovs';

	// Listing pnet interfaces
	foreach (scandir('/sys/devices/virtual/net') as $interface) {
		if (preg_match('/^pnet[0-9]+$/', $interface)) {
			$results[$interface] = $interface;
		}
	}

	return $results;
}

/**
 * Function to list all available startup-config templates.
 *
 * @return	Array						The list of icons
 */
function listNodeConfigTemplates() {
	$results = Array();
	foreach (scandir(BASE_DIR.'/html/configs') as $filename) {
		if (is_file(BASE_DIR.'/html/configs/'.$filename) && preg_match('/^.+\.php$/', $filename)) {
			$patterns[0] = '/^(.+)\.php$/';  // remove extension
			$replacements[0] = '$1';
			$name = preg_replace($patterns, $replacements, $filename);
			$results[$filename] = $name;
		}
	}
	return $results;
}

/**
 * Function to list all available icons.
 *
 * @return	Array						The list of icons
 */
function listNodeIcons() {
	$results = Array();
	foreach (scandir(BASE_DIR.'/html/images/icons') as $filename) {
		if (is_file(BASE_DIR.'/html/images/icons/'.$filename) && preg_match('/^.+\.png$/', $filename)) {
			$patterns[0] = '/^(.+)\.png$/';  // remove extension
			$replacements[0] = '$1';
			$name = preg_replace($patterns, $replacements, $filename);
			$results[$filename] = $name;
		}
	}
	return $results;
}

/**
 * Function to list all available images.
 *
 * @param   string  $t                  Type of image
 * @param   string  $p                  Template of image
 * @return  Array                       The list of images
 */
function listNodeImages($t, $p) {
	$results = Array();

	switch ($t) {
		default:
			break;
		case 'iol':
			foreach (scandir(BASE_DIR.'/addons/iol/bin') as $name => $filename) {
				if (is_file(BASE_DIR.'/addons/iol/bin/'.$filename) && preg_match('/^.+\.bin$/', $filename)) {
					$results[$filename] = $filename;
				}
			}
			break;
		case 'qemu':
			foreach (scandir(BASE_DIR.'/addons/qemu') as $dir) {
				if (is_dir(BASE_DIR.'/addons/qemu/'.$dir) && preg_match('/^'.$p.'-.+$/', $dir)) {
					$results[$dir] = $dir;
				}
			}
			break;
		case 'dynamips':
			foreach (scandir(BASE_DIR.'/addons/dynamips') as $filename) {
				if (is_file(BASE_DIR.'/addons/dynamips/'.$filename) && preg_match('/^'.$p.'-.+\.image$/', $filename)) {
					$results[$filename] = $filename;
				}
			}
			break;
		case 'docker':
			$cmd = '/usr/bin/docker -H=tcp://127.0.0.1:4243 images | sed \'s/^\([^[:space:]]\+\)[[:space:]]\+\([^[:space:]]\+\).\+/\1:\2/g\'';
			exec($cmd, $o, $rc);
			if (!empty($o) && sizeof($o) > 1) {
				unset($o[0]);	// Removing header
				foreach ($o as $image) {
					$results[$image] = $image;
				}
			}
			break;
	}
	return $results;
}

/**
 * Function to list all available node types.
 *
 * @return  Array                       The list of node types
 */
function listNodeTypes() {
	return Array('iol', 'dynamips', 'docker', 'qemu' , 'vpcs');
}

/**
 * Function to scale an image maintaining the aspect ratio.
 *
 * @param   string  $image              The image
 * @param   int     $width              New width
 * @param   int     $height             New height
 * @return  string                      The resized image
 */
function resizeImage($image, $width, $height) {
	$img = new Imagick();
	$img -> readimageblob($image);
	$img -> setImageFormat('png');
	$original_width = $img -> getImageWidth();
	$original_height = $img -> getImageHeight();

	if ($width > 0 && $height == 0) {
		// Use width to scale
		if ($width < $original_width) {
			$new_width = $width;
			$new_height = $original_height / $original_width * $width;
			$new_height > 0 ? $new_height : $new_height = 1; // Must be 1 at least
			$img -> resizeImage($new_width, $new_height, Imagick::FILTER_LANCZOS, 1);
			return $img -> getImageBlob();
		}
	} else if ($width == 0 && $height > 0) {
		// Use height to scale
		if ($height < $original_height) {
			$new_width = $original_width / $original_height * $height;
			$new_width > 0 ? $new_width : $new_width = 1; // Must be 1 at least
			$new_height = $height;
			$img -> resizeImage($new_width, $new_height, Imagick::FILTER_LANCZOS, 1);
			return $img -> getImageBlob();
		}
	} else if ($width > 0 && $height > 0) {
		// No need to keep aspect ratio
		$img -> resizeImage($width, $height, Imagick::FILTER_LANCZOS, 1);
		return $img -> getImageBlob();
	} else {
		// No need to resize, return the original image
		return $image;
	}
}

/**
 * Function to lock a file.
 *
 * @param   string  $file               File to lock
 * @return  bool                        True if locked
 */
function lockFile($file) {
	$timeout = TIMEOUT * 1000000;
	$locked = False;

	while ($timeout > 0) {
		if (file_exists($file.'.lock')) {
			// File is locked, wait for a random interval
			$wait = 1000 * rand(0, 500);
			$timeout = $timeout - $wait;
			usleep($wait);
		} else {
			$locked = True;
			touch($file.'.lock');
			break;
		}
	}
	return $locked;
}

/**
 * Function to unlock a file.
 *
 * @param   string  $file               File to lock
 * @return  bool                        True if unlocked
 */
function unlockFile($file) {
	return unlink($file.'.lock');
}

/**
 * Function to update database.
 *
 * @param   PDO     $db                 PDO object for database connection
 * @return  bool                        True if updated
 */
function updateDatabase($db) {
	// Users table
	try {
		$query = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'users';";
		$statement = $db -> prepare($query);
		$statement -> execute();
		$result = $statement -> fetch();
		if ($result['name'] != 'users') {
			// User table is missing
			$db -> beginTransaction();
			$query = 'CREATE TABLE users (username TEXT PRIMARY KEY, cookie TEXT, email TEXT, expiration INTEGER DEFAULT -1, name TEXT, password TEXT, session INT);';
			$statement = $db -> prepare($query);
			$statement -> execute();

			// Adding admin user
			$query = "INSERT INTO users (email, name, username, password) VALUES('root@localhost', 'UNetLab Administrator', 'admin', '".hash('sha256', 'unl')."');";
			$statement = $db -> prepare($query);
			$statement -> execute();
			$db -> commit();

			error_log(date('M d H:i:s ').'INFO: '.$GLOBALS['messages'][90004]);
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90005]);
		error_log(date('M d H:i:s ').(string) $e);
		return False;
	}

	/*
	// Permissions table
	try {
		$query = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'permissions';";
		$statement = $db -> prepare($query);
		$statement -> execute();
		$result = $statement -> fetch();
		if ($result['name'] != 'permissions') {
			// User table is missing
			$db -> beginTransaction();
			$query = 'CREATE TABLE permissions (lab_id TEXT, role TEXT, username TEXT, PRIMARY KEY (lab_id, role, username));';
			$statement = $db -> prepare($query);
			$statement -> execute();

			// Adding admin user
			$query = "INSERT INTO permissions (lab_id, role, username) SELECT '*', 'admin', 'admin';";
			$statement = $db -> prepare($query);
			$statement -> execute();
			$db -> commit();

			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90007]);
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90008]);
		error_log(date('M d H:i:s ').(string) $e);
		return False;
	}
	 */

	// Pods table
	try {
		$query = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'pods';";
		$statement = $db -> prepare($query);
		$statement -> execute();
		$result = $statement -> fetch();
		if ($result['name'] != 'pods') {
			// User table is missing
			$db -> beginTransaction();
			$query = 'CREATE TABLE pods (id INTEGER PRIMARY KEY, expiration INTEGER DEFAULT -1, username TEXT, lab_id TEXT);';
			$statement = $db -> prepare($query);
			$statement -> execute();
			$query = 'CREATE INDEX username_pods ON pods (username);';
			$statement = $db -> prepare($query);
			$statement -> execute();

			// Adding admin user
			$query = "INSERT INTO pods (id, expiration, username) SELECT 0, -1, 'admin';";
			$statement = $db -> prepare($query);
			$statement -> execute();
			$db -> commit();

			error_log(date('M d H:i:s ').'INFO: '.$GLOBALS['messages'][90009]);
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90010]);
		error_log(date('M d H:i:s ').(string) $e);
		return False;
	}
	
	// Update old database
	try {
		$query = 'PRAGMA user_version;';
		$version = $db -> query($query) -> fetchColumn();
		switch ($version) {
			case 0:
				// From version 0 to version 1, need to add ip and role columns to users table
				$db -> beginTransaction();
				$query = 'ALTER TABLE users ADD COLUMN ip TEXT;';
				$statement = $db -> prepare($query);
				$statement -> execute();
				$query = 'ALTER TABLE users ADD COLUMN role TEXT;';
				$statement = $db -> prepare($query);
				$statement -> execute();
				$db -> commit();
				$query = 'UPDATE users SET role = "admin";';
				$statement = $db -> prepare($query);
				$statement -> execute();

			case 1:
				// From version 1 to version 2, need to add folder column to users table
				$db -> beginTransaction();
				$query = 'ALTER TABLE users ADD COLUMN folder TEXT;';
				$statement = $db -> prepare($query);
				$statement -> execute();
				$db -> commit();

				// Latest database version
				error_log(date('M d H:i:s ').'INFO: '.$GLOBALS['messages'][90031]);
				$query = 'PRAGMA user_version = 2;';
				$version = $db -> query($query);
		}
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90030]);
		error_log(date('M d H:i:s ').(string) $e);
		return False;
	}

	return $db;
}

/**
 * Function to update user session (expiration).
 *
 * @param   PDO     $db                 PDO object for database connection
 * @param   string  $username           Username
 * @param   string  $cookie             Session cookie
 * @return  0                           0 means ok
 */
function updateUserCookie($db, $username, $cookie) {
	try {
		$ip = $_SERVER['REMOTE_ADDR'];
		$now = time() + SESSION;
		$query = 'UPDATE users SET cookie = :cookie, session = :session, ip = :ip WHERE username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':cookie', $cookie, PDO::PARAM_STR);
		$statement -> bindParam(':session', $now, PDO::PARAM_INT);
		$statement -> bindParam(':username', $username, PDO::PARAM_STR);
		$statement -> bindParam(':ip', $ip, PDO::PARAM_STR);
		$statement -> execute();
		return 0;
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90017]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90017;
	}
}

/**
 * Function to update user folder.
 *
 * @param   PDO     $db                 PDO object for database connection
 * @param   string  $cookie             Session cookie
 * @param   string  $folder             Last seen folder
 * @return  0                           0 means ok
 */
function updateUserFolder($db, $cookie, $folder) {
	try {
		$query = 'UPDATE users SET folder = :folder WHERE cookie = :cookie;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':cookie', $cookie, PDO::PARAM_STR);
		$statement -> bindParam(':folder', $folder, PDO::PARAM_STR);
		$statement -> execute();
		return 0;
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90033]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90033;
	}
}

/**
 * Function to update POD lab.
 *
 * @param   PDO     $db                 PDO object for database connection
 * @param   string  $cookie             Session cookie
 * @param   string  $lab				Running lab
 * @return  0                           0 means ok
 */
function updatePodLab($db, $tenant, $lab_file) {
	try {
		$query = 'UPDATE pods SET lab_id = :lab_id WHERE id = :id;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':id', $tenant, PDO::PARAM_STR);
		$statement -> bindParam(':lab_id', $lab_file, PDO::PARAM_STR);
		$statement -> execute();
		return 0;
	} catch (Exception $e) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][90034]);
		error_log(date('M d H:i:s ').(string) $e);
		return 90034;
	}
}
?>
