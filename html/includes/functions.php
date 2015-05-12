<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/functions.php
 *
 * Various functions for UNetLab.
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
 * @version 20150511
 */

/**
 * Function to check if a string is valid as folder_path.
 *
 * @param   string  $s                  Parameter
 * @return  int                         0 is valid and exists, 1 is valid and does not exists, 2 is invalid
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
 * @param   string  $s                  Parameter
 * @return  bool                        True if valid
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
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
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
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
 */
function checkLabName($s) {
	if (preg_match('/[A-Za-z0-9_\\s-]+$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as lab_path.
 *
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
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
 * @param   string  $s                  Parameter
 * @return  bool                        True if valid
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
 * @param   string  $s                  Parameter
 * @return  bool                        True if valid
 */
function checkNodeConfig($s) {
	// TODO
	return True;
}

/**
 * Function to check if a string is valid as node_console.
 *
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
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
 * @param   string  $s                  Parameter
 * @return  bool                        True if valid
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
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
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
 * @param   string  $s                  String to check
 * @param   string  $s                  Node type
 * @param   string  $s                  Node template
 * @return  bool                        True if valid
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
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
 */
function checkNodeName($s) {
	if (preg_match('/[A-Za-z0-9-]+$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as node_type.
 *
 * @param   string  $s                  Parameter
 * @return  bool                        True if valid
 */
function checkNodeType($s) {
	if (in_array($s, listNodeTypes())) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as a picture_map.
 *
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
 */
function checkPictureMap($s) {
	// TODO
	return True;
}

/**
 * Function to check if a string is valid as a picture_type. Currently only
 * PNG and JPEG images are supported.
 *
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
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
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
 */
function checkPosition($s) {
	if (preg_match('/^[0-9]+%$/', $s) && substr($s, 0, -1) >= 0 && substr($s, 0, -1) <= 100) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a string is valid as UUID.
 *
 * @param   string  $s                  String to check
 * @return  bool                        True if valid
 */
function checkUuid($s) {
	if (preg_match('/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/', $s)) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to generate a v4 UUID.
 *
 * @return  string                      The generated UUID
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
 * Function to check if UNetLab is running as a VM.
 *
 * @return  bool                        True is is a VM
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
 * @return  Array                       The list of pnet interfaces
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
 * Function to list all available network types.
 *
 * @return  Array                       The list of network types
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
 * Function to list all available icons.
 *
 * @return  Array                       The list of icons
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
	}
	return $results;
}

/**
 * Function to list all available node types.
 *
 * @return  Array                       The list of node types
 */
function listNodeTypes() {

	return Array('iol', 'dynamips', 'qemu');
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
?>
