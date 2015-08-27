<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_uuser.php
 *
 * UNetLab Users related functions for REST APIs.
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
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with UNetLab. If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2015 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20150804
 */

/**
 * Function to get UNetLab users.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param   string	$user               If empty get all users
 * @return  Array                       Lab node (JSend data)
 */
function apiGetUUsers($db, $user) {
	$data = Array();
	if (empty($user)) {
		// List all users
		$query = 'SELECT users.username AS username, email, users.expiration AS expiration, name, session, role, ip, pods.id AS pod, pods.expiration AS pexpiration FROM users LEFT JOIN pods ON users.username = pods.username ORDER BY users.username ASC;';
		$statement = $db -> prepare($query);
	} else {
		// List a specific user
		$query = 'SELECT users.username AS username, email, users.expiration AS expiration, name, session, role, ip, pods.id AS pod, pods.expiration AS pexpiration FROM users LEFT JOIN pods ON users.username = pods.username WHERE users.username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
	}
	$statement -> execute();
	while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
		$data[$row['username']] = Array();
		$data[$row['username']]['username'] = $row['username'];
		$data[$row['username']]['email'] = $row['email'];
		$data[$row['username']]['expiration'] = $row['expiration'];
		$data[$row['username']]['name'] = $row['name'];
		$data[$row['username']]['session'] = $row['session'];
		$data[$row['username']]['role'] = $row['role'];
		$data[$row['username']]['ip'] = $row['ip'];
		$data[$row['username']]['pod'] = $row['pod'];
		$data[$row['username']]['pexpiration'] = $row['pexpiration'];
	}
	
	if (empty($data)) {
		// User not found
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60039];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60040];
		$output['data'] = $data;
	}
	return $output;
}
?>