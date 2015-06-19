<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/__lab.php
 *
 * Class for UNetLab labs.
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
 * @property type $author Author name of the lab. It's optional.
 * @property type $description Description of the lab. It's optional
 * @property type $filename The filename of the lab (without path). It's mandatory and automatically set.
 * @property type $id UUID of the lab. It's mandatory and automatically set.
 * @property type $name Name of the lab. It's mandatory and part of filename ($filename = $name + '.unl').
 * @property type $networks List of configured networks. It's optional.
 * @property type $nodes List of configured nodes. It's optional.
 * @property type $path Full path of the lab. It's mandatory and automatically set.
 * @property type $pictures List of included pictures. It's optional.
 * @property type $tenant Tenant ID. It's mandatory and set during contruction phase.
 * @property type $version Version of the lab. It's optional.
 */

class Lab {
	private $author;
	private $description;
	private $filename;
	private $id;
	private $name;
	private $networks = array();
	private $nodes = array();
	private $path;
	private $pictures = array();
	private $tenant;
	private $version;

	/**
	 * Constructor which load an existent lab or create an empty one.
	 *
	 * @param	  string  $f                  the file of the lab with full path
	 * @param	  int     $tenant             Tenant ID
	 * @return	  void
	 */
	public function __construct($f, $tenant) {
		$modified = False;

		if (!is_file($f)) {
			// File does not exist, create a new empty lab
			$this -> filename = basename($f);
			$this -> path = dirname($f);
			$this -> tenant = (int) $tenant;

			if (!checkLabFilename($this -> filename)) {
				// Invalid filename
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20001]);
				throw new Exception('20001');
			}

