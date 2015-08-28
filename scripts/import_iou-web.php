#!/usr/bin/php
<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * scripts/import_iou-web.php
 *
 * Script to import an iou-web database into UNetLab.
 *
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
 * @version 20150423
 */

$default_image = 'L3-TPGEN+ADVENTERPRISEK9-M-12.4-20090714.bin';
$dst = '/opt/unetlab/labs/Imported';

if (php_sapi_name() !== 'cli') {
	// Must be executed from CLI
	exit(1);
}

require_once('/opt/unetlab/html/includes/init.php');

if (!isset($argv[1])) {
	// File does not exists or not set
	error_log('ERROR: Must need an iou-web database as argument.');
	exit(1);
}

if (!is_file($argv[1])) {
	// File does not exists
	error_log('ERROR: iou-web database does not exists.');
	exit(2);
}

// Open the iou-web database
try {
	$db = new PDO('sqlite:'.$argv[1]);
	$db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (Exception $e) {
	error_log('ERROR: cannot open iou-web database.');
	error_log((string) $e);
	exit(3);
}

// Creating import dir if it does not exist
if (!is_dir($dst) && !mkdir($dst)) {
	error_log('ERROR: cannot create "'.$dst.'" dir.');
	exit(4);
}

// List all iou-web labs
try {
	$query_labs = 'SELECT lab_id, lab_name, lab_description, lab_info, lab_netmap FROM labs;';
	$statement_labs = $db -> prepare($query_labs);
	$statement_labs -> execute();
} catch (Exception $e) {
	error_log('ERROR: cannot list iou-web labs.');
	error_log((string) $e);
	exit(4);
}

// Import each lab
while ($result_labs = $statement_labs -> fetch(PDO::FETCH_ASSOC)) {
	//error_log('INFO: found iou-web lab "'.$result_labs['lab_name'].'" with lab_id = '.$result_labs['lab_id'].'.');
	$lab_file = $dst.'/'.$result_labs['lab_name'].'.unl';
	if (is_file($lab_file)) {
		error_log('ERROR: skipping lab lab_id = '.$result_labs['lab_id'].', file "'.$lab_file.'" already exists.');
		continue;
	}

	// Adding new file
	try {
		$lab = new Lab($lab_file, 0);
	} catch (Exception $e) {
		error_log('ERROR: skipping lab lab_id = '.$result_labs['lab_id'].', error while creating lab.');
		error_log((string) $e);
		continue;
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
	} catch (Exception $e) {
		error_log('ERROR: cannot list pictures for iou-web lab "'.$result_labs['lab_name'].'.');
		error_log((string) $e);
	}

	while ($result_pictures = $statement_pictures -> fetch(PDO::FETCH_ASSOC)) {
		//error_log('INFO: found iou-web picture img_name = '.$result_pictures['img_name'].' with img_id = '.$result_pictures['img_id'].'.');
		$p_picture = Array(
			'type' => 'image/png',
			'data' => $result_pictures['img_content']
		);
		if (!empty($result_pictures['img_name'])) $p_picture['name'] =  $result_pictures['img_name'];
		if (!empty($result_pictures['img_map'])) $p_picture['map'] =  preg_replace('/:20*([0-9]+)/', ':{{NODE$1}}', $result_pictures['img_map']);
		$rc = $lab -> addPicture($p_picture);
		if ($rc !== 0) {
			error_log('ERROR: skipping picture img_id = '.$result_pictures['img_id'].', error while creating picture.');
			error_log($GLOBALS['messages'][$rc]);
		}
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
						'top' => (int) $result_nodes['dev_top'].'%',
						'left' => (int) $result_nodes['dev_left'].'%'
					);

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

// TODO fixpermissions
exit(0);
?>
