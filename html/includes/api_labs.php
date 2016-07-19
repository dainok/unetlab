<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_labs.php
 *
 * Labs related functions for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
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
		$output['code'] = 400;
		$output['status'] = 'fail';
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][60037]);
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
	$lab -> setId();
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
		$output['message'] = $GLOBALS['messages'][60022];
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
 * Function to export labs.
 *
 * @param	Array		$p				Parameters
 * @return	Array						Return code (JSend data)
 */
function apiExportLabs($p) {
	$export_url = '/Exports/unetlab_export-'.date('Ymd-His').'.zip';
	$export_file = '/opt/unetlab/data'.$export_url;
	if (is_file($export_file)) {
		unlink($export_file);
	}
	
	if (checkFolder(BASE_LAB.$p['path']) !== 0) {
		// Path is not valid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][80077];
		return $output;
	}
	
	if (!chdir(BASE_LAB.$p['path'])) {
		// Cannot set CWD
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS[80072];
		return $output;
	}
	
	foreach ($p as $key => $element) {
		if ($key === 'path') {
			continue;
		}
		
		// Using "element" relative to "path", adding '/' if missing
		$relement = substr($element, strlen($p['path']));
		if ($relement[0] != '/') {
			$relement = '/'.$relement;
		}
		
		if (is_file(BASE_LAB.$p['path'].$relement)) {
			// Adding a file
			$cmd = 'zip '.$export_file.' ".'.$relement.'"';
			exec($cmd, $o, $rc);
			if ($rc != 0) {
				$output['code'] = 400;
				$output['status'] = 'fail';
				$output['message'] = $GLOBALS['messages'][80073];
				return $output;
			}
		}
		
		if (checkFolder(BASE_LAB.$p['path'].$relement) === 0) {
			// Adding a dir
			$cmd = 'zip -r '.$export_file.' ".'.$relement.'"';
			exec($cmd, $o, $rc);
			if ($rc != 0) {
				$output['code'] = 400;
				$output['status'] = 'fail';
				$output['message'] = $GLOBALS['messages'][80074];
				return $output;
			}
		}
	}
	
	// Now remove UUID from labs
	$cmd = BASE_DIR.'/scripts/remove_uuid.sh "'.$export_file.'"';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		if (is_file($export_file)) {
			unlink($export_file);
		}
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
		return $output;
	}
	
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][80075];
	$output['data'] = $export_url;
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
		'body' => $lab -> getBody(),
		'filename' => $lab -> getFilename(),
		'id' => $lab -> getId(),
		'name' => $lab -> getName(),
		'version' => $lab -> getVersion(),
		'scripttimeout' => $lab -> getScriptTimeout(),
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
 * Function to import labs.
 *
 * @param	Array		$p				Parameters
 * @return	Array						Return code (JSend data)
 */
