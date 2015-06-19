<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/cli.php
 *
 * Various functions for UNetLab CLI handler.
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
 * @version 20150527
 */

/**
 * Function to create a bridge
 *
 * @param   string  $s                  Bridge name
 * @return  int                         0 means ok
 */
function addBridge($s) {
	$cmd = 'brctl addbr '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to add the bridge
		error_log('ERROR: '.$GLOBALS['messages'][80026]);
		error_log(implode("\n", $o));
		return 80026;
	}

	$cmd = 'ip link set dev '.$s.' up 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to activate it
		error_log('ERROR: '.$GLOBALS['messages'][80027]);
		error_log(implode("\n", $o));
		return 80027;
	}

	if (!preg_match('/^pnet[0-9]+$/', $s)) {
		// Forward all frames on non-cloud bridges
		$cmd = 'echo 65535 > /sys/class/net/'.$s.'/bridge/group_fwd_mask 2>&1';
		exec($cmd, $o, $rc);
		if ($rc != 0) {
			// Failed to configure forward mask
			error_log('ERROR: '.$GLOBALS['messages'][80028]);
			error_log(implode("\n", $o));
			return 80028;
		}
	}

	$cmd = 'brctl setageing '.$s.' 0 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to set ageing on bridge (need for portmirroring)
		error_log('ERROR: '.$GLOBALS['messages'][80055]);
		error_log(implode("\n", $o));
		return 80055;
	}
	return 0;
}

/**
 * Function to stop a node.
 *
 * @param   Array   $p                  Parameters
 * @return  int                         0 means ok
 */
function addNetwork($p) {
	if (!isset($p['name']) || !isset($p['type'])) {
		// Missing mandatory parameters
		error_log('ERROR: '.$GLOBALS['messages'][80021]);
		return 80021;
	}

	switch ($p['type']) {
		default:
			if (in_array($p['type'], listClouds())) {
				// Cloud already exists
			} else if (preg_match('/^pnet[0-9]+$/', $p['type'])) {
				// Cloud does not exist
				error_log('ERROR: '.$GLOBALS['messages'][80056]);
				return 80056;
			} else {
				// Should not be here
				error_log('ERROR: '.$GLOBALS['messages'][80020]);
				return 80020;
			}
			break;
		case 'bridge':
			if (!isInterface($p['name'])) {
				// Interface does not exist -> create bridge
				return addBridge($p['name']);
			} else if (isBridge($p['name'])) {
				// Bridge already present
				return 0;
			} else if (isOvs($p['name'])) {
				// OVS exists -> delete it and add bridge
				$rc = delOvs($p['name']);
				if ($rc == 0) {
					// OVS deleted, create the bridge
					return addBridge($p['name']);
				} else {
					// Failed to delete OVS
					return $rc;
				}
			} else {
				// Non bridge/OVS interface exist -> cannot create
				error_log('ERROR: '.$GLOBALS['messages'][80022]);
				return 80022;
			}
			break;
		case 'ovs':
			if (!isInterface($p['name'])) {
				// Interface does not exist -> create OVS
				return addOvs($p['name']);
			} else if (isOvs($p['name'])) {
				// OVS already present
				return 0;
			} else if (isBridge($p['name'])) {
				// Bridge exists -> delete it and add OVS
				$rc = delBridge($p['name']);
				if ($rc == 0) {
					// Bridge deleted, create the OVS
					return addOvs($p['name']);
				} else {
					// Failed to delete Bridge
					return $rc;
				}
			} else {
				// Non bridge/OVS interface exist -> cannot create
				error_log('ERROR: '.$GLOBALS['messages'][80022]);
				return 80022;
			}
			break;
	}
	return 0;
}

/*
 * Function to create an OVS
 *
 * @param   string  $s                  OVS name
 * @return  int                         0 means ok
 */
function addOvs($s) {
	$cmd = 'ovs-vsctl add-br '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return 0;
	} else {
		// Failed to add the OVS
		error_log('ERROR: '.$GLOBALS['messages'][80023]);
		error_log(implode("\n", $o));
		return 80023;
	}
}

