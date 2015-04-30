<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/api.php
 *
 * REST API router for UNetLab.
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
 * @version 20150428
 */

/*
 * Output of REST APIs is an extended JSend message:
 * {
 *	status: 'success' || 'fail' || 'error',
 *	data: { 'var1' : 'value1', ... },
 *	message: 'text message',
 *	code: 'NUMERIC HTTP CODE'
 * }
 */

/*
 * Testing from CLI
 *   curl -X GET -i -H "Content-type: application/json" http://127.0.0.1/api/status/mem
 *   curl -X PUT -i -H "Content-type: application/json" -d '{...}' http://127.0.0.1/api/folders/a/b)
 *   curl -X POST -i -H "Content-type: application/json" -d '{...}' http://127.0.0.1/api/folders/a/b)
 *   curl -X DELETE -i -H "Content-type: application/json" http://127.0.0.1/api/folders/a/b)
 *  In PUT and POST parameters use the following syntax: "var1":"value1", "var2":"value2", ...
 */

require_once('/opt/unetlab/html/includes/init.php');
require_once(BASE_DIR.'/html/includes/Slim/Slim.php');
require_once(BASE_DIR.'/html/includes/api_folders.php');
require_once(BASE_DIR.'/html/includes/api_labs.php');
require_once(BASE_DIR.'/html/includes/api_networks.php');
require_once(BASE_DIR.'/html/includes/api_nodes.php');
require_once(BASE_DIR.'/html/includes/api_pictures.php');
require_once(BASE_DIR.'/html/includes/api_status.php');
require_once(BASE_DIR.'/html/includes/api_topology.php');
\Slim\Slim::registerAutoloader();

$tenant = 0;

$app = new \Slim\Slim(Array(
	'mode' => 'production',
	'debug' => True,									// Change to False for production
	'log.level' => \Slim\Log::DEBUG,	// Change to WARN for production
	'log.enabled' => True,
	'log.writer' => new \Slim\LogWriter(fopen('/opt/unetlab/data/Logs/api.txt', 'a'))
));

$app -> hook('slim.after.router', function () use ($app) {
	// Log all requests and responses
	$request = $app -> request;
	$response = $app -> response;

	$app -> log -> debug('Request path: ' . $request -> getPathInfo());
	$app -> log -> debug('Response status: ' . $response -> getStatus());
	// And so on ...
});

$app -> response -> headers -> set('Content-Type', 'application/json');
$app -> response -> headers -> set('X-Powered-By', 'Unified Networking Lab API');

class ResourceNotFoundException extends Exception {}
class AuthenticateFailedException extends Exception {}

/***************************************************************************
 * Status
 **************************************************************************/
