<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/api.php
 *
 * REST API router for UNetLab.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

require_once('/opt/unetlab/html/includes/init.php');
require_once(BASE_DIR.'/html/includes/Slim/Slim.php');
require_once(BASE_DIR.'/html/includes/Slim-Extras/DateTimeFileWriter.php');
require_once(BASE_DIR.'/html/includes/api_authentication.php');
require_once(BASE_DIR.'/html/includes/api_configs.php');
require_once(BASE_DIR.'/html/includes/api_folders.php');
require_once(BASE_DIR.'/html/includes/api_labs.php');
require_once(BASE_DIR.'/html/includes/api_networks.php');
require_once(BASE_DIR.'/html/includes/api_nodes.php');
require_once(BASE_DIR.'/html/includes/api_pictures.php');
require_once(BASE_DIR.'/html/includes/api_status.php');
require_once(BASE_DIR.'/html/includes/api_textobjects.php');
require_once(BASE_DIR.'/html/includes/api_topology.php');
require_once(BASE_DIR.'/html/includes/api_uusers.php');
\Slim\Slim::registerAutoloader();

$app = new \Slim\Slim(Array(
	'mode' => 'production',
	'debug' => True,					// Change to False for production
	'log.level' => \Slim\Log::WARN,		// Change to WARN for production, DEBUG to develop
	'log.enabled' => True,
	'log.writer' => new \Slim\LogWriter(fopen('/opt/unetlab/data/Logs/api.txt', 'a'))
));

$app -> hook('slim.after.router', function () use ($app) {
	// Log all requests and responses
	$request = $app -> request;
	$response = $app -> response;

	$app -> log -> debug('Request path: ' . $request -> getPathInfo());
	$app -> log -> debug('Response status: ' . $response -> getStatus());
});

$app -> response -> headers -> set('Content-Type', 'application/json');
$app -> response -> headers -> set('X-Powered-By', 'Unified Networking Lab API');
$app -> response -> headers -> set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
$app -> response -> headers -> set('Cache-Control', 'post-check=0, pre-check=0');
$app -> response -> headers -> set('Pragma', 'no-cache');

$app -> notFound(function() use ($app) {
	$output['code'] = 404;
	$output['status'] = 'fail';
	$output['message'] = $GLOBALS['messages']['60038'];
	$app -> halt($output['code'], json_encode($output));
});

class ResourceNotFoundException extends Exception {}
class AuthenticateFailedException extends Exception {}

$db = checkDatabase();
if ($db === False) {
	// Database is not available
	$app -> map('/api/(:path+)', function() use ($app) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['90003'];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
	}) -> via('DELETE', 'GET', 'POST');
	$app -> run();
}

if (updateDatabase($db) == False) {
	// Failed to update database
	// TODO should run una tantum
	$app -> map('/api/(:path+)', function() use ($app) {
		$output['code'] = 500;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['90006'];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
	}) -> via('DELETE', 'GET', 'POST');
	$app -> run();
}

// Define output for unprivileged requests
$forbidden = Array(
	'code' => 401,
	'status' => 'forbidden',
	'message' => $GLOBALS['messages']['90032']
);

/***************************************************************************
 * Authentication
 **************************************************************************/