/**
 * Function to create a TAP interface
 *
 * @param   string  $s                  Network name
 * @return  int                         0 means ok
 */
function addTap($s, $u) {
	// TODO if already exist should fail?
	$cmd = 'tunctl -u '.$u.' -g root -t '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to add the TAP interface
		error_log('ERROR: '.$GLOBALS['messages'][80032]);
		error_log(implode("\n", $o));
		return 80032;
	}

	$cmd = 'ip link set dev '.$s.' up 2>&1';
	exec($cmd, $o, $rc); 
	if ($rc != 0) {
		// Failed to activate the TAP interface
		error_log('ERROR: '.$GLOBALS['messages'][80033]);
		error_log(implode("\n", $o));
		return 80033;
	}

	return 0;
}

/**
 * Function to check if a tenant has a valid username.
 *
 * @param   int     $i                  Tenant ID
 * @return  bool                        True if valid
 */
function checkUsername($i) {
	if ((int) $i < 0) {
		// Tenand ID is not valid
		return False;
	} else {
		// Just to be sure
		$i = (int) $i;
	}

	$path = '/opt/unetlab/tmp/'.$i;
	$uid = 32768 + $i;

	$cmd = 'id unl'.$i.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Need to add the user
		$cmd = '/usr/sbin/useradd -c "Unified Networking Lab TID='.$i.'" -d '.$path.' -g unl -M -s /bin/bash -u '.$uid.' unl'.$i.' 2>&1';
		exec($cmd, $o, $rc);
		if ($rc != 0) {
			// Failed to add the username
			error_log('ERROR: '.$GLOBALS['messages'][80009]);
			error_log(implode("\n", $o));
			return False;
		}
	}

	// Now check if the home directory exists
	if (!is_dir($path) && !mkdir($path)) {
		// Failed to create the home directory
		error_log('ERROR: '.$GLOBALS['messages'][80010]);
		return False;
	}

	// Be sure of the setgid bit
	$cmd = 'chmod 2775 '.$path;
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to set the setgid bit
		error_log('ERROR: '.$GLOBALS['messages'][80011]);
		error_log(implode("\n", $o));
		return False;
	}

	// Set permissions
	if (!chown($path, 'unl'.$i)) {
		// Failed to set owner and/or group
		error_log('ERROR: '.$GLOBALS['messages'][80012]);
		return False;
	}

	// Last, link the profile
	if (!file_exists($path.'/.profile') && !symlink('/opt/unetlab/wrappers/unl_profile', $path.'/.profile')) {
		// Failed to link the profile
		error_log('ERROR: '.$GLOBALS['messages'][80013]);
		return False;
	}

	return True;
}

/**
 * Function to connect an interface (TAP) to a network (Bridge/OVS)
 *
 * @param   string  $n                  Network name
 * @param   string  $p                  Interface name
 * @return  int                         0 means ok
 */
function connectInterface($n, $p) {
	if (isBridge($n)) {
		$cmd = 'brctl addif '.$n.' '.$p.' 2>&1';
		exec($cmd, $o, $rc);
		if ($rc == 0) {
			return 0;
		} else {
			// Failed to add interface to Bridge
			error_log('ERROR: '.$GLOBALS['messages'][80030]);
			error_log(implode("\n", $o));
			return 80030;
		}
	} else if (isOvs($n)) {
		$cmd = 'ovs-vsctl add-port '.$n.' '.$p.' 2>&1';
		exec($cmd, $o, $rc);
		if ($rc == 0) {
			return 0;
		} else {
			// Failed to add interface to OVS
			error_log('ERROR: '.$GLOBALS['messages'][80031]);
			error_log(implode("\n", $o));
			return 80031;
		}
	} else {
		// Network not found
		error_log('ERROR: '.$GLOBALS['messages'][80029]);
		return 80029;
	}
}

/**
 * Function to delete a bridge
 *
 * @param   string  $s                  Bridge name
 * @return  int                         0 means ok
 */
