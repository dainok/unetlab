<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_networks.php
 *
 * Networks related functions for REST APIs.
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

/**
 * Function to add a network to a lab.
 *
 * @param   Lab     $lab                Lab
 * @param   Array   $p                  Parameters
 * @param   bool    $o                  True if need to add ID to name
 * @return  Array                       Return code (JSend data)
 */
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

/**
 * Function to delete a lab network.
 *
 * @param   Lab     $lab                Lab
 * @param   int     $id                 Network ID
 * @return  Array                       Return code (JSend data)
 */
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

/**
 * Function to edit a lab network.
 *
 * @param   Lab     $lab                Lab
 * @param   Array   $p                  Parameters
 * @return  Array                       Return code (JSend data)
 */
function apiEditLabNetwork($lab, $p) {
	// Edit network
	$rc = $lab -> editNetwork($p);

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
 * Function to get a single lab network.
 *
 * @param   Lab     $lab                Lab
 * @param   int     $id                 Network ID
 * @return  Array                       Lab network (JSend data)
 */
function apiGetLabNetwork($lab, $id) {
	// Getting network
	if (isset($lab -> getNetworks()[$id])) {
		$network = $lab -> getNetworks()[$id];

		// Printing networks
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60005];
		$output['data'] = Array(
			'left' => $network -> getLeft(),
			'name' => $network -> getName(),
			'top' => $network -> getTop(),
			'type' => $network -> getNType()
		);
	} else {
		// Network not found
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][20023];
	}
	return $output;
}

/**
 * Function to get all lab networks.
 *
 * @param   Lab     $lab                Lab
 * @return  Array                       Lab networks (JSend data)
 */
function apiGetLabNetworks($lab) {
	// Getting network(s)
	$networks = $lab -> getNetworks();

	// Printing networks
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60004];
	$output['data'] = Array();
	foreach ($networks as $network_id => $network) {
		$output['data'][$network_id] = Array(
			'id' => $network_id,
			'left' => $network -> getLeft(),
			'name' => $network -> getName(),
			'top' => $network -> getTop(),
			'type' => $network -> getNType()
		);
	}
	return $output;
}
?>