$app -> post('/api/auth/login', function() use ($app, $db) {
	// Login
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);	// Reading options from POST/PUT
	$cookie = genUuid();
	$output = apiLogin($db, $p, $cookie);
	if ($output['code'] == 200) {
		// User is authenticated, need to set the cookie
		$app -> setCookie('unetlab_session', $cookie, SESSION, '/api/', $_SERVER['SERVER_NAME'], False, False);
	}
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

$app -> get('/api/auth/logout', function() use ($app, $db) {
	// Logout (DELETE request does not work with cookies)
	$cookie = $app -> getCookie('unetlab_session');
	$app -> deleteCookie('unetlab_session');
	$output = apiLogout($db, $cookie);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

$app -> get('/api/auth', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		// Set 401 not 412 for this page only -> used to refresh after a logout
		$output['code'] = 401;
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (checkFolder(BASE_LAB.$user['folder']) !== 0) {
		// User has an invalid last viewed folder
		$user['folder'] = '/';
	}

	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages']['90002'];
	$output['data'] = $user;

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/*
 * TODO
$app -> put('/api/auth', function() use ($app, $db) {
	// Set tenant
	// TODO should be used by admin user on single-user mode only
});
 */

/***************************************************************************
 * Status
 **************************************************************************/
// Get system stats
$app -> get('/api/status', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages']['60001'];
	$output['data'] = Array();
	$output['data']['version'] = VERSION;
	$cmd = '/opt/qemu/bin/qemu-system-x86_64 -version | sed \'s/.* \([0-9.]*\), .*/\1/g\'';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][60044]);
		$output['data']['qemu_version'] = '';
	} else {
		$output['data']['qemu_version'] = $o[0];
	}
	$output['data']['cpu'] = apiGetCPUUsage();
	$output['data']['disk'] = apiGetDiskUsage();
	list($output['data']['cached'], $output['data']['mem']) = apiGetMemUsage();
	$output['data']['swap'] = apiGetSwapUsage();
	list(
		$output['data']['iol'],
		$output['data']['dynamips'],
		$output['data']['qemu'],
		$output['data']['docker'],
		$output['data']['vpcs']
	) = apiGetRunningWrappers();

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Stop all nodes and clear the system
$app -> delete('/api/status', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$cmd = 'sudo /opt/unetlab/wrappers/unl_wrapper -a stopall';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][60044]);
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60050'];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages']['60051'];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * List Objects
 **************************************************************************/
