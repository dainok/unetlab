<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_folders.php
 *
 * Folders related functions for REST APIs.
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
 * Function to add a folder to a path.
 *
 * @param   string     $name            Folder name
 * @param   string     $path            Path
 * @return  Array                       Return code (JSend data)
 */
function apiAddFolder($name, $path) {
	$rc = checkFolder(BASE_LAB.$path);
	if ($rc === 2) {
		// Folder is not valid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60009];
		return $output;
	} else if ($rc === 1) {
		// Folder does not exist
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60008];
		return $output;
	}

	if ($path == '/') {
		// Avoid double '/'
		$path = '';
	}

	// Check if exists
	if (is_dir(BASE_LAB.$path.'/'.$name)) {
		// Folder already exists
		$output['code'] = 304;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60013];
	} else if (mkdir(BASE_LAB.$path.'/'.$name)) {
		// Adding the folder
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60014];
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60015];
	}

	return $output;
}

/**
 * Function to delete a folder.
 *
 * @param   string     $path            Path
 * @return  Array                       Return code (JSend data)
 */
function apiDeleteFolder($path) {
	$rc = checkFolder(BASE_LAB.$path);
	if ($rc === 2) {
		// Folder is not valid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60009];
		return $output;
	} else if ($rc === 1) {
		// Folder does not exist
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60008];
		return $output;
	}

	if ($path == '/') {
		// Cannot delete '/'
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60010];
		return $output;
	}

	// Deleting all tmp files for lab inside the folder
	$cmd = 'find '.BASE_LAB.$path.' -name "*.unl" -exec sudo /opt/unetlab/wrappers/unl_wrapper -a delete -F "{}" -T 0 \;';  // Tenant not required for delete operation
	exec($cmd, $o, $rc);

	// Deleting the folder
	$cmd = 'rm -rf "'.BASE_LAB.$path.'" 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = 'Folder deleted';
		$output['message'] = $GLOBALS['messages'][60012];
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = 'Cannot delete folder';
		$output['message'] = $GLOBALS['messages'][60011];
	}
	return $output;
}

/**
 * Function to get all folders from a path.
 *
 * @param   string     $path            Path
 * @return  Array                       List of folders (JSend data)
 */
function apiGetFolders($path) {
	$rc = checkFolder(BASE_LAB.$path);
	if ($rc === 2) {
		// Folder is not valid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60009];
		return $output;
	} else if ($rc === 1) {
		// Folder does not exist
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60008];
		return $output;
	}

	// Listing content
	$folders = Array();
	$labs = Array();

	if ($path != '/') {
		// Adding '..' folder
		$folders[] = Array(
			'name' => '..',
			'path' => dirname($path)
		);
	}

	// Scanning directory
	foreach (scandir(BASE_LAB.$path) as $element) {
		if (!in_array($element, array('.', '..'))) {
			if (is_dir(BASE_LAB.$path.'/'.$element)) {
				if ($path == '/') {
					$folders[] = Array(
						'name' => $element,
						'path' => '/'.$element
					);
				} else {
					$folders[] = Array(
						'name' => $element,
						'path' => $path.'/'.$element
					);
				}
				continue;
			}
			if (is_file(BASE_LAB.$path.'/'.$element) && preg_match('/^.+\.unl$/', $element)) {
				if ($path == '/') {
					$labs[] = Array(
						'file' => $element,
						'path' => '/'.$element
					);
				} else {
					$labs[] = Array(
						'file' => $element,
						'path' => $path.'/'.$element
					);
				}
				continue;
			}
		}
	}

	// Sorting
	usort($folders, function($a, $b){
		return strnatcasecmp($a['name'], $b['name']);
	});
	usort($labs, function($a, $b){
		return strnatcasecmp($a['file'], $b['file']);
	});

	// Printing info
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60007];
	$output['data'] = Array(
		'folders' => $folders,
		'labs' => $labs
	);
	return $output;
}
?>
