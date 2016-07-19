<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1

/**
 * html/includes/api_textobjects.php
 *
 * Pictures related functions for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/**
 * Function to add a textobject to a lab.
 *
 * @param   Lab     $lab                Lab
 * @param   Array   $p                  Parameters
 * @return  Array                       Return code (JSend data)
 */
function apiAddLabTextObject($lab, $p) {
	// Adding the object
	$rc = $lab -> addTextObject($p);
	if ($rc -> status === 0) {
		$output['code'] = 201;
		$output['result'] = $rc;
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
 * Function to delete a textobject.
 *
 * @param   Lab     $lab                Lab
 * @param   int     $id                 Object ID
 * @return  Array                       Return code (JSend data)
 */
function apiDeleteLabTextObject($lab, $id) {
	// Deleting the picture
	$rc = $lab -> deleteTextObject($id);

	if ($rc === 0) {
		$output['code'] = 200;
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
 * Function to edit a textobject.
 *
 * @param   Lab     $lab                Lab
 * @param   Array   $p                  Parameters
 * @return  Array                       Return code (JSend data)
 */
function apiEditLabTextObject($lab, $p) {
	$rc = $lab -> editTextObject($p);

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
 * Function to get a single textobject.
 *
 * @param   Lab     $lab                Lab
 * @param   int     $id                 Object ID
 * @return  Array                       Lab object (JSend data)
 */
function apiGetLabTextObject($lab, $id) {
	// Getting picture
	if (isset($lab -> getTextObjects()[$id])) {
		$textobject = $lab -> getTextObjects()[$id];
		// Printing picture
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = 'Object loaded';
		$output['data'] = Array(
			'id' => $id,
			'name' => $textobject -> getName(),
			'type' => $textobject -> getNType(),
			'data' => $textobject -> getData()
		);
	} else {
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = 'Object "'.$id.'" not found on lab "'.$lab_file.'".';
	}
	return $output;
}

/**
 * Function to get all lab textobjects.
 *
 * @param   Lab     $lab                Lab
 * @return  Array                       Lab objects (JSend data)
 */
function apiGetLabTextObjects($lab) {
	// Getting pictures
	$textobjects = $lab -> getTextObjects();

	// Printing objects
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60062];
	$output['data'] = Array();
	if (!empty($textobjects)) {
		foreach ($textobjects as $textobject_id => $textobject) {
			$output['data'][$textobject_id] = Array(
				'id' => $textobject_id,
				'name' => $textobject -> getName(),
				'type' => $textobject -> getNType(),
			);
		}
	}
    
    return $output;
}
?>
