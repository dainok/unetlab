#!/usr/bin/env php
<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * wrappers/unl_wrapper
 *
 * CLI handler for UNetLab
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
 * Foobar is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Foobar. If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2015 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20150526
 */

require_once('/opt/unetlab/html/includes/init.php');

// Checking if called from CLI or Web
if (php_sapi_name() != 'cli') {
	error_log('ERROR: '.$GLOBALS['messages'][1]);
	exit(1);
}

// Checking privileges
if (posix_getuid() != 0) {
	error_log('ERROR: '.$GLOBALS['messages'][2]);
	exit(2);
}

// Setting umask
umask(0002);

// Parsing and checking parameters
$options = getopt('oT:D:F:a:');

// Checking -a (action)
if (!isset($options['a'])) {
	usage();
	error_log('ERROR: '.$GLOBALS['messages'][3]);
	exit(3);
}
$action = $options['a'];

// Checking -T (Tenant ID)
if (in_array($action, Array('delete', 'export', 'start', 'stop', 'wipe'))) {
	if (!isset($options['T'])) {
		// Tenant ID is missing
		usage();
		error_log('ERROR: '.$GLOBALS['messages'][4]);
		exit(4);
	} else if ((int) $options['T'] < 0) {
		// Tenant ID is not valid
		usage();
		error_log('ERROR: '.$GLOBALS['messages'][5]);
		exit(5);
	} else {
		$tenant = (int) $options['T'];
	}
}

