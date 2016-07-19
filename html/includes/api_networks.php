<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_networks.php
 *
 * Networks related functions for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
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

	$id = $lab -> getFreeNetworkId();
	if ($o == True && isset($p['name'])) $p['name'] = $p['name'].$id;

	// Adding the network
	$rc = $lab -> addNetwork($p);

	if ($rc === 0) {
		// Network added
		$output['code'] = 201;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60006];
		$output['data'] = array(
			'id'=>$id
		);
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
	$network = $lab->getNetworks()[$id];
	$rc = $lab -> deleteNetwork($id);

	if ($rc === 0) {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60023];
		$output['data'] = Array(
			'id'=>$id,
			'count' => $network -> getCount(),
			'left' => $network -> getLeft(),
			'name' => $network -> getName(),
			'top' => $network -> getTop(),
			'type' => $network -> getNType()
		);
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
			'count' => $network -> getCount(),
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
			'count' => $network -> getCount(),
			'left' => $network -> getLeft(),
			'name' => $network -> getName(),
			'top' => $network -> getTop(),
			'type' => $network -> getNType()
		);
	}
	return $output;
}
?>
