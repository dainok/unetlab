<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/__picture.php
 *
 * Class for UNetLab pictures.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 * @property type $data Binary stream of the picture. It's mandatory.
 * @property type $height Width of the picture. It's automatically get from data.
 * @property type $id ID of the picture. It's mandatory and automatically set during contruction phase.
 * @property type $map HTML Map for the picture. It's optional.
 * @property type $name Name of the picture. It's optional but suggested.
 * @property type $type MIME type of the picture. It's mandatory.
 * @property type $width Width of the picture. It's automatically get from data.
 */

class Picture {
	private $data;
	private $height;
	private $id;
	private $map;
	private $name;
	private $type;
	private $width;
	
	/**
	 * Constructor which creates a picture from a uploaded file.
	 * Parameters:
	 * - data*
	 * - map
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
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][50000]);
			throw new Exception('50000');
			return 50000;
		}

		list($p['width'], $p['height']) = getimagesizefromstring($p['data']);
		if (!$p['height'] > 0 || !$p['width'] > 0) {
			// Picture is not valid
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][50002]);
			throw new Exception(50002);
			return 50002;
		}

		// Optional parameters
		if (isset($p['map']) && !checkPictureMap($p['map'])) {
			// Map is not valid, ignored
			unset($p['map']);
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][50005]);
		}

		if (isset($p['name']) && $p['name'] === '') {
			// Name is empty, ignored
			unset($p['name']);
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][50003]);
		}

		if (!checkPictureType($p['type'])) {
			// Type is not valid
			error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][50004]);
			throw new Exception('50004');
			return 50004;
		}

		// Now building the picture
		$this -> data = $p['data'];
		$this -> height = $p['height'];
		$this -> id = (int) $id;
		$this -> type = $p['type'];
		$this -> width = $p['width'];
		if (isset($p['map'])) $this -> map = $p['map'];
		if (isset($p['name'])) $this -> name = htmlentities($p['name']);
	}

	/**
	 * Method to add or replace the picture metadata.
	 * Editable attributes:
	 * - map
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

		if (isset($p['map']) && $p['map'] === '') {
			// Map is empty, unset the current one
			unset($this -> map);
			$modified = True;
		} else if (isset($p['map']) && !checkPictureMap($p['map'])) {
			// Map is not valid, ignored
			error_log(date('M d H:i:s ').'WARNING: '.$GLOBALS['messages'][50005]);
		} else {
			$this -> map = $p['map'];
			$modified = True;
		}

		if (isset($p['name']) && $p['name'] === '') {
			// Name is empty, unset the current one
			unset($this -> name);
			$modified = True;
		} else {
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
	 * Method to get the picture binary data.
	 *
	 * @return  string                      The picture
	 */
	public function getData() {
		return $this -> data;
	}

	/**
	 * Method to get the picture height.
	 *
	 * @return  int                         The picture height
	 */
	public function getHeight() {
		return $this -> height;
	}

	/**
	 * Method to get the picture map.
	 *
	 * @return  string                      The picture map
	 */
	public function getMap() {
		if (isset($this -> map)) {
			return $this -> map;
		} else {
			// By default return an empty string
			return '';
		}
	}

	/**
	 * Method to get the picture name.
	 *
	 * @return  string                      The picture name
	 */
	public function getName() {
		return html_entity_decode($this -> name);
	}

	/**
	 * Method to get the picture type.
	 *
	 * @return  string                      The picture type
	 */
	public function getNType() {
		return $this -> type;
	}

	/**
	 * Method to get the picture width.
	 *
	 * @return  int                         The picture width
	 */
	public function getWidth() {
		return $this -> width;
	}
}
?>
