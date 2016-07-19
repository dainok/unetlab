<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_uusers.php
 *
 * UNetLab Users related functions for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/**
 * Function to get a UNetLab user.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param   string	$user               Get a single user
 * @return  Array						Single UNetLab user (JSend data)
 */
function apiGetUUser($db, $user) {
	$data = Array();

	$query = 'SELECT users.username AS username, email, users.expiration AS expiration, name, session, role, ip, pods.id AS pod, pods.expiration AS pexpiration FROM users LEFT JOIN pods ON users.username = pods.username WHERE users.username = :username;';

	try {
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch(PDO::FETCH_ASSOC);
		if (!empty($result)) {
			// Check should have a new single user
			foreach ($result as $key => $value) {
				$data[$key] = $value;
			}
			if (!isset($data['pod'])) {
				$data['pod'] = -1;
			}
		} else {
			// User not found
			$output['code'] = 404;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][60039];
			return $output;
		}

		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60040];
		$output['data'] = $data;
	} catch (Exception $e) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90003];
	}
	return $output;
}

/**
 * Function to edit a UNetLab users.
 *
 * @param	PDO		$db					PDO object for database connection
 * @return  Array                       UNetLab users (JSend data)
 */
function apiGetUUsers($db) {
	$data = Array();

	$query = 'SELECT users.username AS username, email, users.expiration AS expiration, folder, name, session, role, ip, pods.id AS pod, pods.expiration AS pexpiration, pods.lab_id AS lab FROM users LEFT JOIN pods ON users.username = pods.username ORDER BY users.username ASC;';
	try {
		$statement = $db -> prepare($query);
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
			$data[$row['username']]['folder'] = $row['folder'];
			$data[$row['username']]['lab'] = $row['lab'];
			if ($row['pod'] == Null) {
				$data[$row['username']]['pod'] = -1;
			} else {
				$data[$row['username']]['pod'] = $row['pod'];
			}
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
	} catch (Exception $e) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90003];
	}
	return $output;
}

/**
 * Function to delete a UNetLab user.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	string	$user				UNetLab user
 * @return  Array                       Return code (JSend data)
 */
function apiDeleteUUser($db, $user) {
	if (empty($user)) {
		// User not found
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60039];
		return $output;
	}

	try {
		// Free previously used pod
		$query = 'DELETE FROM pods WHERE username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();

		// Delete user
		$query = 'DELETE FROM users WHERE username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();

		$output['code'] = 201;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60042];
	} catch (Exception $e) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90003];
	}
	return $output;
}

/**
 * Function to edit UNetLab user.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	string	$user				UNetLab user
 * @param	Array	$p					Parameters
 * @return  Array                       Return code (JSend data)
 */
