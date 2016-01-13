<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_configs.php
 *
 * Configs related functions for REST APIs.
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
 * @copyright 2014-2016 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20151123
 */

/**
 * Function to add a network to a lab.
 *
 * @param   Lab     $lab                Lab
 * @param   Array   $p                  Parameters
 * @param   bool    $o                  True if need to add ID to name
 * @return  Array                       Return code (JSend data)
 */
/*
function apiAddLabNetwork($lab, $p, $o) {
	// Adding network_id to network_name if required
	if ($o == True && isset($p['name'])) $p['name'] = $p['name'].$lab -> getFreeNetworkId();

	// Adding the network
	$rc = $lab -> addNetwork($p);

	if ($rc === 0) {
		// Network added
		$output['code'] = 201;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60006];
	} else {
		// Failed to add network
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	}
	return $output;
}
 */

/**
 * Function to delete a lab network.
 *
 * @param   Lab     $lab                Lab
 * @param   int     $id                 Network ID
 * @return  Array                       Return code (JSend data)
 */
/*
function apiDeleteLabNetwork($lab, $id) {
	// Deleting the network
	$rc = $lab -> deleteNetwork($id);

	if ($rc === 0) {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60023];
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	}
	return $output;
}
 */

/**
 * Function to edit a lab config.
 *
 * @param   Lab     $lab                Lab
 * @param   Array   $p                  Parameters
 * @return  Array                       Return code (JSend data)
 */
function apiEditLabConfig($lab, $p) {
	if (!isset($lab -> getNodes()[$p['id']])) {
		// Node not found
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][20024];
		return $output;
	}

	// Edit config
	$rc = $lab -> setNodeConfigData($p['id'], $p['data']);
	if ($rc === 0) {
		$output['code'] = 201;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60023];
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$rc];
	}
	return $output;
}

/**
 * Function to get a single startup-config.
 *
 * @param   Lab     $lab                Lab
 * @param   int     $id                 Node  ID
 * @return  Array                       startup-config (JSend data)
 */
function apiGetLabConfig($lab, $id) {
	// Getting startup-configs
	$nodes = $lab -> getNodes();

	if (isset($nodes[$id]) && isset($GLOBALS['node_config'][$nodes[$id] -> getTemplate()])) {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60057];
		$output['data'] = Array();
		$output['data']['name'] = $nodes[$id] -> getName();
		$output['data']['id'] = $id;
		$output['data']['data'] = $nodes[$id] -> getConfigData();
	} else {
		$output['code'] = 200;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60058];
	}
	return $output;
}

/**
 * Function to get all startup-configs.
 *
 * @param   Lab     $lab                Lab
 * @return  Array                       startup-configs (JSend data)
 */
function apiGetLabConfigs($lab) {
	// Getting startup-configs
	$nodes = $lab -> getNodes();

	// Printing startup-configs
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60055];
	$output['data'] = Array();
	foreach ($nodes as $node_id => $node) {
		if (isset($GLOBALS['node_config'][$node -> getTemplate()])) {
			$output['data'][$node_id] = Array(
				'config' => $node -> getConfig(),
				'name' => $node -> getName()
			);
		}
	}
	return $output;
}
?>
