<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/__textobject.php
 *
 * Class for UNetLab custom objects.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 * @property type $data of the object. It's mandatory.
 * @property type $id ID of the object. It's mandatory and automatically set during contruction phase.
 * @property type $name Name of the object. It's optional but suggested.
 * @property type $type of the object. It's mandatory.
 */

class TextObject {
	private $data;
	private $id;
	private $name;
	private $type;
	
	/**
	 * Constructor which creates a picture from a uploaded file.
	 * Parameters:
	 * - data*
	 * - name
	 * - type*
	 * *mandatory
	 *
	 * @param   Array   $p                  Parameters
	 * @param   int     $id                 Picture ID
	 * @return	void
	 */
	public function __construct($p, $id) {
		// Mandatory parameters
		if (!isset($p['data']) || !isset($p['type'])) {
			// Missing mandatory parameters
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][51000]);
			throw new Exception('51000');
			return 51000;
		}

		// Optional parameters
		if (isset($p['name']) && $p['name'] === '') {
			// Name is empty, ignored
			unset($p['name']);
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][51002]);
		}

		if (!checkTextObjectType($p['type'])) {
			// Type is not valid
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][51001]);
			throw new Exception('51001');
			return 51001;
		}

		// Now building the object
		$this -> data = $p['data'];
		$this -> id = (int) $id;
		$this -> type = $p['type'];
		if (isset($p['name'])) $this -> name = htmlentities($p['name']);
	}

	/**
	 * Method to edit an object
	 * Editable attributes:
	 * - data
	 * - name
	 * If an attribute is set and is valid, then it will be used. If an
	 * attribute is not set, then the original is maintained. If in attribute
	 * is set and empty '', then the current one is deleted.
	 *
	 * @param   Array   $p                  Parameters
	 * @return  int                         0 means ok
	 */
	public function edit($p) {
		$modified = False;

		if (isset($p['data']) && $p['data'] === '') {
			// Data is not valid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][51003]);
		} else if (isset($p['data'])) {
			$this -> data = $p['data'];
			$modified = True;
		}

		if (isset($p['name']) && $p['name'] === '') {
			// Name is empty, unset the current one
			unset($this -> name);
			$modified = True;
		} else if (isset($p['name']) && !checkTextObjectName($p['name'])) {
			// Name is not valid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][51002]);
		} else if (isset($p['name'])) {
			$this -> name = htmlentities($p['name']);
			$modified = True;
		}

		if ($modified) {
			// At least an attribute is changed
			return 0;
		} else {
			// No attribute has been changed
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][50006]);
			return 50006;
		}
	}

	/**
	 * Method to get the object data
	 *
	 * @return  string                      The object
	 */
	public function getData() {
		return $this -> data;
	}

	/**
	 * Method to get the object name.
	 *
	 * @return  string                      The object name
	 */
	public function getName() {
		return html_entity_decode($this -> name);
	}

	/**
	 * Method to get the object type.
	 *
	 * @return  string                      The object type
	 */
	public function getNType() {
		return $this -> type;
	}
}
?>
