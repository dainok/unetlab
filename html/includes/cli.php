<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/cli.php
 *
 * Various functions for UNetLab CLI handler.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/**
 * Function to create a bridge
 *
 * @param   string  $s                  Bridge name
 * @return  int                         0 means ok
 */
function addBridge($s) {
	$cmd = 'brctl addbr '.$s['name'].' 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to add the bridge
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80026]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return 80026;
	}

	$cmd = 'ip link set dev '.$s['name'].' up 2>&1';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to activate it
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80027]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return 80027;
	}

	if (!preg_match('/^pnet[0-9]+$/', $s['name'])) {
		// Forward all frames on non-cloud bridges
		$cmd = 'echo 65535 > /sys/class/net/'.$s['name'].'/bridge/group_fwd_mask 2>&1';
		exec($cmd, $o, $rc);
		if ($rc != 0) {
			// Failed to configure forward mask
			error_log(date('M d H:i:s ').'ERROR: '.$cmd." --- ".$GLOBALS['messages'][80028]);
			error_log(date('M d H:i:s ').implode("\n", $o));
			return 80028;
		}

		// Disable multicast_snooping
		$cmd = 'echo 0 > /sys/devices/virtual/net/'.$s['name'].'/bridge/multicast_snooping 2>&1';
		exec($cmd, $o, $rc);
		if ($rc != 0) {
			// Failed to configure multicast_snooping
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80071]);
			error_log(date('M d H:i:s ').implode("\n", $o));
			return 80071;
		}
	} 
	if ( $s['count'] < 3 ) {
	        $cmd = 'brctl setageing '.$s['name'].' 0 2>&1';
                exec($cmd, $o, $rc);
                if ($rc != 0) {
                        error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80055]);
                        error_log(date('M d H:i:s ').implode("\n", $o));
                        return 80055;
                }
                $cmd = 'echo 2 > /sys/class/net/'.$s['name'].'/bridge/multicast_router  2>&1';
                exec($cmd, $o, $rc);
                if ($rc != 0) {
                        error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80055]);
                        error_log(date('M d H:i:s ').implode("\n", $o));
                        return 80055;
                }
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80021]);
		return 80021;
	}

	switch ($p['type']) {
		default:
			if (in_array($p['type'], listClouds())) {
				// Cloud already exists
			} else if (preg_match('/^pnet[0-9]+$/', $p['type'])) {
				// Cloud does not exist
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80056]);
				return 80056;
			} else {
				// Should not be here
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80020]);
				return 80020;
			}
			break;
		case 'bridge':
			if (!isInterface($p['name'])) {
				// Interface does not exist -> create bridge
				return addBridge($p);
			} else if (isBridge($p['name'])) {
				// Bridge already present
				return 0;
			} else if (isOvs($p['name'])) {
				// OVS exists -> delete it and add bridge
				$rc = delOvs($p['name']);
				if ($rc == 0) {
					// OVS deleted, create the bridge
					return addBridge($p);
				} else {
					// Failed to delete OVS
					return $rc;
				}
			} else {
				// Non bridge/OVS interface exist -> cannot create
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80022]);
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
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80022]);
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
	if ($rc != 0) {
		// Failed to add the OVS
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80023]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return 80023;
	}
	// ADD BPDU CDP option
	$cmd = "ovs-vsctl set bridge ".$s." other-config:forward-bpdu=true";
	exec($cmd, $o, $rc);
        if ($rc == 0) {
                return 0;
        } else {
                // Failed to add  OVS OPTION
                error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80023]);
                error_log(date('M d H:i:s ').implode("\n", $o));
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
	error_log(date('M d H:i:s ').'INFO: '.$cmd);
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to add the TAP interface
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80032]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return 80032;
	}

	$cmd = 'ip link set dev '.$s.' up 2>&1';
	exec($cmd, $o, $rc); 
	if ($rc != 0) {
		// Failed to activate the TAP interface
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80033]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return 80033;
	}

	$cmd = 'ip link set dev '.$s.' mtu 9000';
	exec($cmd, $o, $rc); 
	if ($rc != 0) {
		// Failed to activate the TAP interface
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80085]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return 80085;
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
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80009]);
			error_log(date('M d H:i:s ').implode("\n", $o));
			return False;
		}
	}

	// Now check if the home directory exists
	if (!is_dir($path) && !mkdir($path)) {
		// Failed to create the home directory
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80010]);
		return False;
	}

	// Be sure of the setgid bit
	$cmd = 'chmod 2775 '.$path;
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		// Failed to set the setgid bit
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80011]);
		error_log(date('M d H:i:s ').implode("\n", $o));
		return False;
	}

	// Set permissions
	if (!chown($path, 'unl'.$i)) {
		// Failed to set owner and/or group
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80012]);
		return False;
	}

	// Last, link the profile
	if (!file_exists($path.'/.profile') && !symlink('/opt/unetlab/wrappers/unl_profile', $path.'/.profile')) {
		// Failed to link the profile
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80013]);
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
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80030]);
			error_log(date('M d H:i:s ').implode("\n", $o));
			return 80030;
		}
	} else if (isOvs($n)) {
		$cmd = 'ovs-vsctl add-port '.$n.' '.$p.' 2>&1';
		exec($cmd, $o, $rc);
		if ($rc == 0) {
			return 0;
		} else {
			// Failed to add interface to OVS
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80031]);
			error_log(date('M d H:i:s ').implode("\n", $o));
			return 80031;
		}
	} else {
		// Network not found
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80029]);
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80025]);
		error_log(date('M d H:i:s ').implode("\n", $o));
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80024]);
		error_log(date('M d H:i:s ').implode("\n", $o));
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
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80034]);
			error_log(date('M d H:i:s ').implode("\n", $o));
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
 * @return  bool                        true if config dumped
 */
