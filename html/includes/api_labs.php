<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_labs.php
 *
 * Labs related functions for REST APIs.
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
 * @version 20150428
 */

/*
 * Function to add a lab.
 *
 * @param	Array		$p				Parameters
 * @return	Array						Return code (JSend data)
 */
function apiAddLab($p, $tenant) {
	// Check mandatory parameters
	if (!isset($p['path']) || !isset($p['name'])) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60017];
		return $output;
	}

	// Parent folder must exist
	if (!is_dir(BASE_LAB.$p['path'])) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60018];
		return $output;
	}

	if ($p['path'] == '/') {
		$lab_file = '/'.$p['name'].'.unl';
	} else {
		$lab_file = $p['path'].'/'.$p['name'].'.unl';
	}

	if (is_file(BASE_LAB.$lab_file)) {
		$output['code'] = 304;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60016];
		return $output;
	}

	try {
		// Create the lab
		$lab = new Lab(BASE_LAB.$lab_file, $tenant);
	} catch(ErrorException $e) {
		// Failed to create the lab
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = (string) $e;
		return $output;
	}

	// Set author/description/version
	$rc = $lab -> edit($p);
	if ($rc !== 0) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	}

	// Printing info
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60019];
	return $output;
}

/*
 * Function to add a lab.
 *
 * @param	Array		$p				Parameters
 * @return	Array						Return code (JSend data)
 */
function apiCloneLab($p, $tenant) {
	$rc = checkFolder(BASE_LAB.dirname($p['source']));
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
	
	if(!is_file(BASE_LAB.$p['source'])) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60000];
		return $output;
	}
	
	if (!copy(BASE_LAB.$p['source'], BASE_LAB.dirname($p['source']).'/'.$p['name'].'.unl')) {
		// Failed to copy
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60037];
		error_log('ERROR: '.$GLOBALS['messages'][60037]);
		return $output;
	}
	
	try {
		$lab = new Lab(BASE_LAB.dirname($p['source']).'/'.$p['name'].'.unl', $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	
	$rc = $lab -> edit($p);
	if ($rc !== 0) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60036];
	}
	
	return $output;
}

/*
 * Function to delete a lab.
 *
 * @param	string		$lab_id			Lab ID
 * @param	string		$lab_file		Lab file
 * @return	Array						Return code (JSend data)
 */
function apiDeleteLab($lab) {
	$tenant = $lab -> getTenant();
	$lab_id = $lab -> getId();
	$lab_file = $lab -> getPath().'/'.$lab -> getFilename();

	$cmd = 'sudo /opt/unetlab/wrappers/unl_wrapper';
	$cmd .= ' -a delete';
	$cmd .= ' -F "'.$lab_file.'"';
	$cmd .= ' -T 0';	// Tenant not required for delete operation
	$cmd .= ' 2>> /opt/unetlab/data/Logs/unl_wrapper.txt';
	exec($cmd, $o, $rc);
	if ($rc == 0 && unlink($lab_file)) {
		$output['code'] = 200;
		$output['status'] = 'success';
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60021];
	}
	return $output;
}

/*
 * Function to edit a lab.
 *
 * @param	Lab			$lab			Lab
 * @param	Array		$lab			Parameters
 * @return	Array						Return code (JSend data)
 */
function apiEditLab($lab, $p) {
	// Set author/description/version
	$rc = $lab -> edit($p);
	if ($rc !== 0) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60023];
	}
	return $output;
}

/*
 * Function to edit a lab.
 *
 * @param	Array		$lab			Parameters
 * @return	Array						Return code (JSend data)
 */
function apiExportLab($p) {
	print_r($p);
	$export_file = tempnam('/tmp', 'unetlab_export_');
	$zip = new ZipArchive();
	$fp = $zip -> open($export_file, ZipArchive::CREATE);
	foreach ($p as $value) {
		if (checkFolder(BASE_LAB.$value) && is_file(BASE_LAB.$value)) {
			$zip -> addFile(BASE_LAB.$value);
		}
	}
	$zip -> close();
	
	// Set author/description/version
	$rc = 0;
	if ($rc !== 0) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60023];
	}
	return $output;
}

/*
 * Function to get a lab.
 *
 * @param	Lab			$lab			Lab
 * @return	Array						Return code (JSend data)
 */
function apiGetLab($lab) {
	// Printing info
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60020];
	$output['data'] = Array(
		'author' => $lab -> getAuthor(),
		'description' => $lab -> getDescription(),
		'id' => $lab -> getId(),
		'name' => $lab -> getName(),
		'version' => $lab -> getVersion(),
	);
	return $output;
}

/*
 * Function to get all lab links (networks and serial endpoints).
 *
 * @param	Lab			$lab			Lab file
 * @return	Array						Return code (JSend data)
 */
function apiGetLabLinks($lab) {
	$output['data'] = Array();

	// Get ethernet links
	$ethernets = Array();
	$networks = $lab -> getNetworks();
	if (!empty($networks)) {
		foreach ($lab -> getNetworks() as $network_id => $network) {
			$ethernets[$network_id] = $network -> getName();
		}
	}

	// Get serial links
	$serials = Array();
	$nodes = $lab -> getNodes();
	if (!empty($nodes)) {
		foreach ($nodes as $node_id => $node) {
			if (!empty($node -> getSerials())) {
				$serials[$node_id] = Array();
				foreach ($node -> getSerials() as $interface_id => $interface) {
					// Print all available serial links
					$serials[$node_id][$interface_id] = $node -> getName().' '.$interface -> getName();
				}
			}
		}
	}

	// Printing info
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60024];
	$output['data']['ethernet'] = $ethernets;
	$output['data']['serial'] = $serials;
	return $output;
}

/*
 * Function to move a lab inside another folder.
 *
 * @param	Lab			$lab			Lab
 * @param	string		$path			Destination path
 * @return	Array						Return code (JSend data)
 */
function apiMoveLab($lab, $path) {
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
	
	if(is_file(BASE_LAB.$path.'/'.$lab -> getFilename())) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60016];
		return $output;
	}
	
	if (rename($lab -> getPath().'/'.$lab -> getFilename(), BASE_LAB.$path.'/'.$lab -> getFilename())) {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60035];
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60034];
		error_log('ERROR: '.$GLOBALS['messages'][60034]);
	}
	return $output;
}
?>