function apiEditUUser($db, $user, $p) {
	// TODO missing try/catch
	// TODO need to check all parameters
	if (empty($user)) {
		// User not found
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60039];
		return $output;
	}

	$update_user = False;
	$query = 'UPDATE users SET ';
	if (isset($p['name']) && !empty($p['name'])) {
		$query .= 'name = :name, ';
		$update_user = True;
	}
	if (isset($p['email']) && !empty($p['email'])) {
		$query .= 'email = :email, ';
		$update_user = True;
	}
	if (isset($p['password']) && !empty($p['password'])) {
		$query .= 'password = :password, ';
		$update_user = True;
	}
	if (isset($p['role']) && !empty($p['role'])) {
		$query .= 'role = :role, ';
		$update_user = True;
	}
	if (isset($p['expiration']) && !empty($p['expiration'])) {
		$query .= 'expiration = :expiration, ';
		$update_user = True;
	}
	$query = substr($query, 0, -2);	// Remove last ', ' chars
	$query .= ' WHERE username = :username;';
	if ($update_user) {
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		if (isset($p['name']) && !empty($p['name'])) {
			$statement -> bindParam(':name', htmlentities($p['name']), PDO::PARAM_STR);
		}
		if (isset($p['email']) && !empty($p['email'])) {
			$statement -> bindParam(':email', htmlentities($p['email']), PDO::PARAM_STR);
		}
		if (isset($p['password']) && !empty($p['password'])) {
			$statement -> bindParam(':password',  $hash = hash('sha256', $p['password']), PDO::PARAM_STR);
		}
		if (isset($p['role']) && !empty($p['role'])) {
			$statement -> bindParam(':role', $p['role'], PDO::PARAM_STR);
		}
		if (isset($p['expiration']) && !empty($p['expiration'])) {
			$statement -> bindParam(':expiration', $p['expiration'], PDO::PARAM_STR);
		}
		$statement -> execute();
		$result = $statement -> fetch();
	}

	// Update PODs
	if (isset($p['pod']) && $p['pod'] !== '') {
		// Free used previously used pod
		$query = 'DELETE FROM pods WHERE username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();
		if (!isset($p['pexpiration'])) {
			$p['pexpiration'] = '-1';
		}
		$query = 'INSERT OR REPLACE INTO pods (id, expiration, username) VALUES(:id, :expiration, :username);';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':id', $p['pod'], PDO::PARAM_INT);
		$statement -> bindParam(':expiration', $p['pexpiration'], PDO::PARAM_STR);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();
	} else if (isset($p['pod'])) {
		$query = 'DELETE FROM pods WHERE username = :username;';
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $user, PDO::PARAM_STR);
		$statement -> execute();
		$result = $statement -> fetch();
	}

	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][60042];
	return $output;
}

/**
 * Function to add a UNetLab user.
 *
 * @param	PDO		$db					PDO object for database connection
 * @param	Array	$p					Parameters
 * @return  Array                       Return code (JSend data)
 */
function apiAddUUser($db, $p) {
	// TODO need to check all parameters
	if (!isset($p['username']) || !isset($p['password']) || !isset($p['role'])) {
		// Username not set
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60043];
		return $output;
	}

	// Setting optional parameters
	if (!isset($p['email'])) $p['email'] = '';
	if (!isset($p['expiration']) || $p['expiration'] == '') {
		$p['expiration'] = -1;
	}
	if (!isset($p['name'])) $p['name'] = '';

	$query = 'INSERT INTO users (username, email, name, password, expiration, role) VALUES (:username, :email, :name, :password, :expiration, :role);';
	try {
		$statement = $db -> prepare($query);
		$statement -> bindParam(':username', $p['username'], PDO::PARAM_STR);
		$statement -> bindParam(':email', $p['email'], PDO::PARAM_STR);
		$statement -> bindParam(':name', $p['name'], PDO::PARAM_STR);
		$statement -> bindParam(':password',  $hash = hash('sha256', $p['password']), PDO::PARAM_STR);
		$statement -> bindParam(':expiration', $p['expiration'], PDO::PARAM_STR);
		$statement -> bindParam(':role', $p['role'], PDO::PARAM_STR);
		$statement -> execute();
	} catch (Exception $e) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60045];
		return $output;
	}

	try {
		// Update PODs
		if (isset($p['pod']) && $p['pod'] !== '-1') {
			$result = $statement -> fetch();
			if (!isset($p['pexpiration'])) {
				$p['pexpiration'] = '-1';
			}
			$query = 'INSERT OR REPLACE INTO pods (id, expiration, username) VALUES(:id, :expiration, :username);';
			$statement = $db -> prepare($query);
			$statement -> bindParam(':id', $p['pod'], PDO::PARAM_INT);
			$statement -> bindParam(':expiration', $p['pexpiration'], PDO::PARAM_STR);
			$statement -> bindParam(':username', $p['username'], PDO::PARAM_STR);
			$statement -> execute();
			$result = $statement -> fetch();
		}

		$output['code'] = 201;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60042];
	} catch (Exception $e) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90003];
	}
	return $output;
}
?>