function dumpConfig($config_data, $file_path) {
	$fp = fopen($file_path, 'w');
	if (!isset($fp)) {
		// Cannot open file
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80068]);
		return False;
	}

	if (!fwrite($fp, $config_data)) {
		// Cannot write file
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80069]);
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80059]);
		return 80059;
	}

	switch ($n -> getNType()) {
		default:
			// Unsupported
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80061]);
			return 80061;
			break;
		case 'dynamips':
			foreach (scandir($n -> getRunningPath()) as $filename) {
				if (preg_match('/_nvram$/', $filename)) {
					$nvram = $n -> getRunningPath().'/'.$filename;
					break;
				} else if (preg_match('/_rom$/', $filename)) {
					$nvram = $n -> getRunningPath().'/'.$filename;
					break;
				}
			}

			if (!isset($nvram) || !is_file($nvram)) {
				// NVRAM file not found
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80066]);
				return 80066;
			}
			$cmd='/opt/unetlab/scripts/wrconf_dyn.py -p '.$n -> getPort().' -t 15';
			exec($cmd, $o, $rc);
			error_log(date('M d H:i:s ').'INFO: force write configuration '.$cmd);
			if ($rc != 0) {
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80060]);
				error_log(date('M d H:i:s ').(string) $o);
				return 80060;
			}
			$cmd = '/usr/bin/nvram_export '.$nvram.' '.$tmp;
			exec($cmd, $o, $rc);
			error_log(date('M d H:i:s ').'INFO: exporting '.$cmd);
			if ($rc != 0) {
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80060]);
				error_log(date('M d H:i:s ').(string) $o);
				return 80060;
			}
			break;
		case 'vpcs':
			if (!is_file($n->getRunningPath().'/startup.vpc')) {
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80062]);
			} else {
				copy($n->getRunningPath().'/startup.vpc',$tmp);
			}
			break;
		case 'iol':
			$nvram = $n -> getRunningPath().'/nvram_'.sprintf('%05u', $node_id);
			if (!is_file($nvram)) {
				// NVRAM file not found
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80066]);
				return 80066;
			}
                        $cmd='/opt/unetlab/scripts/wrconf_iol.py -p '.$n -> getPort().' -t 15';
                        exec($cmd, $o, $rc);
                        error_log(date('M d H:i:s ').'INFO: force write configuration '.$cmd);
                        if ($rc != 0) {
                                error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80060]);
                                error_log(date('M d H:i:s ').(string) $o);
                                return 80060;
                        }
			$cmd = '/opt/unetlab/scripts/iou_export '.$nvram.' '.$tmp;
			exec($cmd, $o, $rc);
			usleep(1);
			error_log(date('M d H:i:s ').'INFO: exporting '.$cmd);
			if ($rc != 0) {
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80060]);
				error_log(date('M d H:i:s ').implode("\n", $o));
				return 80060;
			}
			// Add no shut
			if (is_file($tmp)) file_put_contents($tmp,preg_replace('/(\ninterface.*)/','$1'.chr(10).' no shutdown',file_get_contents($tmp)));
			break;
		case 'qemu':
			if ($n -> getStatus() < 2 || !isset($GLOBALS['node_config'][$n -> getTemplate()])) {
				// Skipping powered off nodes or unsupported nodes
				error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][80084]);
				return 80084;
			} else {
				$cmd = '/opt/unetlab/scripts/'.$GLOBALS['node_config'][$n -> getTemplate()].' -a get -p '.$n -> getPort().' -f '.$tmp.' -t 15';
				exec($cmd, $o, $rc);
				error_log(date('M d H:i:s ').'INFO: exporting '.$cmd);
				if ($rc != 0) {
					error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80060]);
					error_log(date('M d H:i:s ').implode("\n", $o));
					return 80060;
				}
				// Add no shut
				if ( ( $n->getTemplate() == "crv" || $n->getTemplate() == "vios" || $n->getTemplate() == "viosl2" || $n->getTemplate() == "xrv" ) && is_file($tmp) ) file_put_contents($tmp,preg_replace('/(\ninterface.*)/','$1'.chr(10).' no shutdown',file_get_contents($tmp)));
			}
	}

	if (!is_file($tmp)) {
		// File not found
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80062]);
		return 80062;
	}

	// Now save the config file within the lab
	clearstatcache();
	$fp = fopen($tmp, 'r');
	if (!isset($fp)) {
		// Cannot open file
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80064]);
		return 80064;
	}
	$config_data = fread($fp ,filesize($tmp));
	if ($config_data === False || $config_data === ''){
		// Cannot read file
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80065]);
		return 80065;
	}
	
	if ($lab -> setNodeConfigData($node_id, $config_data) !== 0) {
		// Failed to save startup-config
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80063]);
		return 80063;
	}

	if(!unlink($tmp)) {
		// Failed to remove tmp file
		error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][80070]);
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
	if (preg_match('/8000/', $o[1])) {
		// "brctl show" on a ovs bridge or on a non-existent bridge return 0 -> check for 8000
		return True;
	} else {
		return False;
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80036]);
		return 80036;
	}

	// Transition fix: mark the node as prepared (TODO)
	if (is_dir($n -> getRunningPath())) !touch($n -> getRunningPath().'/.prepared');

	if (!is_file($n -> getRunningPath().'/.prepared') && !is_file($n -> getRunningPath().'/.lock')) {

		// Node is not prepared/locked
		if (!is_dir($n -> getRunningPath()) && !mkdir($n -> getRunningPath(), 0775, True)) {
			// Cannot create running directory
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80037]);
			return 80037;
		}

		switch ($n -> getNType()) {
			default:
				// Invalid node_type
				error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80038]);
				return 80038;
			case 'iol':
				// Check license
				if (!is_file('/opt/unetlab/addons/iol/bin/iourc')) {
					// IOL license not found
					error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80039]);
					return 80039;
				}

				if (!file_exists($n -> getRunningPath().'/iourc') && !symlink('/opt/unetlab/addons/iol/bin/iourc', $n -> getRunningPath().'/iourc')) {
					// Cannot link IOL license
					error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80040]);
					return 80040;
				}

				break;
			case 'docker':
				if (!is_file('/usr/bin/docker')) {
					// docker.io is not installed
					error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80082]);
					return 80082;
				}

				$cmd = 'docker -H=tcp://127.0.0.1:4243 inspect --format="{{ .State.Running }}" '.$n -> getUuid();
				exec($cmd, $o, $rc);
				if ($rc != 0) {
					// Must create docker.io container
					$cmd = 'docker -H=tcp://127.0.0.1:4243 create -ti --net=none --name='.$n -> getUuid().' -h '.$n -> getName().' '.$n -> getImage();
					exec($cmd, $o, $rc);
					if ($rc != 0) {
						// Failed to create container
						error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80083]);
						return 80083;
					}
				}
				break;
			case 'vpcs':
				if (!is_file('/opt/vpcsu/bin/vpcs')) {
                                        error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80088]);
                                        return 80082;
                                }
				break;
			case 'dynamips':
				// Nothing to do
				break;
			case 'qemu':
				$image = '/opt/unetlab/addons/qemu/'.$n -> getImage();

				if (!touch($n -> getRunningPath().'/.lock')) {
					// Cannot lock directory
					error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80041]);
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
							error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80045]);
							error_log(date('M d H:i:s ').implode("\n", $o));
							return 80045;
						}
					}

				}

				if (!unlink($n -> getRunningPath().'/.lock')) {
					// Cannot unlock directory
					error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80042]);
					return 80042;
				}
				break;
		}

		if ($n -> getConfig() == '1' && $n -> getConfigData() != '') {
			// Node should use saved startup-config
			if (!dumpConfig($n -> getConfigData(), $n -> getRunningPath().'/startup-config')) {
				// Cannot dump config to startup-config file
				error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][80067]);
			} else {
				switch ($n -> getTemplate()) {
					default:
						break;
					case 'xrv':
						copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/iosxr_config.txt');
						$isocmd = 'mkisofs -o '.$n -> getRunningPath().'/config.iso -l --iso-level 2 '.$n -> getRunningPath().'/iosxr_config.txt' ;
						exec($isocmd, $o, $rc);
						break;
					case 'csr1000v':
						copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/iosxe_config.txt');
	                                        $isocmd = 'mkisofs -o '.$n -> getRunningPath().'/config.iso -l --iso-level 2 '.$n -> getRunningPath().'/iosxe_config.txt' ;
        	                                exec($isocmd, $o, $rc);
						break;
					case 'asav':
						copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/day0-config');
						$isocmd = 'mkisofs -r -o '.$n -> getRunningPath().'/config.iso -l --iso-level 2 '.$n -> getRunningPath().'/day0-config' ;
						exec($isocmd, $o, $rc);
						break;
                                        case 'titanium':
                                                copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/nxos_config.txt');
                                                $isocmd = 'mkisofs -o '.$n -> getRunningPath().'/config.iso -l --iso-level 2 '.$n -> getRunningPath().'/nxos_config.txt' ;
                                                exec($isocmd, $o, $rc);
                                                break;
					case 'vios':
					case 'viosl2':
						copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/ios_config.txt');
	                                        $diskcmd = '/opt/unetlab/scripts/createdosdisk.sh '.$n -> getRunningPath() ;
        	                                exec($diskcmd, $o, $rc);
						break;
					case 'vsrxng':
					case 'vmx':
					case 'vsrx':
						copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/juniper.conf');
						$isocmd = 'mkisofs -o '.$n -> getRunningPath().'/config.iso -l --iso-level 2 '.$n -> getRunningPath().'/juniper.conf' ;
						exec($isocmd, $o, $rc);
                                                break;
					case 'veos':
						$diskcmd = '/opt/unetlab/scripts/veos_diskmod.sh '.$n -> getRunningPath() ;
						exec($diskcmd, $o, $rc);
						break;
					case 'vpcs':
						copy ($n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/startup.vpc');
						break;
					case 'pfsense':
						copy (  $n -> getRunningPath().'/startup-config',  $n -> getRunningPath().'/config.xml');
						$isocmd = 'mkisofs -o '.$n -> getRunningPath().'/config.iso -l --iso-level 2 '.$n -> getRunningPath().'/config.xml' ;
						exec($isocmd, $o, $rc);
						break;
				}
			}
		}
		// Mark the node as prepared
		if (!touch($n -> getRunningPath().'/.prepared')) {
			// Cannot write on directory
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80044]);
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
 * @param   int     $scripttimeout      Config Script Timeout
 * @return  int                         0 means ok
 */