$app -> get('/api/status', function() use ($app, $tenant) {
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages']['60001'];
	$output['data'] = Array();
	$output['data']['cpu'] = apiGetCPUUsage();
	$output['data']['disk'] = apiGetDiskUsage();
	list($output['data']['cached'], $output['data']['mem']) = apiGetMemUsage();
	$output['data']['swap'] = apiGetSwapUsage();
	list(
		$output['data']['iol'],
		$output['data']['dynamips'],
		$output['data']['qemu']
	) = apiGetRunningWrappers();

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * List Objects
 **************************************************************************/
// Node templates
$app -> get('/api/list/templates/(:template)', function($template = '') use ($app, $tenant) {
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
$app -> get('/api/list/networks', function() use ($app, $tenant) {
	$output['code'] = 200;
	$output['status'] = 'success';
	$output['message'] = $GLOBALS['messages']['60002'];
	$output['data'] = listNetworkTypes();

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * Folders
 **************************************************************************/

// Get folder content
$app -> get('/api/folders/(:path+)', function($path = array()) use ($app, $tenant) {
	$s = '/'.implode('/', $path);
	$output = apiGetFolders($s);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Add a new folder
$app -> post('/api/folders', function() use ($app, $tenant) {
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);
	$output = apiAddFolder($p['name'], $p['path']);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Delete an existing folder
$app -> delete('/api/folders/(:path+)', function($path = array()) use ($app, $tenant) {
	$s = '/'.implode('/', $path);
	$output = apiDeleteFolder($s);
	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

/***************************************************************************
 * Labs
 **************************************************************************/
// Get an object
$app -> get('/api/labs/(:path+)', function($path = array()) use ($app, $tenant) {
	$s = '/'.implode('/', $path);

	$patterns[0] = '/(.+).unl.*$/';           // Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';    // Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);    // Intefer after lab_file.unl

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
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks$/', $s)) {
		$output = apiGetLabNetworks($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks\/[0-9]+$/', $s)) {
		$output = apiGetLabNetwork($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/links$/', $s)) {
		$output = apiGetLabLinks($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes$/', $s)) {
		$output = apiGetLabNodes($lab);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/start$/', $s)) {
		$output = apiStartLabNodes($lab, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/stop$/', $s)) {
		$output = apiStopLabNodes($lab, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/wipe$/', $s)) {
		$output = apiWipeLabNodes($lab, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+$/', $s)) {
		$output = apiGetLabNode($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/interfaces$/', $s)) {
		$output = apiGetLabNodeInterfaces($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/start$/', $s)) {
		$output = apiStartLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/stop$/', $s)) {
		$output = apiStopLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/wipe$/', $s)) {
		$output = apiWipeLabNode($lab, $id, $tenant);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/topology$/', $s)) {
		$output = apiGetLabTopology($lab);
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
$app -> put('/api/labs/(:path+)', function($path = array()) use ($app, $tenant) {
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);    // Reading options from POST/PUT
	$s = '/'.implode('/', $path);

	$patterns[0] = '/(.+).unl.*$/';           // Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';    // Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);    // Intefer after lab_file.unl

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
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabNetwork($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabNode($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+\/interfaces$/', $s)) {
		$output = apiEditLabNodeInterfaces($lab, $id, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/pictures\/[0-9]+$/', $s)) {
		$p['id'] = $id;
		$output = apiEditLabPicture($lab, $p);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl$/', $s)) {
		$output = apiEditLab($lab, $p);
	} else {
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][60027];
	}

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Add new lab
$app -> post('/api/labs', function() use ($app, $tenant) {
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);;
	$output = apiAddLab($p, $tenant);

	$app -> response -> setStatus($output['code']);
	$app -> response -> setBody(json_encode($output));
});

// Add new object
$app -> post('/api/labs/(:path+)', function($path = array()) use ($app, $tenant) {
	$event = json_decode($app -> request() -> getBody());
	$p = json_decode(json_encode($event), True);    // Reading options from POST/PUT
	$s = '/'.implode('/', $path);
	$o = False;

	$patterns[0] = '/(.+).unl.*$/';           // Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';    // Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);    // Intefer after lab_file.unl

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

	try {
		$lab = new Lab(BASE_LAB.$lab_file, $tenant);
	} catch(Exception $e) {
		// Lab file is invalid
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks$/', $s)) {
		$output = apiAddLabNetwork($lab, $p, $o);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes$/', $s)) {
		$output = apiAddLabNode($lab, $p, $o);
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
});

// Delete an object
$app -> delete('/api/labs/(:path+)', function($path = array()) use ($app, $tenant) {
	$event = json_decode($app -> request() -> getBody());
	$s = '/'.implode('/', $path);

	$patterns[0] = '/(.+).unl.*$/';           // Drop after lab file (ending with .unl)
	$replacements[0] = '$1.unl';
	$patterns[1] = '/.+\/([0-9]+)\/*.*$/';    // Drop after lab file (ending with .unl)
	$replacements[1] = '$1';

	$lab_file = preg_replace($patterns[0], $replacements[0], $s);
	$id = preg_replace($patterns[1], $replacements[1], $s);    // Intefer after lab_file.unl

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
		$output['code'] = 400;
		$output['status'] = 'fail';
		$output['message'] = $GLOBALS['messages'][$e -> getMessage()];
		$app -> response -> setStatus($output['code']);
		$app -> response -> setBody(json_encode($output));
		return;
	}

	if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/networks\/[0-9]+$/', $s)) {
		$output = apiDeleteLabNetwork($lab, $id);
	} else if (preg_match('/^\/[A-Za-z0-9_+\/\\s-]+\.unl\/nodes\/[0-9]+$/', $s)) {
		$output = apiDeleteLabNode($lab, $id);
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
 * Run
 **************************************************************************/
$app -> run();
?>