// Checking -F (Lab file)
if (in_array($action, Array('delete', 'export', 'start', 'stop', 'wipe'))) {
	if (!is_file($options['F'])) {
		// File not found
		usage();
		error_log('ERROR: '.$GLOBALS['messages'][6]);
		exit(6);
	}

	try {
		$lab = new Lab($options['F'], $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		error_log('ERROR: '.$GLOBALS['messages'][$e -> getMessage()]);
		error_log('ERROR: '.$GLOBALS['messages'][7]);
		exit(7);
	}
}

// Checking -D (Node ID)
if (isset($options['D'])) {
	if ((int) $options['D'] > 0 && isset($lab -> getNodes()[$options['D']])) {
		$node_id = (int) $options['D'];
	} else {
		// Node ID must be numeric, greater than 0 and exists on lab
		usage();
		error_log('ERROR: '.$GLOBALS['messages'][8]);
		exit(8);
	}
}

switch ($action) {
	default:
		// Invalid action
		usage();
		error_log('ERROR: '.$GLOBALS['messages'][9]);
		exit(9);
	case 'delete':
		if (isset($node_id)) {
			// Removing temporary files for a single node in all tenants
			$cmd = 'rm -rf /opt/unetlab/tmp/*/'.$lab -> getId().'/'.$node_id.'/';
		} else {
			// Removing all temporary files in all tenants
			$cmd = 'rm -rf /opt/unetlab/tmp/*/'.$lab -> getId().'/';
		}
		exec($cmd, $o, $rc);
		break;
	case 'export':
		// Exporting node(s) running-config
		if (isset($node_id)) {
			// Node ID is set, export a single node
			export($node_id, $lab -> getNodes()[$node_id], $lab);
		} else {
			// Node ID is not set, export all nodes
			foreach ($lab -> getNodes() as $node_id => $node) {
				export($node_id, $node, $lab);
			}
		}
		break;
	case 'fixpermissions':
		// Default permissions for directories
		$cmd = '/usr/bin/find /opt/unetlab -type d -exec chown root:root {} \; > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		$cmd = '/usr/bin/find /opt/unetlab -type d -exec chmod 755 {} \; > /dev/null 2>&1';
		exec($cmd, $o, $rc);

		// Default permissions for files
		$cmd = '/usr/bin/find /opt/unetlab -type d -exec chown root:root {} \; > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		$cmd = '/usr/bin/find /opt/unetlab -type f -exec chmod 644 {} \; > /dev/null 2>&1';
		exec($cmd, $o, $rc);

		// /opt/unetlab/scripts
		$cmd = '/bin/chmod 755 /opt/unetlab/scripts/* > /dev/null 2>&1';
		exec($cmd, $o, $rc);

		// /opt/unetlab/data and /opt/unetlab/labs
		$cmd = '/bin/chown -R www-data:www-data /opt/unetlab/data /opt/unetlab/labs > /dev/null 2>&1';
		exec($cmd, $o, $rc);

		// /opt/unetlab/tmp
		$cmd = '/bin/chown -R root:unl /opt/unetlab/tmp > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		$cmd = '/bin/chmod -R g+w /opt/unetlab/tmp > /dev/null 2>&1';
		exec($cmd, $o, $rc);

		// /opt/unetlab/addons/iol/bin
		$cmd = '/bin/chmod 755 /opt/unetlab/addons/iol/bin/*.bin > /dev/null 2>&1';
		exec($cmd, $o, $rc);

		// Wrappers
		$cmd = '/bin/chmod 755 /opt/unetlab/wrappers/*_wrapper* > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		break;
	case 'platform':
		$cmd = '/usr/sbin/dmidecode -s system-product-name';
		exec($cmd, $o, $rc);
		print(implode('', $o)."\n");
		break;
	case 'start':
		// Starting node(s)
		if (!checkUsername($lab -> getTenant())) {
			// Cannot create username
			error_log('ERROR: '.$GLOBALS['messages'][14]);
			exit(14);
		}

		if (isset($node_id)) {
			// Node ID is set, create attached networks, prepare node and start it

			foreach ($lab -> getNodes()[$node_id] -> getEthernets() as $interface) {
				if ($interface -> getNetworkId() !== 0 && !isset($lab -> getNetworks()[$interface -> getNetworkId()])) {
					// Interface is set but network does not exist
					error_log('ERROR: '.$GLOBALS['messages'][10]);
					exit(10);
				} else if ($interface -> getNetworkId() !== 0) {
					// Create attached networks only
					$p = Array(
						'name' => 'vnet'.$lab -> getTenant().'_'.$interface -> getNetworkId(),
						'type' => $lab -> getNetworks()[$interface -> getNetworkId()] -> getNType()
					);
					$rc = addNetwork($p);
					if ($rc !== 0) {
						// Failed to create network
						error_log('ERROR: '.$GLOBALS['messages'][$rc]);
						error_log('ERROR: '.$GLOBALS['messages'][11]);
						exit(11);
					}
				}
			}

			// Starting the node
			$rc = start($lab -> getNodes()[$node_id], $node_id, $tenant, $lab -> getNetworks());
			if ($rc !== 0) {
				// Failed to start the node
				error_log('ERROR: '.$GLOBALS['messages'][$rc]);
				error_log('ERROR: '.$GLOBALS['messages'][12]);
				exit(12);
			}
		} else {
			// Node ID is not set, start all nodes

			// Create all networks
			foreach ($lab -> getNetworks() as $network_id => $network) {
				$p = Array(
					'name' => 'vnet'.$lab -> getTenant().'_'.$network_id,
					'type' => $network -> getNType()
				);
				$rc = addNetwork($p);
				if ($rc !== 0) {
					// Failed to create network
					error_log('ERROR: '.$GLOBALS['messages'][$rc]);
					error_log('ERROR: '.$GLOBALS['messages'][11]);
					exit(11);
				}
			}

			// Starting all non-IOL nodes
			foreach ($lab -> getNodes() as $node_id => $node) {
				if ($node -> getNType() != 'iol') {
					// IOL nodes drop privileges, so need to be postponed
					$rc = start($node, $node_id, $tenant, $lab -> getNetworks());
					if ($rc !== 0) {
						// Failed to start the node
						error_log('ERROR: '.$GLOBALS['messages'][$rc]);
						error_log('ERROR: '.$GLOBALS['messages'][12]);
						exit(12);
					}
				}
			}

			// Starting all IOL nodes
			foreach ($lab -> getNodes() as $node_id => $node) {
				if ($node -> getNType() == 'iol') {
					// IOL nodes drop privileges, so need to be postponed
					$rc = start($node, $node_id, $tenant, $lab -> getNetworks());
					if ($rc !== 0) {
						// Failed to start the node
						error_log('ERROR: '.$GLOBALS['messages'][$rc]);
						error_log('ERROR: '.$GLOBALS['messages'][12]);
						exit(12);
					}
				}
			}
		}
		break;
	case 'stop':
		// Stopping node(s)
		if (isset($node_id)) {
			// Node ID is set, stop and wipe the node
			stop($lab -> getNodes()[$node_id]);
		} else {
			// Node ID is not set, stop and wipe all nodes
			foreach ($lab -> getNodes() as $node) {
				stop($node);
			}
		}
		break;
	case 'wipe':
		// Removing temporary files
		if (isset($node_id)) {
			// Node ID is set, stop and wipe the node
			stop($lab -> getNodes()[$node_id]);
			$cmd = 'rm -rf "/opt/unetlab/tmp/'.$tenant.'/'.$lab -> getId().'/'.$node_id.'/"';
			exec($cmd, $o, $rc);
			if ($rc !== 0) {
				error_log('ERROR: '.$GLOBALS['messages'][13]);
				error_log(implode("\n", $o));
				exit(13);
			}
		} else {
			// Node ID is not set, stop and wipe all nodes
			foreach ($lab -> getNodes() as $node_id => $node) {
				stop($node);
			}
			$cmd = 'rm -rf "/opt/unetlab/tmp/'.$tenant.'/'.$lab -> getId().'/"';
			exec($cmd, $o, $rc);
			if ($rc !== 0) {
				error_log('ERROR: '.$GLOBALS['messages'][13]);
				error_log(implode("\n", $o));
				exit(13);
			}
		}
		break;
}
exit(0);
?>