function start($n, $id, $t, $nets, $scripttimeout) {
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
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80046]);
		return 80046;
	}

	if(!chdir($n -> getRunningPath())) {
		// Failed to change directory
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80047]);
		return 80047;
	}

	// Starting the node
	switch ($n -> getNType()) {
		default:
			// Invalid node_type
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80038]);
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
		case 'docker':
			$cmd = 'docker -H=tcp://127.0.0.1:4243 start '.$n -> getUuid();
			break;
		case 'vpcs':
			$cmd ='/opt/vpcsu/bin/vpcs -m '.$id.' -N '.$n -> getName();
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
	// Special Case for xrv - csr1000v - vIOS - vIOSL - Docker
	if (( $n->getTemplate() == 'xrv' || $n->getTemplate() == 'csr1000v' || $n->getTemplate() == 'asav' || $n->getTemplate() == 'titanium' )  && is_file($n -> getRunningPath().'/config.iso') && !is_file($n -> getRunningPath().'/.configured') && $n -> getConfig() != 0)  {
		$flags .= ' -cdrom config.iso' ;
        }

	if (( $n->getTemplate() == 'vios'  || $n->getTemplate() == 'viosl2') && is_file($n -> getRunningPath().'/minidisk') && !is_file($n -> getRunningPath().'/.configured') && $n -> getConfig() != 0)  {
		$flags .= ' -drive file=minidisk,if=virtio,bus=0,unit=1,cache=none' ;
	}

	if (( $n->getTemplate() == 'vmx'  || $n->getTemplate() == 'vsrx') && is_file($n -> getRunningPath().'/config.iso') && !is_file($n -> getRunningPath().'/.configured') && $n -> getConfig() != 0)  {
		$flags .= ' -drive file=config.iso,if=virtio,media=cdrom,index=2' ;
	}

        if ((  $n->getTemplate() == 'vsrxng') && is_file($n -> getRunningPath().'/config.iso') && !is_file($n -> getRunningPath().'/.configured') && $n -> getConfig() != 0)  {
                $flags .= ' -drive file=config.iso,if=ide,media=cdrom,index=2' ;
        }

	if (( $n -> getTemplate() == 'pfsense')   && is_file($n -> getRunningPath().'/config.iso') && !is_file($n -> getRunningPath().'/.configured') && $n -> getConfig() != 0)  {
		$flags .= ' -cdrom config.iso' ;
	}

	if ( $n -> getNType() != 'docker' && $n -> getNType() != 'vpcs')  {
		$cmd .= ' -- '.$flags.' > '.$n -> getRunningPath().'/wrapper.txt 2>&1 &';
	}

	if ( $n -> getNType() == 'vpcs')  {
		$cmd .= $flags.' > '.$n -> getRunningPath().'/wrapper.txt 2>&1 &';
	}
	

	error_log(date('M d H:i:s ').'INFO: CWD is '.getcwd());
	error_log(date('M d H:i:s ').'INFO: starting '.$cmd);
	exec($cmd, $o, $rc);

	if ($rc == 0 && $n -> getNType() == 'qemu' && is_file($n -> getRunningPath().'/startup-config') && !is_file($n -> getRunningPath().'/.configured') && $n -> getConfig() != 0 ) {
		// Start configuration process or check if bootstrap is done
		touch($n -> getRunningPath().'/.lock');
		$cmd = 'nohup /opt/unetlab/scripts/config_'.$n -> getTemplate().'.py -a put -p '.$n -> getPort().' -f '.$n -> getRunningPath().'/startup-config -t '.($n -> getDelay() + $scripttimeout).' > /dev/null 2>&1 &';
		exec($cmd, $o, $rc);
		error_log(date('M d H:i:s ').'INFO: importing '.$cmd);
	}

	if ($rc == 0 && $n -> getNType() == 'docker') {
		// Need to configure each interface
		foreach ($n -> getEthernets() as $interface_id => $interface) {
			// TODO must check each step against errors
			// ip link add docker3_4_5 type veth peer name vnet3_4_5
			$cmd = 'ip link add docker'.$t.'_'.$id.'_'.$interface_id.' type veth peer name vnet'.$t.'_'.$id.'_'.$interface_id;
			error_log(date('M d H:i:s ').'INFO: starting '.$cmd);
			exec($cmd, $o, $rc);
			// ip link set dev vnet3_4_5 up
			$cmd = 'ip link set dev vnet'.$t.'_'.$id.'_'.$interface_id.' up';
			error_log(date('M d H:i:s ').'INFO: starting '.$cmd);
			exec($cmd, $o, $rc);
			// brctl addif vnet0_1 vnet3_4_5
			$cmd = 'brctl addif vnet'.$t.'_'.$interface -> getNetworkId().'  vnet'.$t.'_'.$id.'_'.$interface_id;
			error_log(date('M d H:i:s ').'INFO: starting '.$cmd);
			exec($cmd, $o, $rc);
			// PID=$(docker inspect --format '{{ .State.Pid }}' docker3_4) # Must be greater than 0
			$cmd = 'docker -H=tcp://127.0.0.1:4243 inspect --format "{{ .State.Pid }}" '.$n -> getUuid();
			error_log(date('M d H:i:s ').'INFO: starting '.$cmd);
			exec($cmd, $o, $rc);
			// ip link set netns ${PID} docker3_4_5 name eth0 address 22:ce:e0:99:04:05 up
			$cmd = 'ip link set netns '.$o[1].' docker'.$t.'_'.$id.'_'.$interface_id.' name eth0 address '.'50:'.sprintf('%02x', $t).':'.sprintf('%02x', $id / 512).':'.sprintf('%02x', $id % 512).':00:'.sprintf('%02x', $interface_id).' up';
			error_log(date('M d H:i:s ').'INFO: starting '.$cmd);
			exec($cmd, $o, $rc);
			// /opt/unetlab/wrappers/nsenter -t ${PID} -n ip addr add 1.1.1.1/24 dev eth0
			// /opt/unetlab/wrappers/nsenter -t ${PID} -n ip route add default via 1.1.1.254
		}

		// Start configuration process
		touch($n -> getRunningPath().'/.lock');
		$cmd = 'nohup /opt/unetlab/scripts/config_'.$n -> getTemplate().'.py -a put -i '.$n -> getUuid().' -f '.$n -> getRunningPath().'/startup-config -t '.($n -> getDelay() + 300).' > /dev/null 2>&1 &';
		exec($cmd, $o, $rc);
		error_log(date('M d H:i:s ').'INFO: importing '.$cmd);
	}

	return 0;
}

/**
 * Function to stop a node.
 *
 * @param   Node    $n                  Node
 * @return  int                         0 means ok
 */
function stop($n) {
	if ($n -> getStatus() != 0) {
		if ($n -> getNType() == 'docker') {
			$cmd = 'docker -H=tcp://127.0.0.1:4243 stop '.$n -> getUuid();
		} else {
			$cmd = 'fuser -n tcp -k -TERM '.$n -> getPort().' > /dev/null 2>&1';
		}
		error_log(date('M d H:i:s ').'INFO: stopping '.$cmd);
		exec($cmd, $o, $rc);
		if ($rc  == 0) {
			return 0;
		} else {
			// Node is still running
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][80035]);
			error_log(date('M d H:i:s ').implode("\n", $o));
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
	$output .= "           - start: start one or all nodes\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "           - stop: stop one or all nodes\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "           - wipe: wipe one or all nodes\n";
	$output .= "                     requires -T, -F, -D is optional\n";
	$output .= "Options:\n";
	$output .= "-F <n>     Lab file\n";
	$output .= "-T <n>     Tenant ID\n";
	$output .= "-D <n>     Device ID (if not used, all devices will be impacted)\n";
	print($output);
}
?>

