<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1

/**
 * html/includes/api_topology.php
 *
 * Topology related functions for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/**
 * Function to add a node to a lab.
 *
 * @param   Lab     $lab                Lab
 * @return  Array                       Return code (JSend data)
 */
function apiGetLabTopology($lab) {
 	// Printing topology
	$output['code'] = '200';
	$output['status'] = 'success';
	$output['message'] = 'Topology loaded';
	$output['data'] = Array();
	foreach ($lab -> getNodes() as $node_id => $node) {
		foreach ($node -> getEthernets() as $interface) {
			if ($interface -> getNetworkId() != '' && isset($lab -> getNetworks()[$interface -> getNetworkId()])) {
				// Interface is connected
				switch ($lab -> getNetworks()[$interface -> getNetworkId()] -> getCount()) {
					default:
						// More than two connected nodes
						$output['data'][] = Array(
							'type' => 'ethernet',
							'source' => 'node'.$node_id,
							'source_type' => 'node',
							'source_label' => $interface -> getName(),
							'destination' => 'network'.$interface -> getNetworkId(),
							'destination_type' => 'network',
							'destination_label' => ''
						);
						break;
					case 0:
						// Network not used
						break;
					case 1:
						// Only one connected node
						$output['data'][] = Array(
							'type' => 'ethernet',
							'source' => 'node'.$node_id,
							'source_type' => 'node',
							'source_label' => $interface -> getName(),
							'destination' => 'network'.$interface -> getNetworkId(),
							'destination_type' => 'network',
							'destination_label' => ''
						);
						break;
					case 2:
						// P2P Link
						if ($lab -> getNetworks()[$interface -> getNetworkId()] -> isCloud()) {
							// Cloud are never printed as P2P link
							$output['data'][] = Array(
								'type' => 'ethernet',
								'source' => 'node'.$node_id,
								'source_type' => 'node',
								'source_label' => $interface -> getName(),
								'destination' => 'network'.$interface -> getNetworkId(),
								'destination_type' => 'network',
								'destination_label' => ''
							);
						} else {
							foreach ($lab -> getNodes() as $remote_node_id => $remote_node) {
								foreach ($remote_node -> getEthernets() as $remote_interface) {
									if ($interface -> getNetworkId() == $remote_interface -> getNetworkId()) {
										// To avoid duplicates, only print if source node_id > destination node_id
										if ($node_id > $remote_node_id) {
											$output['data'][] = Array(
												'type' => 'ethernet',
												'source' => 'node'.$node_id,
												'source_type' => 'node',
												'source_label' => $interface -> getName(),
												'destination' => 'node'.$remote_node_id,
												'destination_type' => 'node',
												'destination_label' => $remote_interface -> getName()
											);
										}
										break;
									}
								}
							}
						}
						break;
				}
			}
		}
		foreach ($node -> getSerials() as $interface) {
			if ($interface -> getRemoteID() != '' && $node_id > $interface -> getRemoteId()) {
				$output['data'][] = Array(
					'type' => 'serial',
					'source' => 'node'.$node_id,
					'source_type' => 'node',
					'source_label' => $interface -> getName(),
					'destination' => 'node'.$interface -> getRemoteID(),
					'destination_type' => 'node',
					'destination_label' => $lab -> getNodes()[$interface -> getRemoteID()] -> getSerials()[$interface -> getRemoteIf()] -> getName()
				);
			}
		}
	}

	return $output;
}
?>
