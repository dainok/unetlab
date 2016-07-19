#!/usr/bin/env php
<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * scripts/unl_wrapper.php
 *
 * CLI handler for UNetLab
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

require_once('/opt/unetlab/html/includes/init.php');

// Checking if called from CLI or Web
if (php_sapi_name() != 'cli') {
	error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][1]);
	exit(1);
}

// Checking privileges
if (posix_getuid() != 0) {
	error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][2]);
	exit(2);
}

// Setting umask
umask(0002);

// Parsing and checking parameters
$options = getopt('oT:D:F:a:');

// Checking -a (action)
if (!isset($options['a'])) {
	usage();
	error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][3]);
	exit(3);
}
$action = $options['a'];

// Checking -T (Tenant ID)
if (in_array($action, Array('delete', 'export', 'start', 'stop', 'wipe'))) {
	if (!isset($options['T'])) {
		// Tenant ID is missing
		usage();
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][4]);
		exit(4);
	} else if ((int) $options['T'] < 0) {
		// Tenant ID is not valid
		usage();
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][5]);
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
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][6]);
		exit(6);
	}

	try {
		$lab = new Lab($options['F'], $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][$e -> getMessage()]);
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][7]);
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
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][8]);
		exit(8);
	}
}

switch ($action) {
	default:
		// Invalid action
		usage();
		error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][9]);
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
		$cmd = '/usr/bin/find /opt/unetlab -type f -exec chown root:root {} \; > /dev/null 2>&1';
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

		// /tmp
		$cmd = '/bin/chown root:root /tmp 2>&1';
		exec($cmd, $o, $rc);
		$cmd = '/bin/chmod u=rwx,g=rwx,o=rwxt /tmp > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		break;
	case 'stopall':
		// Kill all nodes and clear the system
		$cmd = 'pkill -TERM dynamips_wrapper > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		$cmd = 'pkill -TERM iol_wrapper > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		$cmd = 'pkill -TERM qemu_wrapper > /dev/null 2>&1';
		exec($cmd, $o, $rc);
		$cmd = 'brctl show | grep vnet | sed \'s/^\(vnet[0-9]\+_[0-9]\+\).*/\1/g\' | while read line; do ifconfig $line down; brctl delbr $line; done';
		exec($cmd, $o, $rc);
		$cmd = 'ovs-vsctl list-br | while read line; do ovs-vsctl del-br $line; done';
		exec($cmd, $o, $rc);
		$cmd = 'ifconfig | grep vunl | cut -d\' \' -f1 | while read line; do tunctl -d $line; done';
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
			error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][14]);
			exit(14);
		}

		if (isset($node_id)) {
			// Node ID is set, create attached networks, prepare node and start it

			foreach ($lab -> getNodes()[$node_id] -> getEthernets() as $interface) {
				if ($interface -> getNetworkId() !== 0 && !isset($lab -> getNetworks()[$interface -> getNetworkId()])) {
					// Interface is set but network does not exist
					error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][10]);
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
						error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][$rc]);
						error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][11]);
						exit(11);
					}
				}
			}

			// Starting the node
			$rc = start($lab -> getNodes()[$node_id], $node_id, $tenant, $lab -> getNetworks());
			if ($rc !== 0) {
				// Failed to start the node
				error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][$rc]);
				error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][12]);
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
					error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][$rc]);
					error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][11]);
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
						error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][$rc]);
						error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][12]);
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
						error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][$rc]);
						error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][12]);
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
				error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][13]);
				error_log(date('M d H:i:s ').date('M d H:i:s ').implode("\n", $o));
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
				error_log(date('M d H:i:s ').date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][13]);
				error_log(date('M d H:i:s ').date('M d H:i:s ').implode("\n", $o));
				exit(13);
			}
		}
		break;
}
exit(0);
?>