			if (!checkLabPath($this -> path)) {
				// Invalid path
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20002]);
				throw new Exception('20002');
			}

			$this -> name = substr(basename($f), 0, -4);
			$this -> id = genUuid();
			$modified = True;
			error_log('WARNING: '.$f.' '.$GLOBALS['messages'][20000]);
		} else {
			// Load the existent lab
			$this -> filename = basename($f);
			$this -> path = dirname($f);
			$this -> tenant = (int) $tenant;

			if (!checkLabFilename($this -> filename)) {
				// Invalid filename
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20001]);
				throw new Exception('20001');
			}

			if (!checkLabPath($this -> path)) {
				// Invalid path
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20002]);
				throw new Exception('20002');
			}

			libxml_use_internal_errors(true);
			$xml = simplexml_load_file($f);
			if (!$xml) {
				// Invalid XML document
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20003]);
				throw new Exception('20003');
			}

			// Lab name
			$result = $xml -> xpath('//lab/@name');
			if (empty($result)) {
				// Invalid UNetLab file (attribute is missing)
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20004]);
				throw new Exception('20004');
				return;
			} else if (!checkLabName($result[0])) {
				// Attribute not valid
				error_log('ERROR: '.$f.' '.$GLOBALS['messages'][20005]);
				throw new Exception('20005');
				return;
			} else {
				$this -> name = (string) $result[0];
			}

			// Lab ID
			$result = $xml -> xpath('//lab/@id');
			if (empty($result)) {
				// Lab ID not set, create a new one
				$this -> id = genUuid();
				error_log('WARNING: '.$f.' '.$GLOBALS['messages'][20011]);
				$modified = True;
			} else if (!checkUuid($result[0])) {
				// Attribute not valid
				$this -> id = genUuid();
				error_log('WARNING: '.$f.' '.$GLOBALS['messages'][20012]);
				$modified = True;
			} else {
				$this -> id = (string) $result[0];
			}

			// Lab description
			$result = (string) array_pop($xml -> xpath('//lab/description'));
			if (strlen($result) !== 0) {
				$this -> description = htmlspecialchars($result, ENT_DISALLOWED, 'UTF-8', TRUE);
			} else if (strlen($result) !== 0) {
				error_log('WARNING: '.$f.' '.$GLOBALS['messages'][20006]);
			}

			// Lab author
			$result = (string) array_pop($xml -> xpath('//lab/@author'));
			if (strlen($result) !== 0) {
				$this -> author = htmlspecialchars($result, ENT_DISALLOWED, 'UTF-8', TRUE);
			} else if (strlen($result) !== 0) {
				error_log('WARNING: '.$f.' '.$GLOBALS['messages'][20007]);
			}

			// Lab version
			$result = (string) array_pop($xml -> xpath('//lab/@version'));
			if (strlen($result) !== 0 && (int) $result >= 0) {
				$this -> version = $result;
			} else if (strlen($result) !== 0) {
				error_log('WARNING: '.$f.' '.$GLOBALS['messages'][20008]);
			}

			// Lab networks
			foreach ($xml -> xpath('//lab/topology/networks/network') as $network) {
				$w = Array();
				if (isset($network -> attributes() -> id)) $w['id'] = (string) $network -> attributes() -> id;
				if (isset($network -> attributes() -> left)) $w['left'] = (string) $network -> attributes() -> left;
				if (isset($network -> attributes() -> name)) $w['name'] = (string) $network -> attributes() -> name;
				if (isset($network -> attributes() -> top)) $w['top'] = (string) $network -> attributes() -> top;
				if (isset($network -> attributes() -> type)) $w['type'] = (string) $network -> attributes() -> type;

				try {
					$this -> networks[$w['id']] = new Network($w, $w['id'], $this -> tenant);
				} catch (Exception $e) {
					// Invalid network
					error_log('WARNING: '.$f.':net'.$w['id'].' '.$GLOBALS['messages'][20009]);
					error_log((string) $e);
					continue;
				}
			}

			// Lab nodes (networks must be alredy loaded)
			foreach ($xml -> xpath('//lab/topology/nodes/node') as $node_id => $node) {
				$n = Array();
				if (isset($node -> attributes() -> config)) $n['config'] = (string) $node -> attributes() -> config;
				if (isset($node -> attributes() -> console)) $n['console'] = (string) $node -> attributes() -> console;
				if (isset($node -> attributes() -> cpu)) $n['cpu'] = (int) $node -> attributes() -> cpu;
				if (isset($node -> attributes() -> delay)) $n['delay'] = (string) $node -> attributes() -> delay;
				if (isset($node -> attributes() -> ethernet)) $n['ethernet'] = (int) $node -> attributes() -> ethernet;
				if (isset($node -> attributes() -> icon)) $n['icon'] = (string) $node -> attributes() -> icon;
				if (isset($node -> attributes() -> id)) $n['id'] = (int) $node -> attributes() -> id;
				if (isset($node -> attributes() -> idlepc)) $n['idlepc'] = (string) $node -> attributes() -> idlepc;
				if (isset($node -> attributes() -> image)) $n['image'] = (string) $node -> attributes() -> image;
				if (isset($node -> attributes() -> left)) $n['left'] = (string) $node -> attributes() -> left;
				if (isset($node -> attributes() -> name)) $n['name'] = (string) $node -> attributes() -> name;
				if (isset($node -> attributes() -> nvram)) $n['nvram'] = (int) $node -> attributes() -> nvram;
				if (isset($node -> attributes() -> ram)) $n['ram'] = (int) $node -> attributes() -> ram;
				if (isset($node -> attributes() -> serial)) $n['serial'] = (int) $node -> attributes() -> serial;
				if (isset($node -> attributes() -> template)) $n['template'] = (string) $node -> attributes() -> template;
				if (isset($node -> attributes() -> top)) $n['top'] = (string) $node -> attributes() -> top;
				if (isset($node -> attributes() -> type)) $n['type'] = (string) $node -> attributes() -> type;
				if (isset($node -> attributes() -> uuid)) $n['uuid'] = (string) $node -> attributes() -> uuid;

				try {
					$this -> nodes[$n['id']] = new Node($n, $n['id'], $this -> tenant, $this -> id);
				} catch (Exception $e) {
					// Invalid node
					error_log('WARNING: '.$f.':node'.$n['id'].' '.$GLOBALS['messages'][20010]);
					error_log((string) $e);
					continue;
				}

				// Slot must be loaded before interfaces
				foreach ($node -> slot as $slot) {
					// Loading configured slots for this node
					$s = Array();
					if (isset($slot -> attributes() -> id)) $s['id'] = (string) $slot -> attributes() -> id;
					if (isset($slot -> attributes() -> module)) $s['module'] = (string) $slot -> attributes() -> module;
					if ($this -> nodes[$n['id']] -> setSlot($s['id'], $s['module']) !== 0) {
						error_log('WARNING: '.$f.':node'.$n['id'].':slot'.$s['id'].' '.$GLOBALS['messages'][20013]);
					}
				}

				foreach ($node -> interface as $interface) {
					// Loading configured interfaces for this node
					$i = Array();
					if (isset($interface -> attributes() -> id)) $i['id'] = (string) $interface -> attributes() -> id;
					if (isset($interface -> attributes() -> network_id)) $i['network_id'] = (string) $interface -> attributes() -> network_id;
					if (isset($interface -> attributes() -> remote_id)) $i['remote_id'] = (string) $interface -> attributes() -> remote_id;
					if (isset($interface -> attributes() -> remote_if)) $i['remote_if'] = (string) $interface -> attributes() -> remote_if;
					if (isset($interface -> attributes() -> remote_host)) $i['remote_host'] = (string) $interface -> attributes() -> remote_host;
					if (isset($interface -> attributes() -> type)) $i['type'] = (string) $interface -> attributes() -> type;
					switch ($i['type']) {
						default:
							error_log('WARNING: '.$f.':node'.$n['id'].':inv'.$s['id'].' '.$GLOBALS['messages'][20016]);
							break;
						case 'ethernet':
							if ($this -> nodes[$n['id']] -> linkInterface($i) !== 0) {
								error_log('WARNING: '.$f.':node'.$n['id'].':eth'.$i['id'].' '.$GLOBALS['messages'][20014]);
							}
							break;
						case 'serial':
							// Serial
							if ($this -> nodes[$n['id']] -> linkInterface($i) !== 0) {
								error_log('WARNING: '.$f.':node'.$n['id'].':ser'.$i['id'].' '.$GLOBALS['messages'][20015]);
							}
							break;
					}
				}
			}

			// startup-config
			foreach ($xml -> xpath('//lab/objects/configs/config') as $config) {
				$node_id = 0;
				$config_data = '';
				if (isset($config -> attributes() -> id)) $node_id = (string) $config -> attributes() -> id;
				$result = (string) array_pop($config -> xpath('.'));
				if (strlen($result) > 0) $config_data = base64_decode($result);

				$rc = $this -> nodes[$node_id] -> setConfigData($config_data);
				if ($rc != 0) {
					error_log('WARNING: '.$f.':cfg'.$node_id.' '.$GLOBALS['messages'][20037]);
					continue;
				}
			}

			// Lab Pictures
			foreach ($xml -> xpath('//lab/objects/pictures/picture') as $picture) {
				$p = Array();
				if (isset($picture -> attributes() -> id)) $p['id'] = (string) $picture -> attributes() -> id;
				if (isset($picture -> attributes() -> name)) $p['name'] = (string) $picture -> attributes() -> name;
				if (isset($picture -> attributes() -> type)) $p['type'] = (string) $picture -> attributes() -> type;
				$result = (string) array_pop($picture -> xpath('./data'));
				if (strlen($result) > 0) $p['data'] = base64_decode($result);
				$result = (string) array_pop($picture -> xpath('./map'));
				if (strlen($result) > 0) $p['map'] = html_entity_decode($result);

				try {
					$this -> pictures[$p['id']] = new Picture($p, $p['id']);
				} catch (Exception $e) {
					// Invalid picture
					error_log('WARNING: '.$f.':pic'.$p['id'].' '.$GLOBALS['messages'][20020]);
					error_log((string) $e);
					continue;
				}
			}

			// Update attached network count
			$this -> setNetworkCount();
		}

		if ($modified) {
			// Need to save
			$rc = $this -> save();
			if ($rc != 0) {
				throw new Exception($rc);
				return $rc;
			}
		}

		return 0;
	}

	/**
	 * Method to add a new network.
	 *
	 * @param   Array   $p                  Parameters
	 * @return	int	                        0 if OK
	 */
	public function addNetwork($p) {
		$p['id'] = $this -> getFreeNetworkId();

		// Adding the network
		try {
			$this -> networks[$p['id']] = new Network($p, $p['id'], $this -> tenant);
			return $this -> save();
		} catch (Exception $e) {
			// Failed to create the network
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?net='.$p['id'].' '.$GLOBALS['messages'][20021]);
			error_log((string) $e);
			return 20021;
		}
		return 0;
	}

	/**
	 * Method to add a new node.
	 *
	 * @param   Array   $p                  Parameters
	 * @return	int	                        0 if OK
	 */
	public function addNode($p) {
		$p['id'] = $this -> getFreeNodeId();

		// Add the node
		try {
			$this -> nodes[$p['id']] = new Node($p, $p['id'], $this -> tenant, $this -> id);
			return $this -> save();
		} catch (Exception $e) {
			// Failed to create the node
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$p['id'].' '.$GLOBALS['messages'][20022]);
			error_log((string) $e);
			return 20022;
		}
	}

	/**
	 * Method to add a new picture.
	 *
	 * @param   Array   $p                  Parameters
	 * @return	int	                        0 if OK
	 */
	public function addPicture($p) {
		$p['id'] = 1;

		// Finding a free picture ID
		while (True) {
			if (!isset($this -> pictures[$p['id']])) {
				break;
			} else {
				$p['id'] = $p['id'] + 1;
			}
		}

		// Adding the picture
		try {
			$this -> pictures[$p['id']] = new Picture($p, $p['id']);
			return $this -> save();
		} catch (Exception $e) {
			// Failed to create the picture
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?pic='.$p['id'].' '.$GLOBALS['messages'][20017]);
			error_log((string) $e);
			return 20017;
		}
	}

	/**
	 * Method to delete a network.
	 *
	 * @param   int     $i                  Network ID
	 * @return  int                         0 if OK
	 */
	public function deleteNetwork($i) {
		if (isset($this -> networks[$i])) {
			// Unlink node interfaces
			foreach ($this -> getNodes() as $node_id => $node) {
				foreach ($node -> getInterfaces() as $interface_id => $interface) {
					if ($interface -> getNetworkId() === $i) {
						$this -> nodes[$node_id] -> unlinkInterface($interface_id);
					}
				}
			}
			unset($this -> networks[$i]);
		} else {
			error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?net='.$i.' '.$GLOBALS['messages'][20023]);
		}
		return $this -> save();
	}

	/**
	 * Method to delete a node.
	 *
	 * @param   int     $i                  Node ID
	 * @return  int                         0 if OK
	 */
	public function deleteNode($i) {
		if (isset($this -> nodes[$i])) {
			$node = $this -> nodes[$i];
			if (!empty($node -> getSerials())) {
				// Node has configured Serial interfaces
				foreach ($node -> getSerials() as $interface_id => $interface) {
					if ($interface -> getRemoteId() != 0) {
						// Serial interface is configured, unlink remote node
						$rc = $this -> nodes[$interface -> getRemoteId()] -> unlinkInterface($interface -> getRemoteIf());
						if ($rc !== 0) {
							error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?node='.$interface -> getRemoteId().' '.$GLOBALS['messages'][20035]);
						}
					}
				}
			}

			// Delete the node
			unset($this -> nodes[$i]);
		} else {
			error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?node='.$i.' '.$GLOBALS['messages'][20024]);
		}
		return $this -> save();
	}

	/**
	 * Method to delete a picture.
	 *
	 * @param   int     $i                  Picture ID
	 * @return  int                         0 if OK
	 */
	public function deletePicture($i) {
		if (isset($this -> pictures[$i])) {
			unset($this -> pictures[$i]);
		} else {
			error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?pic='.$i.' '.$GLOBALS['messages'][20018]);
		}
		return $this -> save();
	}

	/**
	 * Method to add or replace the lab metadata.
	 * Editable attributes:
	 * - author
	 * - description
	 * - version
	 * If an attribute is set and is valid, then it will be used. If an
	 * attribute is not set, then the original is maintained. If in attribute
	 * is set and empty '', then the current one is deleted.
	 *
	 * @param   Array   $p                  Parameters
	 * @return  int                         0 means ok
	 */
	public function edit($p) {
		$modified = False;

		if (isset($p['author']) && $p['author'] === '') {
			// Author is empty, unset the current one
			unset($this -> author);
			$modified = True;
		} else if (isset($p['author'])) {
			$this -> author = htmlspecialchars($p['author'], ENT_DISALLOWED, 'UTF-8', TRUE);
			$modified = True;
		}

		if (isset($p['description']) && $p['description'] === '') {
			// Description is empty, unset the current one
			unset($this -> description);
			$modified = True;
		} else if (isset($p['description'])) {
			$this -> description = htmlspecialchars($p['description'], ENT_DISALLOWED, 'UTF-8', TRUE);
			$modified = True;
		}

		if (isset($p['version']) && $p['version'] === '') {
			// Version is empty, unset the current one
			unset($this -> version);
			$modified = True;
		} else if (isset($p['version']) && (int) $p['version'] < 0) {
			// Version is not valid, ignored
			error_log('WARNING: '.$GLOBALS['messages'][30008]);
		} else {
			$this -> version = (int) $p['version'];
			$modified = True;
		}

		if ($modified) {
			// At least an attribute is changed
			return $this -> save();
		} else {
			// No attribute has been changed
			error_log('ERROR: '.$GLOBALS['messages'][20030]);
			return 20030;
		}
	}

	/**
	 * Method to edit a network.
	 *
	 * @param   Array   $p                  Parameters
	 * @return	int	                        0 if OK
	 */
	public function editNetwork($p) {
		if (!isset($this -> networks[$p['id']])) {
			// Network not found
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?net='.$p['id'].' '.$GLOBALS['messages'][20023]);
			return 20023;
		} else if ($this -> networks[$p['id']] -> edit($p) === 0) {
			return $this -> save();
		} else {
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?net='.$p['id'].' '.$GLOBALS['messages'][20025]);
			return False;
		}
	}

	/**
	 * Method to edit a node.
	 *
	 * @param   Array   $p                  Parameters
	 * @return	int	                        0 if OK
	 */
	public function editNode($p) {
		if (!isset($this -> nodes[$p['id']])) {
			// Node not found
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$p['id'].' '.$GLOBALS['messages'][20024]);
			return 20024;
		} else if ($this -> nodes[$p['id']] -> edit($p) === 0) {
			return $this -> save();
		} else {
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$p['id'].' '.$GLOBALS['messages'][20026]);
			return 20026;
		}
	}

	/**
	 * Method to edit a picture.
	 *
	 * @param   Array   $p                  Parameters
	 * @return	int	                        0 if OK
	 */
	public function editPicture($p) {
		if (!isset($this -> pictures[$p['id']])) {
			// Picture not found
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?pic='.$p['id'].' '.$GLOBALS['messages'][20018]);
			return 20018;
		} else if ($this -> pictures[$p['id']] -> edit($p) === 0) {
			return $this -> save();
		} else {
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?pic='.$p['id'].' '.$GLOBALS['messages'][20019]);
			return False;
		}
	}

	/**
	 * Method to get lab author.
	 *
	 * @return  string                      Lab author or False if not set
	 */
	public function getAuthor() {
		if (isset($this -> author)) {
			return $this -> author;
		} else {
			// By default return an empty string
			return '';
		}
	}

	/**
	 * Method to get lab description.
	 *
	 * @return  string                      Lab description or False if not set
	 */
	public function getDescription() {
		if (isset($this -> description)) {
			return $this -> description;
		} else {
			// By default return an empty string
			return '';
		}
	}

	/**
	 * Method to get lab filename.
	 *
	 * @return  string                      Lab filename
	 */
	public function getFilename() {
		return $this -> filename;
	}

	/**
	 * Method to get free network ID.
	 *
	 * @return  int                         Free network ID
	 */
	public function getFreeNetworkId() {
		$id = 1;

		// Finding a free network ID
		while (True) {
			if (!isset($this -> networks[$id])) {
				return $id;
			}
			$id = $id + 1;
		}
	}

	/**
	 * Method to get free node ID.
	 *
	 * @return  int                         Free node ID
	 */
	public function getFreeNodeId() {
		$id = 1;

		// Finding a free node ID
		while (True) {
			if (!isset($this -> nodes[$id])) {
				return $id;
			}
			$id = $id + 1;
		}
	}

	/**
	 * Method to get lab ID.
	 *
	 * @return  string                      Lab ID
	 */
	public function getId() {
		return $this -> id;
	}

	/**
	 * Method to get lab name.
	 *
	 * @return  string                      Lab name
	 */
	public function getName() {
		return $this -> name;
	}

	/**
	 * Method to get all lab networks.
	 *
	 * @return  Array                       Lab networks
	 */
	public function getNetworks() {
		if (!empty($this -> networks)) {
			return $this -> networks;
		} else {
			// By default return an empty array
			return Array();
		}
	}

	/**
	 * Method to get all lab nodes.
	 *
	 * @return  Array                       Lab nodes
	 */
	public function getNodes() {
		if (!empty($this -> nodes)) {
			return $this -> nodes;
		} else {
			// By default return an empty array
			return Array();
		}
	}

	/**
	 * Method to get all lab pictures.
	 *
	 * @return  Array                       Lab pictures
	 */
	public function getPictures() {
		if (!empty($this -> pictures)) {
			return $this -> pictures;
		} else {
			// By default return an empty array
			return Array();
		}
	}

	/**
	 * Method to get lab path.
	 *
	 * @return  string                      Lab absolute path
	 */
	public function getPath() {
		return $this -> path;
	}

	/**
	 * Method to get tenant ID.
	 *
	 * @return  int                         Tenant ID
	 */
	public function getTenant() {
		return $this -> tenant;
	}

	/**
	 * Method to get lab version.
	 *
	 * @return  string                      Lab version or False if not set
	 */
	public function getVersion() {
		if (isset($this -> version)) {
			return $this -> version;
		} else {
			// By default return 0
			return 0;
		}
	}

	/**
	 * Method to connect a node to a network or to a remote node.
	 *
	 * @param   int     $n                  Node ID
	 * @param   Array   $p                  Array of interfaces to link (index = interface_id, value = remote)
	 * @return	int                         0 means ok
	 */
	public function connectNode($n, $p) {
		if (!isset($this -> nodes[$n])) {
			// Node not found
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$i.' '.$GLOBALS['messages'][20032]);
			return 20032;
		}

		foreach ($p as $interface_id => $interface_link) {
			if ($interface_link !== '') {
				// Interface must be configured
				$i = Array();
				$i['id'] = $interface_id;

				if (strpos($interface_link, ':') === False) {
					// No ':' found -> simple Ethernet interface
					if (isset($this -> getNetworks()[$interface_link])) {
						// Network exists
						$i['network_id'] = $interface_link;

						// Link the interface
						if ($this -> nodes[$n] -> linkInterface($i) !== 0) {
							error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$n.' '.$GLOBALS['messages'][20034]);
							return 20034;
						}
					} else {
						error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?net='.$interface_link.' '.$GLOBALS['messages'][20033]);
						return 20033;
					}
				} else {
					// ':' found -> should be Serial interface
					$remote_id = substr($interface_link, 0, strpos($interface_link, ':'));
					$remote_if = substr($interface_link, strpos($interface_link, ':') + 1);

					// Before connect, we need to unlink remote node of both source and destination node
					$node = $this -> nodes[$n];  // Source node
					if (isset($node -> getSerials()[$interface_id]) && $node -> getSerials()[$interface_id] -> getRemoteId() !== 0) {
						// Serial interfaces was previously connected, need to unlink remote node
						$rc = $this -> nodes[$node -> getSerials()[$interface_id] -> getRemoteId()] -> unlinkInterface($node -> getSerials()[$interface_id] -> getRemoteIf());
						if ($rc !== 0) {
							error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?node='.$node_id.' '.$GLOBALS['messages'][20035]);
						}
					}
					$node = $this -> nodes[$remote_id];  // Destination node
					if (isset($node -> getSerials()[$remote_if]) && $node -> getSerials()[$remote_if] -> getRemoteId() !== 0) {
						// Serial interfaces was previously connected, need to unlink remote node
						$rc = $this -> nodes[$node -> getSerials()[$remote_if] -> getRemoteId()] -> unlinkInterface($node -> getSerials()[$remote_if] -> getRemoteIf());
						if ($rc !== 0) {
							error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?node='.$node_id.' '.$GLOBALS['messages'][20035]);
						}
					}

					// Connect local to remote: Local $n:$interface_id -> Remote $remote_id:$remote_if
					$i['id'] = $interface_id;
					$i['remote_id'] = $remote_id;
					$i['remote_if'] = $remote_if;

					// Link the interface
					if ($this -> nodes[$n] -> linkInterface($i) !== 0) {
						error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$n.' '.$GLOBALS['messages'][20034]);
						return 20034;
					}

					// Connect remote to local: Local $n:$interface_id <- Remote $remote_id:$remote_if
					$i = Array();
					$i['id'] = $remote_if;
					$i['remote_id'] = $n;
					$i['remote_if'] = $interface_id;

					// Link the interface
					if ($this -> nodes[$remote_id] -> linkInterface($i) !== 0) {
						error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$remote_id.' '.$GLOBALS['messages'][20034]);
						return 20034;
					}
				}
			} else {
				// Interface must be deconfigured
				$node = $this -> nodes[$n];
				if (isset($node -> getSerials()[$interface_id]) && $node -> getSerials()[$interface_id] -> getRemoteId() !== 0) {
					// Serial interfaces was previously connected, need to unlink remote node
					$rc = $this -> nodes[$node -> getSerials()[$interface_id] -> getRemoteId()] -> unlinkInterface($node -> getSerials()[$interface_id] -> getRemoteIf());
					if ($rc !== 0) {
						error_log('WARNING: '.$this -> path .'/'.$this -> filename.'?node='.$node -> getSerials()[$interface_id] -> getRemoteId().' '.$GLOBALS['messages'][20035]);
					}
				}

				// Now deconfigure local interface
				if ($this -> nodes[$n] -> unlinkInterface($interface_id) !== 0) {
					error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$n.' '.$GLOBALS['messages'][20035]);
					return 20035;
				}
			}
		}

		return $this -> save();
	}

	/**
	 * Method to save a lab into a file.
	 *
	 * @return  int                         0 means ok
	 */
	public function save() {
		// XML header is splitted because of a highlight syntax bug on VIM
		$xml = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8" standalone="yes"?'.'><lab></lab>');
		$xml -> addAttribute('name', $this -> name);
		$xml -> addAttribute('id', $this -> id);

		if (isset($this -> version)) $xml -> addAttribute('version', $this -> version);
		if (isset($this -> author)) $xml -> addAttribute('author', $this -> author);
		if (isset($this -> description)) $xml -> addChild('description', $this -> description);

		// Add topology
		if (!empty($this -> getNodes()) || !empty($this -> getNetworks())) {
			$xml -> addChild('topology');

			// Add nodes
			if (!empty($this -> getNodes())) {
				$xml -> topology -> addChild('nodes');
				foreach ($this -> getNodes() as $node_id => $node) {
					$d = $xml -> topology -> nodes -> addChild('node');
					$d -> addAttribute('id', $node_id);
					$d -> addAttribute('name', $node -> getName());
					$d -> addAttribute('type', $node -> getNType());
					$d -> addAttribute('template', $node -> getTemplate());
					$d -> addAttribute('image', $node -> getImage());
					switch ($node -> getNType()) {
						case 'iol':
							// IOL specific parameters
							$d -> addAttribute('ethernet', $node -> getEthernetCount());
							$d -> addAttribute('nvram', $node -> getNvram());
							$d -> addAttribute('ram', $node -> getRam());
							$d -> addAttribute('serial', $node -> getSerialCount());
							break;
						case 'dynamips':
							// Dynamips specific parameters
							$d -> addAttribute('idlepc', $node -> getIdlePc());
							$d -> addAttribute('nvram', $node -> getNvram());
							$d -> addAttribute('ram', $node -> getRam());
							foreach ($node -> getSlot() as $slot => $module) {
								$s = $d -> addChild('slot');
								$s -> addAttribute('id', $slot);
								$s -> addAttribute('module', $module);
							}
							break;
						case 'qemu':
							// QEMU specific parameters
							$d -> addAttribute('console', $node -> getConsole());
							$d -> addAttribute('cpu', $node -> getCpu());
							$d -> addAttribute('ram', $node -> getRam());
							$d -> addAttribute('ethernet', $node -> getEthernetCount());
							$d -> addAttribute('uuid', $node -> getUuid());
							break;
					}

					$d -> addAttribute('delay', $node -> getDelay());
					$d -> addAttribute('icon', $node -> getIcon());
					$d -> addAttribute('config', $node -> getConfig());
					$d -> addAttribute('left', $node -> getLeft());
					$d -> addAttribute('top', $node -> getTop());

					// Add Ethernet interfaces
					foreach ($node -> getEthernets() as $interface_id => $interface) {
						if ($interface -> getNetworkId() > 0 && isset($this -> getNetworks()[$interface -> getNetworkId()])) {
							$e = $d -> addChild('interface');
							$e -> addAttribute('id', $interface_id);
							$e -> addAttribute('name', $interface -> getName());
							$e -> addAttribute('type', $interface -> getNType());
							$e -> addAttribute('network_id', $interface -> getNetworkId());
						}
					}

					// Add Serial interfaces
					foreach ($node -> getSerials() as $interface_id => $interface) {
						if ($interface -> getRemoteId() > 0 && isset($this -> getNodes()[$interface -> getRemoteId()])) {
							$e = $d -> addChild('interface');
							$e -> addAttribute('id', $interface_id);
							$e -> addAttribute('type', $interface -> getNType());
							$e -> addAttribute('name', $interface -> getName());
							$e -> addAttribute('remote_id', $interface -> getRemoteId());
							$e -> addAttribute('remote_if', $interface -> getRemoteIf());
						}
					}
				}
			}

			// Add networks
			if (!empty($this -> getNetworks())) {
				$xml -> topology -> addChild('networks');
				foreach ($this -> getNetworks() as $network_id => $network) {
					$n = $xml -> topology -> networks -> addChild('network');
					$n -> addAttribute('id', $network_id);
					$n -> addAttribute('type', $network -> getNType());
					$n -> addAttribute('name', $network -> getName());
					$n -> addAttribute('left', $network -> getLeft());
					$n -> addAttribute('top', $network -> getTop());
				}
			}

			// Update attached network count
			$this -> setNetworkCount();
		}

		// Add objects
		$objects = False;

		// Add pictures
		if (!empty($this -> getPictures())) {
			$objects = True;
			$xml -> addChild('objects');
			$xml -> objects -> addChild('pictures');
		}
		foreach ($this -> getPictures() as $picture_id => $picture) {
			$p = $xml -> objects -> pictures -> addChild('picture');
			$p -> addAttribute('id', $picture_id);
			$p -> addAttribute('name', $picture -> getName());
			$p -> addAttribute('type', $picture -> getNType());
			$p -> addAttribute('width', $picture -> getWidth());
			$p -> addAttribute('height', $picture -> getHeight());
			$p -> addChild('data', base64_encode($picture -> getData()));
			$p -> addChild('map', htmlspecialchars($picture -> getMap()));
		}

		// Add configs
		$configs = False;
		foreach ($this -> getNodes() as $node_id => $node) {
			$config_data = $node -> getConfigData();
			if ($config_data !== '') {
				if ($objects == False) {
					$xml -> addChild('objects');
					$objects = True;
				}
				if ($configs == False) {
					$xml -> objects -> addChild('configs');
					$configs = True;
				}
				$c = $xml -> objects -> configs -> addChild('config', base64_encode($config_data));
				$c -> addAttribute('id', $node_id);
			}
		}


		// Well format the XML
		$dom = new DOMDocument('1.0');
		$dom -> preserveWhiteSpace = false;
		$dom -> formatOutput = true;
		$dom -> loadXML($xml -> asXML());

		// Write to file
		$tmp = $this -> path.'/'.$this -> filename.'.swp';
		$dst = $this -> path.'/'.$this -> filename;
		$fp = fopen($tmp, 'w');
		if (!fwrite($fp, $dom -> saveXML())) {
			// Failed to write
			fclose($fp);
			unlink($tmp);
			error_log('ERROR: '.$GLOBALS['messages'][20027]);
			return 20027;
		} else {
			// Write OK
			fclose($fp);
			if (is_file($dst) && !unlink($dst)) {
				// Cannot delete original lab
				unlink($tmp);
				error_log('WARNING: '.$GLOBALS['messages'][20028]);
				return 20028;
			}
			if (!rename($tmp, $dst)) {
				// Cannot move $tmp to $dst
				error_log('WARNING: '.$GLOBALS['messages'][20029]);
				return 20029;
			}
		}
		return 0;
	}

	/**
	 * Method to set attached node count for each network
	 *
	 * @return	void
	 */
	public function setNetworkCount() {
		// Count attached nodes for this network
		foreach ($this -> getNetworks() as $network_id => $network) {
			$i = 0;
			foreach ($this -> getNodes() as $node) {
				foreach ($node -> getEthernets() as $interface) {
					if ($interface -> getNetworkId() === $network_id) {
						$i++;
					}
				}
			}
			$network -> setCount($i);
		}
	}

	/**
	 * Method to set startup-config for a specific node
	 *
	 * @param   int		$node_id			Node ID
	 * @param   string  $config_data         Binary config
	 * @return  int                         0 means ok
	 */
	public function setNodeConfigData($node_id, $config_data) {
		if (!isset($this -> nodes[$node_id])) {
			// Node not found
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$node_id.' '.$GLOBALS['messages'][20024]);
			return 20024;
		} else if ($this -> nodes[$node_id] -> setConfigData($config_data) === 0) {
			$this -> nodes[$node_id] -> edit(Array('config' => 'Saved'));
			return $this -> save();
		} else {
			error_log('ERROR: '.$this -> path .'/'.$this -> filename.'?node='.$node_id.' '.$GLOBALS['messages'][20036]);
			return False;
		}

	}
}
?>
