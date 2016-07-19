<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/__network.php
 *
 * Class for UNetLab networks.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 * @property type $count Total of connected nodes to this network. If not set, it's automatically set to 0.
 * @property type $id Network ID. Mandatory and set during construction phase.
 * @property type $left Left margin for visual position. It's optional.
 * @property type $name Name of the network. It's optional but suggested.
 * @property type $tenant Tenant ID. Mandatory and set during construction phase.
 * @property type $top Top margin for visual position.
 * @property type $type Type of the network. It's mandatory.
 */

class Network {
	private $count;
	private $id;
	private $left;
	private $name; 
	private $tenant;
	private $top;
	private $type; 

	/**
	* Constructor which creates an Ethernet network.
	* Parameters:
	* - count
	* - left
	* - name
	* - top
	* - type*
	* *mandatory
	* 
	* @param   Array   $p                  Parameters
	* @param   int     $id                 Network ID
	* @return  void
	*/
	public function __construct($p, $id, $tenant) {
		// Mandatory parameters
		if (!isset($p['type'])) {
			// Missing mandatory parameters
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][30000]);
			throw new Exception('30000');
			return 30000;
		}

		if (!checkNetworkType($p['type'])) {
			// Type is not valid
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][30001]);
			throw new Exception('30001');
			return 30001;
		}

		// Optional parameters
		if (!isset($p['count'])) {
			// By default set to 0
			$p['count'] = 0;
		} else if ((int) $p['count'] < 0) {
			// Count is invalid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30007]);
			$p['count'] = 0;
		}

		if (isset($p['left']) && !checkPosition($p['left'])) {
			if (preg_match('/^[0-9]+%$/', $p['left']) && substr($p['left'], 0, -1) >= 0 && substr($p['left'], 0, -1) <= 100) {
				// Converting percentage to absolute using a 800x600 viewport
				$p['left'] = 1024 * substr($p['left'], 0, -1) / 100;
			} else {
				// Left is invalid, ignored
				unset($p['left']);
				error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30003]);
			}
		}

		if (isset($p['name']) && $p['name'] === '') {
			// Name is empty, ignored
			unset($p['name']);
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30002]);
		}

		if (isset($p['top']) && !checkPosition($p['top'])) {
			if (preg_match('/^[0-9]+%$/', $p['top']) && substr($p['top'], 0, -1) >= 0 && substr($p['top'], 0, -1) <= 100) {
				// Converting percentage to absolute using a 800x600 viewport
				$p['top'] = 768 * substr($p['top'], 0, -1) / 100;
			} else {
				// Top is invalid, ignored
				unset($p['top']);
				error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30004]);
			}
		}

		// Now building the network
		$this -> count = 0;
		$this -> id = (int) $id;
		$this -> tenant = (int) $tenant;
		$this -> type = $p['type'];
		if (isset($p['left'])) $this -> left = (int) $p['left'];
		if (isset($p['name'])) $this -> name = htmlentities($p['name']);
		if (isset($p['top'])) $this -> top = (int) $p['top'];
	}

	/**
	 * Method to add or replace the network metadata.
	 * Editable attributes:
	 * - left
	 * - name
	 * - top
	 * - type
	 * If an attribute is set and is valid, then it will be used. If an
	 * attribute is not set, then the original is maintained. If in attribute
	 * is set and empty '', then the current one is deleted.
	 *
	 * @param   Array   $p                  Parameters
	 * @return  int                         0 means ok
	 */
	public function edit($p) {
		$modified = False;

		if (isset($p['left']) && $p['left'] === '') {
			// Left is empty, unset the current one
			unset($this -> left);
			$modified = True;
		} else if (isset($p['left']) && !checkPosition($p['left'])) {
			// Left is not valid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30003]);
		} else if (isset($p['left'])) {
			$this -> left = $p['left'];
			$modified = True;
		}

		if (isset($p['name']) && $p['name'] === '') {
			// Name is empty, unset the current one
			unset($this -> name);
			$modified = True;
		} else if (isset($p['name'])) {
			$this -> name = htmlentities($p['name']);
			$modified = True;
		}

		if (isset($p['top']) && $p['top'] === '') {
			// Top is empty, unset the current one
			unset($this -> top);
			$modified = True;
		} else if (isset($p['top']) && !checkPosition($p['top'])) {
			// Top is not valid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30004]);
		} else if (isset($p['top'])) {
			$this -> top = $p['top'];
			$modified = True;
		}

		if (isset($p['type']) && !checkNetworkType($p['type'])) {
			// Type is not valid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30005]);
		} else if (isset($p['type'])) {
			$this -> type = $p['type'];
			$modified = True;
		}

		if ($modified) {
			// At least an attribute is changed
			return 0;
		} else {
			// No attribute has been changed
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][30006]);
			return 30006;
		}
	}

	/**
	 * Method to get the total connected nodes.
	 *
	 * @return  int                         Attached node count
	 */
	public function getCount() {
		return $this -> count;
	}

	/**
	 * Method to get left offset.
	 *
	 * @return  string                      Left offset
	 */
	public function getLeft() {
		if (isset($this -> left)) {
			return $this -> left;
		} else {
			// By default return a random value between 240 and 560
			return rand(240, 560);
		}
	}

	/**
	 * Method to get network name.
	 *
	 * @return  string                      Network name
	 */
	public function getName() {
		if (isset($this -> name)) {
			return $this -> name;
		} else {
			// By default return an empty string
			return 'Network '.$this -> id;
		}
	}

	/**
	 * Method to get network type.
	 *
	 * @return  string                      Network type
	 */
	public function getNType() {
		return $this -> type;
	}

	/**
	 * Method to get top offset.
	 *
	 * @return  string                      Top offset
	 */
	public function getTop() {
		if (isset($this -> top)) {
			return $this -> top;
		} else {
			// By default return a random value between 180 and 420
			return rand(180, 420);
		}
	}

	/**
	 * Method to check if a network is a cloud
	 *
	 * @return  bool                        True if network is a cloud
	 */
	public function isCloud() {
		if (in_array($this -> type, listClouds())) {
			return True;
		} else {
			return False;
		}
	}

	/**
	 * Method to set attached node count
	 *
	 * @param   int     $i                  Node count
	 * @return  0                           0 means ok
	 */
	public function setCount($i) {
		if ((int) $i >= 0) {
			$this -> count = (int) $i;
			return 0;
		} else {
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][30008]);
			return 30008;
		}
	}
}
?>