function delBridge($s) {
	// Need to deactivate it
	$cmd = 'ip link set dev '.$s.' down 2>&1';
	exec($cmd, $o, $rc); 

	$cmd = 'brctl delbr '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return 0;
	} else {
		// Failed to delete the OVS
		error_log('ERROR: '.$GLOBALS['messages'][80025]);
		error_log(implode("\n", $o));
		return 80025;
	}
}

/**
 * Function to delete an OVS
 *
 * @param   string  $s                  OVS name
 * @return  int                         0 means ok
 */
function delOvs($s) {
	$cmd = 'ovs-vsctl del-br '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return 0;
	} else {
		// Failed to delete the OVS
		error_log('ERROR: '.$GLOBALS['messages'][80024]);
		error_log(implode("\n", $o));
		return 80024;
	}
}

/**
 * Function to delete a TAP interface
 *
 * @param   string  $s                  Interface name
 * @return  int                         0 means ok
 */
function delTap($s) {
	if (isInterface($s)) {
		// Remove interface from OVS switches
		$cmd = 'ovs-vsctl del-port '.$s.' 2>&1';
		exec($cmd, $o, $rc);

		// Delete TAP (so it's removed from bridges too)
		$cmd = 'tunctl -d '.$s.' 2>&1';
		exec($cmd, $o, $rc);
		if (isInterface($s)) {
			// Failed to delete the TAP interface
			error_log('ERROR: '.$GLOBALS['messages'][80034]);
			error_log(implode("\n", $o));
			return 80034;
		} else {
			return 0;
		}
	} else {
		// Interface does not exist
		return 0;
	}
}

/**
 * Function to push startup-config to a file
 *
 * @param   string  $config_data        The startup-config
 * @param   string  $file_path          File with full path where config is stored
 * @return  bool                        true if configured
 */
function dumpConfig($config_data, $file_path) {
	$fp = fopen($file_path, 'w');
	if (!isset($fp)) {
		// Cannot open file
		error_log('ERROR: '.$GLOBALS['messages'][80068]);
		return False;
	}

	if (!fwrite($fp, $config_data)) {
		// Cannot write file
		error_log('ERROR: '.$GLOBALS['messages'][80069]);
		return False;
	}

    return True;
}

/**
 * Function to export a node running-config.
 *
 * @param   int     $node_id            Node ID
 * @param   Node    $n                  Node
 * @param   Lab     $lab                Lab
 * @return  int                         0 means ok
 */
function export($node_id, $n, $lab) {
	$tmp = tempnam(sys_get_temp_dir(), 'unl_cfg_'.$node_id.'_');

	if (is_file($tmp) && !unlink($tmp)) {
		// Cannot delete tmp file
		error_log('ERROR: '.$GLOBALS['messages'][80059]);
		return 80059;
	}

	switch ($n -> getNType()) {
		default:
			// Unsupported
			error_log('ERROR: '.$GLOBALS['messages'][80061]);
			return 80061;
			break;
		case 'dynamips':
			foreach (scandir($n -> getRunningPath()) as $filename) {
				if (preg_match('/_nvram$/', $filename)) {
					$nvram = $n -> getRunningPath().'/'.$filename;
				}
			}

			if (!isset($nvram) || !is_file($nvram)) {
				// NVRAM file not found
				error_log('ERROR: '.$GLOBALS['messages'][80066]);
				return 80066;
			}
			$cmd = '/usr/bin/nvram_export '.$nvram.' '.$tmp;
			exec($cmd, $o, $rc);
			error_log('INFO: exporting '.$cmd);
			if ($rc != 0) {
				error_log('ERROR: '.$GLOBALS['messages'][80060]);
				error_log((string) $o);
				return 80060;
			}
			break;
		case 'iol':
			$nvram = $n -> getRunningPath().'/nvram_'.sprintf('%05u', $node_id);
			if (!is_file($nvram)) {
				// NVRAM file not found
				error_log('ERROR: '.$GLOBALS['messages'][80066]);
				return 80066;
			}
			$cmd = '/opt/unetlab/scripts/iou_export '.$nvram.' '.$tmp;
			exec($cmd, $o, $rc);
			error_log('INFO: exporting '.$cmd);
			if ($rc != 0) {
				error_log('ERROR: '.$GLOBALS['messages'][80060]);
				error_log((string) $o);
				return 80060;
			}
			break;
	}

	if (!is_file($tmp)) {
		// File not found
		error_log('ERROR: '.$GLOBALS['messages'][80062]);
		return 80062;
	}

	// Now save the config file within the lab
	$fp = fopen($tmp, 'r');
	if (!isset($fp)) {
		// Cannot open file
		error_log('ERROR: '.$GLOBALS['messages'][80064]);
		return 80064;
	}
	$config_data = fread($fp ,filesize($tmp));
	if ($config_data === False || $config_data === ''){
		// Cannot read file
		error_log('ERROR: '.$GLOBALS['messages'][80065]);
		return 80065;
	}
	
	if ($lab -> setNodeConfigData($node_id, $config_data) !== 0) {
		// Failed to save startup-config
		error_log('ERROR: '.$GLOBALS['messages'][80063]);
		return 80063;
	}

	if(!unlink($tmp)) {
		// Failed to remove tmp file
		error_log('WARNING: '.$GLOBALS['messages'][80070]);
	}

	return 0;
}