function apiImportLabs($p) {
	ini_set('max_execution_time', '300');
	ini_set('memory_limit', '64M');

	if (!isset($p['file']) || empty($p['file'])) {
		// Upload failed
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][80081];
		return $output;
	}

	if (!isset($p['path'])) {
		// Path is not set
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][80076];
		return $output;
	}
	
	if (checkFolder(BASE_LAB.$p['path']) !== 0) {
		// Path is not valid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][80077];
		return $output;
	}
	
	$finfo = new finfo(FILEINFO_MIME);
	if (strpos($finfo -> file($p['file']), 'application/zip') !== False) {
		// UNetLab export
		$cmd = 'unzip -o -d "'.BASE_LAB.$p['path'].'" '.$p['file'].' *.unl';
		exec($cmd, $o, $rc);
		if ($rc != 0) {
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][80079];
			return $output;
		}

		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][80080];
		return $output;
	} else if (strpos($finfo -> file($p['file']), 'application/x-gzip') !== False) {
		// iou-web export
		$tmp = tempnam(sys_get_temp_dir(), 'iouweb_');
		$dst = '/opt/unetlab/labs/Imported';
		$cmd = 'gunzip -c '.$p['file'].' > '.$tmp;
		$default_image = 'L3-TPGEN+ADVENTERPRISEK9-M-12.4-20090714.bin';
		exec($cmd, $o, $rc);
		if ($rc != 0) {
			unlink($tmp);
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][80086];
			return $output;
		}
		
		// Open the iou-web database
		try {
			$db = new PDO('sqlite:'.$tmp);
			$db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		} catch (Exception $e) {
			unlink($tmp);
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][80086];
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80086]);
			error_log(date('M d H:i:s ').(string) $e);
			return $output;
		}

		// Creating import dir if it does not exist
		if (!is_dir($dst) && !mkdir($dst)) {
			unlink($tmp);
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][80086];
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80086]);
			error_log(date('M d H:i:s ').(string) $e);
			return $output;
		}

		// List all iou-web labs
		try {
			$query_labs = 'SELECT lab_id, lab_name, lab_description, lab_info, lab_netmap FROM labs;';
			$statement_labs = $db -> prepare($query_labs);
			$statement_labs -> execute();
		} catch (Exception $e) {
			unlink($tmp);
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][80086];
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80086]);
			error_log(date('M d H:i:s ').(string) $e);
			return $output;
		}

		// Import each lab
		while ($result_labs = $statement_labs -> fetch(PDO::FETCH_ASSOC)) {
			//error_log('INFO: found iou-web lab "'.$result_labs['lab_name'].'" with lab_id = '.$result_labs['lab_id'].'.');
			$lab_file = $dst.'/'.$result_labs['lab_name'].'.unl';
			if (is_file($lab_file)) {
				error_log('ERROR: skipping lab lab_id = '.$result_labs['lab_id'].', file "'.$lab_file.'" already exists.');
				//continue;
				unlink($lab_file);
			}

			// Adding new file
			try {
				$lab = new Lab($lab_file, 0);
			} catch (Exception $e) {
				unlink($tmp);
				$output['code'] = 400;
				$output['status'] = 'fail';
				$output['message'] = $GLOBALS['messages'][80086];
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80086]);
				error_log(date('M d H:i:s ').(string) $e);
				return $output;
			}

			//error_log('INFO: importing lab "'.$result_labs['lab_name'].'.');

			// Setting author, description, version
			$p_lab = Array(
				'author' => 'Imported from iou-web',
				'version' => date('Ymd')
			);
			if (!empty($result['lab_description']) || !empty($result_labs['lab_info'])) $p_lab['description'] = trim($result_labs['lab_description'].' '.$result_labs['lab_info']);
			$rc = $lab -> edit($p_lab);
			if ($rc !== 0) {
				error_log('ERROR: failed to set author/description/version while importing lab "'.$result_labs['lab_name'].'.');
				error_log($GLOBALS['messages'][$rc]);
			};
			
			// Adding pictures
			try {
				$query_pictures = 'SELECT images.img_id, img_name, img_content, img_map FROM images LEFT JOIN rel_img_lab ON images.img_id = rel_img_lab.img_id WHERE rel_img_lab.lab_id = :lab_id';
				$statement_pictures = $db -> prepare($query_pictures);
				$statement_pictures -> bindParam(':lab_id', $result_labs['lab_id'], PDO::PARAM_INT);
				$statement_pictures -> execute();
				$statement_pictures -> execute();
				while ($result_pictures = $statement_pictures -> fetch(PDO::FETCH_ASSOC)) {
					//error_log('INFO: found iou-web picture img_name = '.$result_pictures['img_name'].' with img_id = '.$result_pictures['img_id'].'.');
					$p_picture = Array(
						'type' => 'image/png',
						'data' => $result_pictures['img_content']
					);
					if (!empty($result_pictures['img_name'])) $p_picture['name'] =  $result_pictures['img_name'];
					if (!empty($result_pictures['img_map'])) {
						$p_picture['map'] =  $result_pictures['img_map'];
						$p_picture['map'] = preg_replace_callback('/:2*([0-9]+)/', function($m) { return ':{{NODE$'.((int) $m[1]).'}}'; }, $p_picture['map']);
						//$p_picture['map'] = preg_replace_callback('/coords=\'([0-9]+),([0-9]+),/', function($m) { return 'coords=\''.((int) ($m[1] / 1.78)).','.((int) ($m[2] / 1.78).','); }, $p_picture['map']);
					}
					$rc = $lab -> addPicture($p_picture);
					if ($rc !== 0) {
						error_log('ERROR: skipping picture img_id = '.$result_pictures['img_id'].', error while creating picture.');
						error_log($GLOBALS['messages'][$rc]);
					}
				}
			} catch (Exception $e) {
				error_log('ERROR: cannot list pictures for iou-web lab "'.$result_labs['lab_name'].'.');
				error_log((string) $e);
			}
			
			// Parsing NETMAP
			$netmap = preg_replace('/(#.*)/', '', $result_labs['lab_netmap']);				// Remove comments
			$netmap = preg_replace("/(^[\r\n]*|[\r\n]+)[\s\t]*[\r\n\']+/", "\n", $netmap);	// Remove empty lines
			$netmap = preg_replace("/[\s]+\n/", "\n", $netmap);								// Remove trailing spaces (trim lines)
			$netmap = trim($netmap);														// Remove trailing spaces (trim all)

			$network_id = 1;
			$node_id = 1;
			$all_nodes = Array();		// Key is iou-web node_id, value is UNetLab node_id
			$all_ethernets = Array();	// Key is iou-web node_id, value is configured ethernet interfaces

			foreach (explode("\n", $netmap) as $line) {
				$line = preg_replace('/\s+/', ' ', $line);	// Remove duplicated spaces
				$elements = explode(' ', $line);
				$network_added = False;
				$remote_node = False;
				foreach ($elements as $element) {
					$id = (int) substr($element, 0, strpos($element, ':'));
					$portgroup = (int) substr($element, strpos($element, ':') + 1, strpos($element, '/'));
					$interface = (int) substr($element, strpos($element, '/') + 1);
					$interface_id = $portgroup + $interface * 16;
					//error_log('INFO: found iou-web node '.$id.':'.$portgroup.'/'.$interface.'.');
					if ($id < 1) {
						error_log('ERROR: skipping node, invalid iou-web ID.');
						continue;
					}

					if (!isset($all_nodes[$id])) {
						// New node, need to create
						// Getting a single node
						try {
							$query_nodes = 'SELECT dev_name, bin_name, dev_ram, dev_nvram, dev_ethernet, dev_serial, dev_picture, dev_delay, dev_top, dev_left, cfg_config FROM devices LEFT JOIN configs ON devices.cfg_id = configs.cfg_id WHERE dev_id = :dev_id AND lab_id = :lab_id AND dev_picture != "cloud";';
							$statement_nodes = $db -> prepare($query_nodes);
							$statement_nodes -> bindParam(':dev_id', $id, PDO::PARAM_INT);
							$statement_nodes -> bindParam(':lab_id', $result_labs['lab_id'], PDO::PARAM_INT);
							$statement_nodes -> execute();
							$result_nodes = $statement_nodes -> fetch(PDO::FETCH_ASSOC);
							$p_node = Array(
								'iou-web' => $id,
								'id' => $node_id,
								'type' => 'iol',
								'template' => 'iol',
								'name' => $result_nodes['dev_name'],
								'image' => $result_nodes['bin_name'],
								'nvram' => (int) $result_nodes['dev_nvram'],
								'ram' => (int) $result_nodes['dev_ram'],
								'ethernet' => (int) $result_nodes['dev_ethernet'],
								'serial' => (int) $result_nodes['dev_serial'],
								'picture' => $result_nodes['dev_picture'],
								'delay' => (int) $result_nodes['dev_delay'],
								'top' => 768 * $result_nodes['dev_top'] / 100,
								'left' => 1024 * $result_nodes['dev_left'] / 100
							);
							
							if ($p_node['top'] == 0) unset($p_node['top']);
							if ($p_node['left'] == 0) unset($p_node['left']);

							// Fixing images
							if (!is_file('/opt/unetlab/addons/iol/bin/'.$p_node['image'])) $p_node['image'] = $default_image;

							// Fixing pictures
							if ($p_node['picture'] == 'desktop') $p_node['picture'] = 'Desktop.png';
							if ($p_node['picture'] == 'hub') $p_node['picture'] = 'HUB.png';
							if ($p_node['picture'] == 'mpls') $p_node['picture'] = 'MPLS.png';
							if ($p_node['picture'] == 'router') $p_node['picture'] = 'Router.png';
							if ($p_node['picture'] == 'framerelay') $p_node['picture'] = 'Frame Relay.png';
							if ($p_node['picture'] == 'l3switch') $p_node['picture'] = 'Switch L3.png';
							if ($p_node['picture'] == 'switch') $p_node['picture'] = 'Switch.png';
							if ($p_node['picture'] == 'nam') $p_node['picture'] = 'Network Analyzer.png';

							//error_log('INFO: adding node node_id = '.$node_id.' (name = '.$p_node['name'].', image = '.$p_node['image'].', nvram = '.$p_node['nvram'].', ram = '.$p_node['ram'].', eth = '.$p_node['ethernet'].', ser = '.$p_node['serial'].', picture = '.$p_node['picture'].', delay = '.$p_node['delay'].', top = '.$p_node['top'].', left = '.$p_node['left'].').');
							//print_r('INFO: adding node node_id = '.$node_id.' (name = '.$p_node['name'].', image = '.$p_node['image'].', nvram = '.$p_node['nvram'].', ram = '.$p_node['ram'].', eth = '.$p_node['ethernet'].', ser = '.$p_node['serial'].', picture = '.$p_node['picture'].', delay = '.$p_node['delay'].', top = '.$p_node['top'].', left = '.$p_node['left'].').');

							$rc = $lab -> addNode($p_node);
							if ($rc !== 0) {
								error_log('ERROR: skipping node node_id = '.$node_id.', error while importing.');
								error_log($GLOBALS['messages'][$rc]);
								continue;
							}

							// Adding startup-config
							if (!empty($result_nodes['cfg_config'])) {
								//error_log('INFO: adding config for node_id = '.$node_id.').');
							}
							$rc = $lab -> setNodeConfigData($node_id, $result_nodes['cfg_config']);
							if ($rc !== 0) {
								error_log('ERROR: skipping config for for node_id = '.$node_id.', error while importing.');
								error_log($GLOBALS['messages'][$rc]);
							}

							$all_nodes[$id] = $node_id;
							$all_ethernets[$id] = $p_node['ethernet'];
							$node_id = $node_id + 1;
						} catch (Exception $e) {
							error_log('ERROR: skipping node dev_id = '.$id.', error while creating node.');
							error_log((string) $e);
							continue;
						}
					} else {
						//error_log('INFO: skipping iou-web node '.$id.':'.$portgroup.'/'.$interface.' ('.$interface_id.'), already created.');
					}

					// Node is added, need to connect interfaces
					if ($portgroup <= $all_ethernets[$id] - 1) {
						// Got an ethernet inteface
						if ($network_added === False) {
							// Need to create the network
							//error_log('INFO: adding network network_id = '.$network_id.').');
							$p_network = Array(
								'type' => 'bridge',
								'name' => 'Net'.$network_id
							);
							$rc = $lab -> addNetwork($p_network);
							if ($rc != 0) {
								error_log('ERROR: skipping network network_id = '.$network_id.', error while creating.');
								error_log($GLOBALS['messages'][$rc]);
								continue;
							} else {
								$network_added = True;
							}
						}

						// Connect the node
						$p_interface = Array(
							$interface_id => $network_id
						);
						//error_log('INFO: connecting (ethernet) node '.$id.':'.$portgroup.'/'.$interface.' ('.$all_nodes[$id].':'.$interface_id.') to network '.$network_id.'.');
						$rc = $lab -> connectNode($all_nodes[$id], $p_interface);
						if ($rc != 0) {
							error_log('ERROR: skipping interface '.$portgroup.'/'.$interface.' ('.$all_nodes[$id].':'.$interface_id.') for node_id = '.$all_nodes[$id].', error while connecting.');
							error_log($GLOBALS['messages'][$rc]);
						}
					} else {
						// Got a serial interface
						if ($remote_node === False) {
							// Fisrt node on this link
							$remote_node = $all_nodes[$id].':'.$interface_id;
						} else {
							// Second node on this link, connect and reset the parameter
							$p_interface = Array(
								$interface_id => $remote_node
							);
							//error_log('INFO: connecting (serial) node '.$all_nodes[$id].':'.$portgroup.'/'.$interface.' ('.$all_nodes[$id].':'.$interface_id.') to node '.$remote_node.'.');
							$rc = $lab -> connectNode($all_nodes[$id], $p_interface);
							if ($rc != 0) {
								error_log('ERROR: skipping interface '.$portgroup.'/'.$interface.' ('.$all_nodes[$id].':'.$interface_id.') for node_id = '.$all_nodes[$id].', error while connecting.');
								error_log($GLOBALS['messages'][$rc]);
							}
							$remote_node = False;
						}
					}
				}
				if ($network_added === True) {
					$network_id = $network_id + 1;
					$network_added = False;
				}
			}
			error_log('INFO: lab "'.$result_labs['lab_name'].'" imported into "'.$lab_file.'".');
		}

		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][80087];
		unlink($tmp);
		return $output;	
	} else {
		// File is not a Zip
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][80078];
		return $output;	
	}
	
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][60034]);
	}
	return $output;
}
?>
