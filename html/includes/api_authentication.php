<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/api_authentication.php
 *
 * Users related functions for REST APIs.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/*
 * Function to login a user.
 *
 * @param	PDO			$db				PDO object for database connection
 * @param	Array		$p				Parameters
 * @param	String		$cookie			Session cookie
 * @return	bool						True if valid
 */
function apiLogin($db, $p, $cookie) {
	if (!isset($p['username'])) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90011];
		return $output;
	} else {
		$username = $p['username'];
	}

	if (!isset($p['password'])) {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90012];
		return $output;
	} else {
		$hash = hash('sha256', $p['password']);
	}

	$rc = deleteSessions($db, $username);
	if ($rc !== 0) {
		// Cannot delete old sessions
		$output['code'] = 500;
		$output['status'] = 'error';
		$output['message'] = $GLOBALS['messages'][$rc];
		return $output;
	}

	$query = 'SELECT COUNT(*) as rows FROM users WHERE username = :username AND password = :password;';
	$statement = $db -> prepare($query);
	$statement -> bindParam(':username', $username, PDO::PARAM_STR);
	$statement -> bindParam(':password', $hash, PDO::PARAM_STR);
	$statement -> execute();
	$result = $statement -> fetch();

	if ($result['rows'] == 1) {
		// User/Password match
		if (checkUserExpiration($db, $username) === False) {
			$output['code'] = 401;
			$output['status'] = 'unauthorized';
			$output['message'] = $GLOBALS['messages'][90018];
			return $output;
		}

		// UNetLab is running in multi-user mode
		$rc = configureUserPod($db, $username);
		if ($rc !== 0) {
			// Cannot configure a POD
			$output['code'] = 500;
			$output['status'] = 'error';
			$output['message'] = $GLOBALS['messages'][$rc];
			return $output;
		}

		$rc = updateUserCookie($db, $username, $cookie);
		if ($rc !== 0) {
			// Cannot update user cookie
			$output['code'] = 500;
			$output['status'] = 'error';
			$output['message'] = $GLOBALS['messages'][$rc];
			return $output;
		}

		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][90013];
	} else if ($result['rows'] == 0) {
		// User/Password does not match
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][90014];
	} else {
		// Invalid result
		$output['code'] = 500;
		$output['status'] = 'error';
		$output['message'] = $GLOBALS['messages'][90015];
	}

	return $output;
}

/*
 * Function to logout a user.
 *
 * @param	PDO			$db				PDO object for database connection
 * @param	String		$cookie			Session cookie
 * @return	bool						True if valid
 */
function apiLogout($db, $cookie) {
	$query = 'UPDATE users SET cookie = NULL, session = NULL WHERE cookie = :cookie;';
	$statement = $db -> prepare($query);
	$statement -> bindParam(':cookie', $cookie, PDO::PARAM_STR);
	$statement -> execute();
	$result = $statement -> fetch();

	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages'][90019];
	return $output;
}

/*
 * Function to check authorization
 *
 * @param	PDO			$db				PDO object for database connection
 * @param	String		$cookie			Session cookie
 * @return	Array						Username, role, tenant if logged in; JSend data if not authorized
 */
function apiAuthorization($db, $cookie) {
	$output = Array();
	$user = getUserByCookie($db, $cookie);	// This will check session/web/pod expiration too

	if (empty($user)) {
		// Used not logged in
		$output['code'] = 412;
		$output['status'] = 'unauthorized';
		$output['message'] = $GLOBALS['messages']['90001'];
		return Array(False, False, $output);
	} else {
		// User logged in
		$rc = updateUserCookie($db, $user['username'], $cookie);
		if ($rc !== 0) {
			// Cannot update user cookie
			$output['code'] = 500;
			$output['status'] = 'error';
			$output['message'] = $GLOBALS['messages'][$rc];
			return Array(False, False, $output);
		}
	}

	return Array($user, $user['tenant'], False);
}
?>