/**
 * Function to check if a bridge exists
 *
 * @param   string  $s                  Bridge name
 * @return  bool                        True if exists
 */
function isBridge($s) {
	$cmd = 'brctl show '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if (preg_match('/can\'t get info No such device/', $o[1])) {
		return False;
	} else {
		return True;
	}
}

/**
 * Function to check if a interface exists
 *
 * @param   string  $s                  Interface name
 * @return  bool                        True if exists
 */
function isInterface($s) {
	$cmd = 'ip link show '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if an OVS exists
 *
 * @param   string  $s                  OVS name
 * @return  bool                        True if exists
 */
function isOvs($s) {
	$cmd = 'ovs-vsctl br-exists '.$s.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a node is running.
 *
 * @param   int     $p                  Port
 * @return  bool                        true if running
 */
function isRunning($p) {
	// If node is running, the console port is used
	$cmd = 'fuser -n tcp '.$p.' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc == 0) {
		return True;
	} else {
		return False;
	}
}

/**
 * Function to check if a TAP interface exists
 *
 * @param   string  $s                  Interface name
 * @return  bool                        True if exists
 */
function isTap($s) {
	if (is_dir('/sys/class/net/'.$s)) {
		// TODO can be bridge or OVS
		return True;
	} else {
		return False;
	}
}

/**
 * Function to prepare a node before starging it
 *
 * @param   Node    $n                  The Node
 * @param   Int     $id                 Node ID
 * @param   Int     $t                  Tenant ID
 * @param   Array   $nets               Array of networks
 * @return  int                         0 Means ok
 */
function prepareNode($n, $id, $t, $nets) {
	$user = 'unl'.$t;

	// Get UID from username
	$cmd = 'id -u '.$user.' 2>&1';
	exec($cmd, $o, $rc);
	$uid = $o[0];

	// Creating TAP interfaces
	foreach ($n -> getEthernets() as $interface_id => $interface) {
		$tap_name = 'vunl'.$t.'_'.$id.'_'.$interface_id;
		if (isset($nets[$interface -> getNetworkId()]) && $nets[$interface -> getNetworkId()] -> isCloud()) {
			// Network is a Cloud
			$net_name = $nets[$interface -> getNetworkId()] -> getNType();
		} else {
			$net_name = 'vnet'.$t.'_'.$interface -> getNetworkId();
		}

		// Remove interface
		$rc = delTap($tap_name);
		if ($rc !== 0) {
			// Failed to delete TAP interface
			return $rc;
		}


		// Add interface
		$rc = addTap($tap_name, $user);
		if ($rc !== 0) {
			// Failed to add TAP interface
			return $rc;
		}

		if ($interface -> getNetworkId() !== 0) {
			// Connect interface to network
			$rc = connectInterface($net_name, $tap_name);
			if ($rc !== 0) {
				// Failed to connect interface to network
				return $rc;
			}
		}
	}

	// Preparing image

	// Dropping privileges
	posix_setsid();
	posix_setgid(32768);
	if ($n -> getNType() == 'iol' && !posix_setuid($uid)) {
		error_log('ERROR: '.$GLOBALS['messages'][80036]);
		return 80036;
	}

	if (!is_file($n -> getRunningPath().'/.configured') && !is_file($n -> getRunningPath().'/.lock')) {
		// Node is not configured/locked
		if (!is_dir($n -> getRunningPath()) && !mkdir($n -> getRunningPath(), 0775, True)) {
			// Cannot create running directory
			error_log('ERROR: '.$GLOBALS['messages'][80037]);
			return 80037;
		}

		switch ($n -> getNType()) {
			default:
				// Invalid node_type
				error_log('ERROR: '.$GLOBALS['messages'][80038]);
				return 80038;
			case 'iol':
				// Check license
				if (!is_file('/opt/unetlab/addons/iol/bin/iourc')) {
					// IOL license not found
					error_log('ERROR: '.$GLOBALS['messages'][80039]);
					return 80039;
				}

				if (!file_exists($n -> getRunningPath().'/iourc') && !symlink('/opt/unetlab/addons/iol/bin/iourc', $n -> getRunningPath().'/iourc')) {
					// Cannot link IOL license
					error_log('ERROR: '.$GLOBALS['messages'][80040]);
					return 80040;
				}

				if ($n -> getConfig() == 'Saved') {
					// Node should use saved startup-config
					if (!dumpConfig($n -> getConfigData(), $n -> getRunningPath().'/startup-config')) {
						// Cannot dump config to startup-config file
						error_log('WARNING: '.$GLOBALS['messages'][80067]);
					}
				}
				break;
			case 'dynamips':
				if ($n -> getConfig() == 'Saved') {
					// Node should use saved startup-config
					if (!dumpConfig($n -> getConfigData(), $n -> getRunningPath().'/startup-config')) {
						// Cannot dump config to startup-config file
						error_log('WARNING: '.$GLOBALS['messages'][80067]);
					}
				}
				break;
			case 'qemu':
				$image = '/opt/unetlab/addons/qemu/'.$n -> getImage();

				if (!touch($n -> getRunningPath().'/.lock')) {
					// Cannot lock directory
					error_log('ERROR: '.$GLOBALS['messages'][80041]);
					return 80041;
				}

				// Copy files from template
				foreach(scandir($image) as $filename) {
					if (preg_match('/^[a-zA-Z0-9]+.qcow2$/', $filename)) {
						// TODO should check if file exists
						$cmd = '/opt/qemu/bin/qemu-img create -b "'.$image.'/'.$filename.'" -f qcow2 "'.$n -> getRunningPath().'/'.$filename.'"';
						exec($cmd, $o, $rc);
						if ($rc !== 0) {
							// Cannot make linked clone
							error_log('ERROR: '.$GLOBALS['messages'][80045]);
							error_log(implode("\n", $o));
							return 80045;
						}
					}

				}

				if (!unlink($n -> getRunningPath().'/.lock')) {
					// Cannot unlock directory
					error_log('ERROR: '.$GLOBALS['messages'][80042]);
					return 80042;
				}
				break;
		}

		// Mark the node as configured
		if (!touch($n -> getRunningPath().'/.configured')) {
			// Cannot write on directory
			error_log('ERROR: '.$GLOBALS['messages'][80044]);
			return 80044;
		}

	}

	return 0;
}

/**
 * Function to start a node.
 *
 * @param   Node    $n                  Node
 * @param   Int     $id                 Node ID
 * @param   Int     $t                  Tenant ID
 * @param   Array   $nets               Array of networks
 * @return  int                         0 means ok
 */
function start($n, $id, $t, $nets) {
	if ($n -> getStatus() !== 0) {
		// Node is in running or building state
		return 0;
	}

	$rc = prepareNode($n, $id, $t, $nets);
	if ($rc !== 0) {
		// Failed to prepare the node
		return $rc;
	}

	list($bin, $flags) = $n -> getCommand();

	if ($bin == False || $flags == False) {
		// Invalid CMD line
		error_log('ERROR: '.$GLOBALS['messages'][80046]);
		return 80046;
	}

	if(!chdir($n -> getRunningPath())) {
		// Failed to change directory
		error_log('ERROR: '.$GLOBALS['messages'][80047]);
		return 80047;
	}

	// Starting the node
	switch ($n -> getNType()) {
		default:
			// Invalid node_type
			error_log('ERROR: '.$GLOBALS['messages'][80038]);
			return 80028;
		case 'iol':
			$cmd = '/opt/unetlab/wrappers/iol_wrapper -T '.$t.' -D '.$id.' -t "'.$n -> getName().'" -F /opt/unetlab/addons/iol/bin/'.$n -> getImage().' -d '.$n -> getDelay().' -e '.$n -> getEthernetCount().' -s '.$n -> getSerialCount();
			// Adding Serial links
			foreach ($n -> getSerials() as $interface_id => $interface) {
				if ($interface -> getRemoteId() > 0) {
					$cmd .= ' -l '.$interface_id.':localhost:'.$interface -> getRemoteId().':'.$interface -> getRemoteIf();
				}
			}
			break;
		case 'dynamips':
			$cmd = '/opt/unetlab/wrappers/dynamips_wrapper -T '.$t.' -D '.$id.' -t "'.$n -> getName().'" -F /opt/unetlab/addons/dynamips/'.$n -> getImage().' -d '.$n -> getDelay();
			break;
		case 'qemu':
			$cmd = '/opt/unetlab/wrappers/qemu_wrapper -T '.$t.' -D '.$id.' -t "'.$n -> getName().'" -F '.$bin.' -d '.$n -> getDelay();
			if ($n -> getConsole() == 'vnc') {
				// Disable telnet (wrapper) console
				$cmd .= ' -x';
			}
			break;
	}

	$cmd .= ' -- '.$flags.' > '.$n -> getRunningPath().'/wrapper.txt 2>&1 &';
	exec($cmd, $o, $rc);
	error_log('INFO: CWD is '.getcwd());
	error_log('INFO: starting '.$cmd);

	return 0;
}

/**
 * Function to stop a node.
 *
 * @param   Node    $n                  Node
 * @return  int                         0 means ok
 */
function stop($n) {
	if ($n -> getStatus() == 1) {
		$cmd = 'kill -s TERM $(fuser -n tcp '.$n -> getPort().' 2> /dev/null | sed "s/^.* \([0-9]\+\)$/\1/g")';
		exec($cmd, $o, $rc);
		error_log('INFO: stopping '.$cmd);
		sleep(1);  // Need to wait a few
		if ($n -> getStatus() == 0) {
			return 0;
		} else {
			// Node is still running
			error_log('ERROR: '.$GLOBALS['messages'][80035]);
			error_log(implode("\n", $o));
			return 80035;
		}
	} else {
		return 0;
	}
}

/**
 * Function to print how to use the unl_wrapper
 *
 * @return  string                      usage output
 */
function usage() {
	global $argv;
	$output = '';
	$output .= "Usage: ".$argv[0]." -a <action> <options>\n";
	$output .= "-a <s>     Action can be:\n";
	$output .= "           - delete: delete a lab file even if it's not valid\n";
	$output .= "                     requires -T, -F\n";
	$output .= "           - export: export a runnign-config to a file\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "           - fixpermissions: fix file/dir permissions\n";
	$output .= "           - platform: print the hardware platform\n";
	$output .= "           - start: fix file/dir permissions\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "           - stop: fix file/dir permissions\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "           - wipe: fix file/dir permissions\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "Options:\n";
	$output .= "-F <n>     Lab file\n";
	$output .= "-T <n>     Tenant ID\n";
	$output .= "-D <n>     Device ID (if not used, all devices will be impacted)\n";
	print($output);
}
?>