// Node templates
$app -> get('/api/list/templates/(:template)', function($template = '') use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (!isset($template) || $template == '') {
		// Print all available templates
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages']['60003'];
		$output['data'] = $GLOBALS['node_templates'];
	} else if (isset($GLOBALS['node_templates'][$template]) && is_file(BASE_DIR.'/html/templates/'.$template.'.php')) {
		// Template found
		include(BASE_DIR.'/html/templates/'.$template.'.php');
		$p['template'] = $template;
		$output = apiGetLabNodeTemplate($p);
	} else {
		// Template not found (or not available)
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60031'];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Network types
$app -> get('/api/list/networks', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages']['60002'];
	$output['data'] = listNetworkTypes();

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Network types
$app -> get('/api/list/roles', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages']['60041'];
	$output['data'] = listRoles();

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * Folders
 **************************************************************************/
// Get folder content
$app -> get('/api/folders/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	$s = '/'.implode('/', $path);
	$output = apiGetFolders($s);

	if ($output['status'] === 'success') {
		// Setting folder as last viewed
		$rc = updateUserFolder($db, $app -> getCookie('unetlab_session'), $s);
		if ($rc !== 0) {
			// Cannot update user folder
			$output['code'] = 500;
			$output['status'] = 'error';
			$output['message'] = $GLOBALS['messages'][$rc];
		}
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Edit (move and rename) a folder
$app -> put('/api/folders/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	// TODO must check before using p name and p path

	$event = json_decode($app -> request() -> getBody());
	$s = '/'.implode('/', $path);
	$p = json_decode(json_encode($event), True);
	$output = apiEditFolder($s, $p['path']);

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Add a new folder
$app -> post('/api/folders', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}


	// TODO must check before using p name and p path

	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);
	$output = apiAddFolder($p['name'], $p['path']);

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Delete an existing folder
$app -> delete('/api/folders/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$s = '/'.implode('/', $path);
	$output = apiDeleteFolder($s);

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * Labs
 **************************************************************************/
// Get an object
$app -> get('/api/labs/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	$s = '/'.implode('/', $path);

	$patterns[0] = '/(.+).unl.*$/';			// Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';	// Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);	// Interfere after lab_file.unl

	if (!is_file(BASE_LAB.$lab_file)) {
		// Lab file does not exists
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60000];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	try {
		$lab = new Lab(BASE_LAB.$lab_file, $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60056];
		$output['message'] = $e -> getMessage();
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/html$/', $s)) {
		$Parsedown = new Parsedown();
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages']['60054'];
		$output['data'] = $Parsedown -> text($lab -> getBody());
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/configs$/', $s)) {
		$output = apiGetLabConfigs($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/configs\/[0-9]+$/', $s)) {
		$output = apiGetLabConfig($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks$/', $s)) {
		$output = apiGetLabNetworks($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks\/[0-9]+$/', $s)) {
		$output = apiGetLabNetwork($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/links$/', $s)) {
		$output = apiGetLabLinks($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes$/', $s)) {
		$output = apiGetLabNodes($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/start$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}

		// Locking to avoid "device vnet12_20 already exists; can't create bridge with the same name"
		if (!lockFile(BASE_LAB.$lab_file)) {
			// Failed to lockFile within the time
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][60061];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiStartLabNodes($lab, $tenant);
		unlockFile(BASE_LAB.$lab_file);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/stop$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiStopLabNodes($lab, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/wipe$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiWipeLabNodes($lab, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+$/', $s)) {
		$output = apiGetLabNode($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/interfaces$/', $s)) {
		$output = apiGetLabNodeInterfaces($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/start$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiStartLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/stop$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiStopLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/wipe$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiWipeLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/topology$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		// Setting lab as last viewed
		$rc = updatePodLab($db, $tenant, $lab_file);
		if ($rc !== 0) {
			// Cannot update user lab
			$output['code'] = 500;
			$output['status'] = 'error';
			$output['message'] = $GLOBALS['messages'][$rc];
		} else {
			$output = apiGetLabTopology($lab);
		}
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/textobjects$/', $s)) {
		$output = apiGetLabTextObjects($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/textobjects\/[0-9]+$/', $s)) {
		$output = apiGetLabTextObject($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures$/', $s)) {
		$output = apiGetLabPictures($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+$/', $s)) {
		$output = apiGetLabPicture($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+\/data$/', $s)) {
		$height = 0;
		$width = 0;
		if ($app -> request() -> params('width') > 0) {
			$width = $app -> request() -> params('width');
		}
		if ($app -> request() -> params('height')) {
			$height = $app -> request() -> params('height');
		}
		$output = apiGetLabPictureData($lab, $id, $width, $height);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+\/data\/[0-9]+\/[0-9]+$/', $s)) {
		// Get Thumbnail
		$height = preg_replace('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+\/data\/\([0-9]+\)\/\([0-9]+\)$/', '$1', $s);
		$width = preg_replace('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+\/data\/\([0-9]+\)\/\([0-9]+\)$/', '$1', $s);
		$output = apiGetLabPictureData($lab, $id, $width, $height);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl$/', $s)) {
		$output = apiGetLab($lab);
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60027];
	}

	$app -> response -> setStatus($output['code']);
	if (isset($output['encoding'])) {
		// Custom encoding
		$app -> response -> headers -> set('Content-Type', $output['encoding']);
		$app -> response -> setBody($output['data']);
	} else {
		// Default encoding
		$app -> response -> setBody(json_encode($output));
	}
});

// Edit an existing object
$app -> put('/api/labs/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);	// Reading options from POST/PUT
	$s = '/'.implode('/', $path);

	$patterns[0] = '/(.+).unl.*$/';			// Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';	// Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);	// Intefer after lab_file.unl

	if (!is_file(BASE_LAB.$lab_file)) {
		// Lab file does not exists
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60000'];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	// Locking
	if (!lockFile(BASE_LAB.$lab_file)) {
		// Failed to lockFile within the time
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60061];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	try {
		$lab = new Lab(BASE_LAB.$lab_file, $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		unlockFile(BASE_LAB.$lab_file);
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		if (isset($p['count'])) {
			// count cannot be set from API
			unset($p['count']);
		}
		$output = apiEditLabNetwork($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/configs\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabConfig($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/export$/', $s)) {
		if (!in_array($user['role'], Array('admin', 'editor'))) {
			$app -> response -> setStatus($GLOBALS['forbidden']['code']);
			$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
			return;
		}
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiExportLabNodes($lab, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabNode($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/export$/', $s)) {
		if ($tenant < 0) {
			// User does not have an assigned tenant
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages']['60052'];
			$app -> response -> setStatus($output['code']);
			$app -> response -> setBody(json_encode($output));
			return;
		}
		$output = apiExportLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/interfaces$/', $s)) {
		$output = apiEditLabNodeInterfaces($lab, $id, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/textobjects\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabTextObject($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabPicture($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl$/', $s)) {
		$output = apiEditLab($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/move$/', $s)) {
		$output = apiMoveLab($lab, $p['path']);
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60027];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
	unlockFile(BASE_LAB.$lab_file);
});

// Add new lab
$app -> post('/api/labs', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}
	
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);;
	
	if (isset($p['source'])) {
		$output = apiCloneLab($p, $tenant);
	} else {
		$output = apiAddLab($p, $tenant);
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Add new object inside a lab
$app -> post('/api/labs/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);	// Reading options from POST/PUT
	$s = '/'.implode('/', $path);
	$o = False;

	$patterns[0] = '/(.+).unl.*$/';			// Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';	// Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);	// Intefer after lab_file.unl

	// Reading options from POST/PUT
	if (isset($event -> postfix) && $event -> postfix == True) $o = True;

	if (!is_file(BASE_LAB.$lab_file)) {
		// Lab file does not exists
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60000'];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	// Locking
	if (!lockFile(BASE_LAB.$lab_file)) {
		// Failed to lockFile within the time
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60061];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	try {
		$lab = new Lab(BASE_LAB.$lab_file, $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		unlockFile(BASE_LAB.$lab_file);
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks$/', $s)) {
		$output = apiAddLabNetwork($lab, $p, $o);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes$/', $s)) {
		if (isset($p['count'])) {
			// count cannot be set from API
			unset($p['count']);
		}
		$output = apiAddLabNode($lab, $p, $o);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/textobjects$/', $s)) {
		$output = apiAddLabTextObject($lab, $p, $o);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures$/', $s)) {
		// Cannot use $app -> request() -> getBody()
		$p = $_POST;
		if (!empty($_FILES)) {
			foreach ($_FILES as $file) {
				if (file_exists($file['tmp_name'])) {
					$fp = fopen($file['tmp_name'], 'r');
					$size = filesize($file['tmp_name']);
					if ($fp !== False) {
						$finfo = new finfo(FILEINFO_MIME);
						$p['data'] = fread($fp, $size);
						$p['type'] = $finfo -> buffer($p['data'], FILEINFO_MIME_TYPE);
					}
				}
			}
		}
		$output = apiAddLabPicture($lab, $p);
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60027];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
	unlockFile(BASE_LAB.$lab_file);
});

// Close a lab
$app -> delete('/api/labs/close', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if ($tenant < 0) {
		// User does not have an assigned tenant
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60052'];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	$rc = updatePodLab($db, $tenant, null);
	if ($rc !== 0) {
		// Cannot update user lab
		$output['code'] = 500;
		$output['status'] = 'error';
		$output['message'] = $GLOBALS['messages'][$rc];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages'][60053];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Delete an object
$app -> delete('/api/labs/(:path+)', function($path = array()) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$event = json_decode($app -> request() -> getBody());
	$s = '/'.implode('/', $path);

	$patterns[0] = '/(.+).unl.*$/';			// Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';	// Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);	// Intefer after lab_file.unl

	if (!is_file(BASE_LAB.$lab_file)) {
		// Lab file does not exists
		$output['code'] = 404;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60000'];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	try {
		$lab = new Lab(BASE_LAB.$lab_file, $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl$/', $s)) {
			// Delete the lab
			if (unlink(BASE_LAB.$lab_file)) {
				$output['code'] = 200;
				$output['status'] = 'success';
			} else {
				$output['code'] = 400;
				$output['status'] = 'fail';
				$output['message'] = $GLOBALS['messages'][60021];
			}
		} else {
			// Cannot delete objects on non-valid lab
			$output['code'] = 400;
			$output['status'] = 'fail';
			$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		}
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks\/[0-9]+$/', $s)) {
		$output = apiDeleteLabNetwork($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+$/', $s)) {
		$output = apiDeleteLabNode($lab, $id,$tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/textobjects\/[0-9]+$/', $s)) {
		$output = apiDeleteLabTextObject($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+$/', $s)) {
		$output = apiDeleteLabPicture($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl$/', $s)) {
		$output = apiDeleteLab($lab);
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60027];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * Users
 **************************************************************************/
// Get a user
$app -> get('/api/users/(:uuser)', function($uuser = False) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin')) && false) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	if (empty($uuser)) {
		$output = apiGetUUsers($db);
	} else {
		$output = apiGetUUser($db, $uuser);
	}
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Edit a user
$app -> put('/api/users/(:uuser)', function($uuser = False) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);	// Reading options from POST/PUT
	
	if ($user['role'] == 'editor') {
		unset($p['role']);
		unset($p['expiration']);
		unset($p['pod']);
		unset($p['pexpiration']);
	}
	$output = apiEditUUser($db, $uuser, $p);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Add a user
$app -> post('/api/users', function($uuser = False) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);	// Reading options from POST/PUT

	$output = apiAddUUser($db, $p);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Delete a user
$app -> delete('/api/users/(:uuser)', function($uuser = False) use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$output = apiDeleteUUser($db, $uuser);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * Export/Import
 **************************************************************************/
// Export labs
$app -> post('/api/export', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}
	
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);;
	
	$output = apiExportLabs($p);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Import labs
 $app -> post('/api/import', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin', 'editor'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	// Cannot use $app -> request() -> getBody()
	$p = $_POST;
	if (!empty($_FILES)) {
		foreach ($_FILES as $file) {
			$p['name'] = $file['name'];
			$p['file'] = $file['tmp_name'];
			$p['error'] = $file['name'];
		}
	}
	$output = apiImportLabs($p);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
 });

/***************************************************************************
 * Update
 **************************************************************************/
$app -> get('/api/update', function() use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	if (!in_array($user['role'], Array('admin'))) {
		$app -> response -> setStatus($GLOBALS['forbidden']['code']);
		$app -> response -> setBody(json_encode($GLOBALS['forbidden']));
		return;
	}

	$cmd = 'sudo /opt/unetlab/wrappers/unl_wrapper -a update';
	exec($cmd, $o, $rc);
	if ($rc != 0) {
		error_log(date('M d H:i:s ').'ERROR: '.$GLOBALS['messages'][60059]);
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages']['60059'];
	} else {
		$output['code'] = 200;
		$output['status'] = 'success';
		$output['message'] = $GLOBALS['messages']['60060'];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});


/***************************************************************************
 * LOGS
 **************************************************************************/
$app -> get('/api/logs/(:file)/(:lines)/(:search)', function($file = False, $lines = 10, $search="") use ($app, $db) {
	list($user, $tenant, $output) = apiAuthorization($db, $app -> getCookie('unetlab_session'));
	if ($user === False) {
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}
	

	$f = @file_get_contents("/opt/unetlab/data/Logs/" . $file);
	if ($f)
	{
		$arr = explode("\n", $f);
		if (!is_array($arr))
			$arr = array();
		$arr = array_reverse($arr);
		
		if ($search)
		{
			foreach($arr as $k=>$v )
			{
				if (strstr($v, $search) === false)
					unset($arr[$k]);
			}
		}
		
		$arr = array_slice($arr, 0 , $lines);
	}
	else
		$arr = array();
	
	$app -> response -> setStatus(200);
	$app -> response -> setBody(json_encode($arr));
});
/***************************************************************************
 * Run
 **************************************************************************/
$app -> run();
?>
