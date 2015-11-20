// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/functions.js
 *
 * Functions
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
 * @version 20150909
 */

// Basename: given /a/b/c return c
function basename(path) {
	return path.replace(/\\/g,'/').replace( /.*\//, '');
}
 
// Dirname: given /a/b/c return /a/b
function dirname(path) {
	var dir = path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');
	if (dir == '') {
		return '/';
	} else {
		return dir;
	}
}

// Alert management
function addMessage(severity, message) {
	// Severity can be success (green), info (blue), warning (yellow) and danger (red)
	
	var timeout = 3000;		// by default close messges after 3 seconds
	if (severity == 'alert') timeout = 10000;
	if (severity == 'warning') timeout = 10000;
	
	if (!$('#alert_container').length) {
		// Add the frame container if not exists
		$('#lab-viewport').append('<div id="alert_container"></div>');
	}
	
    $('<div class="alert alert-' + severity.toLowerCase() + '">' + message + '</div>').prependTo('#alert_container').fadeTo(timeout, 500).slideUp(500, function() {
        $(this).alert('close');
    });
}

// Add Modal
function addModal(title, body, footer) {
	var html = '<div aria-hidden="false" style="display: block;" class="modal fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">' + body + '</div><div class="modal-footer">' + footer + '</div></div></div></div>';
	$('body').append(html);
	$('body > .modal').modal('show');
}

// Add Modal
function addModalError(message) {
	var html = '<div aria-hidden="false" style="display: block;" class="modal fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + MESSAGES[15] + '</h4></div><div class="modal-body">' + message + '</div><div class="modal-footer"></div></div></div></div>';
	$('body').append(html);
	$('body > .modal').modal('show');
}

// Add Modal
function addModalWide(title, body, footer) {
	var html = '<div aria-hidden="false" style="display: block;" class="modal modal-wide fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">' + body + '</div><div class="modal-footer">' + footer + '</div></div></div></div>';
	$('body').append(html);
	$('body > .modal').modal('show');
}

// Clone selected labs
function cloneLab(form_data) {
	var deferred = $.Deferred();
	var type = 'POST'
	var url = '/api/labs';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: created lab "' + form_data['name'] + '" from "' + form_data['source'] + '".');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Close lab
function closeLab() {
	var deferred = $.Deferred();
	var url = '/api/labs/close';
	var type = 'DELETE'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab closed.');
				LAB = null;
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Delete folder
function deleteFolder(path) {
	var deferred = $.Deferred();
	var type = 'DELETE'
	var url = '/api/folders' + path;
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: folder "' + path + '" deleted.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}
	
// Delete lab
function deleteLab(path) {
	var deferred = $.Deferred();
	var type = 'DELETE'
	var url = '/api/labs' + path;
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab "' + path + '" deleted.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Delete network
function deleteNetwork(id) {
	var deferred = $.Deferred();
	var type = 'DELETE'
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = '/api/labs' + lab_filename + '/networks/' + id;
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: node deleted.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Delete node
function deleteNode(id) {
	var deferred = $.Deferred();
	var type = 'DELETE'
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = '/api/labs' + lab_filename + '/nodes/' + id;
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: node deleted.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Delete user
function deleteUser(path) {
	var deferred = $.Deferred();
	var type = 'DELETE'
	var url = '/api/users/' + path;
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user "' + path + '" deleted.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Export selected folders and labs
function exportObjects(form_data) {
	var deferred = $.Deferred();
	var type = 'POST'
	var url = '/api/export';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: objects exported into "' + data['data'] + '".');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// HTML Form to array
function form2Array(form_name) {
	var form_array = {};
	$('form :input[name^="' + form_name + '["]').each(function(id, object) {
		// INPUT name is in the form of "form_name[value]", get value only
		form_array[$(this).attr('name').substr(form_name.length + 1, $(this).attr('name').length - form_name.length - 2)] = $(this).val();
	});
	return form_array;
}

// Get JSon message from HTTP response
function getJsonMessage(response) {
	var message = '';
	try {
		message = JSON.parse(response)['message'];
		code = JSON.parse(response)['code'];
		if (code == 412) {
			// if 412 should redirect (user timed out)
			window.setTimeout(function() {
				location.reload();
			}, 2000);
		}
	} catch(e) {
		if (response != '') {
			message = response;
		} else {
			message = 'Undefined message, check if the UNetLab VM is powered on. If it is, see <a href="/Logs" target="_blank">logs</a>.';
		}
	}
	return message;
}

// Get lab info
function getLabInfo(lab_filename) {
	var deferred = $.Deferred();
	var url = '/api/labs' + lab_filename;
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab "' + lab_filename + '" found.');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get lab body
function getLabBody() {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = '/api/labs' + lab_filename + '/html';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab "' + lab_filename + '" body found.');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get lab endpoints
function getLabLinks() {
	var lab_filename = $('#lab-viewport').attr('data-path');
	var deferred = $.Deferred();
	var url = '/api/labs' + lab_filename + '/links';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got available links(s) from lab "' + lab_filename + '".');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get lab networks
function getNetworks(network_id) {
	var lab_filename = $('#lab-viewport').attr('data-path');
	var deferred = $.Deferred();
	if (network_id != null) {
		var url = '/api/labs' + lab_filename + '/networks/' + network_id;
	} else {
		var url = '/api/labs' + lab_filename + '/networks';
	}
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got network(s) from lab "' + lab_filename + '".');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get available network types
function getNetworkTypes() {
	var deferred = $.Deferred();
	var url = '/api/list/networks';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got network types.');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get lab nodes
function getNodes(node_id) {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	if (node_id != null) {
		var url = '/api/labs' + lab_filename + '/nodes/' + node_id;
	} else {
		var url = '/api/labs' + lab_filename + '/nodes';
	}
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got node(s) from lab "' + lab_filename + '".');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get lab node interfaces
function getNodeInterfaces(node_id) {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/interfaces';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got node(s) from lab "' + lab_filename + '".');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get lab topology
function getTopology() {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = '/api/labs' + lab_filename + '/topology';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got topology from lab "' + lab_filename + '".');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get roles
function getRoles() {
	var deferred = $.Deferred();
	var form_data = {};
	var url = '/api/list/roles';
	var type = 'GET';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got roles.');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get system stats
function getSystemStats() {
	var deferred = $.Deferred();
	var url = '/api/status';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: system stats.');
                data['data']['cpu'] = data['data']['cpu'] / 100;
                data['data']['disk'] = data['data']['disk'] / 100;
                data['data']['mem'] = data['data']['mem'] / 100;
                data['data']['cached'] = data['data']['cached'] / 100;
                data['data']['swap'] = data['data']['swap'] / 100;
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get templates
function getTemplates(template) {
	var deferred = $.Deferred();
	var url = (template == null) ? '/api/list/templates/': '/api/list/templates/' + template;
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got template(s).');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get user info
function getUserInfo() {
	var deferred = $.Deferred();
	var url = '/api/auth';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user is authenticated.');
				EMAIL = data['data']['email'];
				FOLDER = (data['data']['folder'] == null) ? '/' : data['data']['folder'];
				LAB = data['data']['lab'];
				LANG = data['data']['lang'];
				NAME = data['data']['name'];
				ROLE = data['data']['role'];
				TENANT = data['data']['tenant'];
				USERNAME = data['data']['username'];
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Get users
function getUsers(user) {
	var deferred = $.Deferred();
	if (user != null) {
		var url = '/api/users/' + user;
	} else {
		var url = '/api/users/';
	}
	var type = 'GET';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got user(s).');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Logging
function logger(severity, message) {
	if (DEBUG >= severity) {
		console.log(message);
	}
}

// Logout user
function logoutUser() {
	var deferred = $.Deferred();
	var url = '/api/auth/logout';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user is logged off.');
				deferred.resolve();
			} else {
				// Authentication error
				logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Authentication error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Move folder inside a folder
function moveFolder(folder, path) {
	var deferred = $.Deferred();
	var type = 'PUT';
	var url = '/api/folders' + folder;
	var form_data = {};
	form_data['path'] = (path == '/') ? '/' + basename(folder) : path + '/' + basename(folder);
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: folder is moved.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Move lab inside a folder
function moveLab(lab, path) {
	var deferred = $.Deferred();
	var type = 'PUT';
	var url = '/api/labs' + lab + '/move';
	var form_data = {};
	form_data['path'] = path;
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab is moved.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Post login
function postLogin() {
	if (UPDATEID != null) {
		// Stop updating node_status
		clearInterval(UPDATEID);
	}
	
	if (LAB == null) {
		logger(1, 'DEBUG: loading folder "' + FOLDER + '".');
		printPageLabList(FOLDER);
	} else {
		logger(1, 'DEBUG: loading lab "' + LAB + '".');
		printPageLabOpen(LAB);
				
		// Update node status
        UPDATEID = setInterval('printLabStatus("' + LAB + '")', 5000);
	}
}

// Set network position
function setNetworkPosition(network_id, left, top) {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var form_data = {}
	form_data['left'] = left;
	form_data['top'] = top;
	var url = '/api/labs' + lab_filename + '/networks/' + network_id;
	var type = 'PUT'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: network position updated.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
			addMessage(data['status'], data['message']);

		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Set node position
function setNodePosition(node_id, left, top) {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var form_data = {}
	form_data['left'] = left;
	form_data['top'] = top;
	var url = '/api/labs' + lab_filename + '/nodes/' + node_id;
	var type = 'PUT'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: node position updated.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Start node(s)
function start(node_id) {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = (node_id == null) ? '/api/labs' + lab_filename + '/nodes/start' : '/api/labs' + lab_filename + '/nodes/' + node_id + '/start';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: node(s) started.');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Stop node(s)
function stop(node_id) {
	var deferred = $.Deferred();
	var lab_filename = $('#lab-viewport').attr('data-path');
	var url = (node_id == null) ? '/api/labs' + lab_filename + '/nodes/stop' : '/api/labs' + lab_filename + '/nodes/' + node_id + '/stop';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: node(s) stopped.');
				deferred.resolve(data['data']);
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

// Stop all nodes
function stopAll() {
	var deferred = $.Deferred();
	var type = 'DELETE'
	var url = '/api/status';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: stopped all nodes.');
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data['message']);
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject(message);
		}
	});
	return deferred.promise();
}

/***************************************************************************
 * Print forms and pages
 **************************************************************************/
// Context menu
function printContextMenu(title, body, pageX, pageY) {
    var menu = '<div id="context-menu" class="collapse clearfix dropdown">';
    menu += '<ul class="dropdown-menu" role="menu"><li role="presentation" class="dropdown-header">' + title + '</li>' + body + '</ul></div>';

	$('body').append(menu);
	
	// Set initial status
	$('.menu-interface, .menu-edit').slideToggle();
	$('.menu-interface, .menu-edit').hide();
	
	// Calculating position
    if (pageX + $('#context-menu').width() > $(window).width()) {
        // Dropright
        var left = pageX - $('#context-menu').width();
    } else {
        // Dropleft
        var left = pageX;
    }
	if ($('#context-menu').height() > $(window).height()) {
		// Page is too short, drop down by default
        var top = 0;
	} else if ($(window).height() - pageY >= $('#context-menu').height()) {
        // Dropdown if enough space
        var top = pageY;
    } else {
		// Dropup
        var top = $(window).height() - $('#context-menu').height();
    }

    // Setting position via CSS
    $('#context-menu').css({
        left: left + 'px',
		maxHeight: $('#context-menu').height(),
        top: top + 'px',
    });
}

// Folder form
function printFormFolder(action, values) {
	var name = (values['name'] != null) ? values['name'] : '';
	var path = (values['path'] != null) ? values['path'] : '';
	var original = (path == '/') ? '/' + name : path + '/' + name;
	var submit = (action == 'add') ? MESSAGES[17] : MESSAGES[21];
	var title = (action == 'add') ? MESSAGES[4] : MESSAGES[10];
	if (original == '/' && action == 'rename') {
		addModalError(MESSAGES[51]);
	} else {
		var html = '<form id="form-folder-' + action + '" class="form-horizontal form-folder-' + action + '"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="folder[path]" value="' + path + '" disabled type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control autofocus" name="folder[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><input class="form-control" name="folder[original]" value="' + original + '" type="hidden"/><button type="submit" class="btn btn-aqua">' + submit + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
		logger(1, 'DEBUG: popping up the folder-' + action + ' form.');
		addModal(title, html, '');
		validateFolder();
	}
}
 
// Import external labs
function printFormImport(path) {
	var html = '<form id="form-import" class="form-horizontal form-import"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="import[path]" value="' + path + '" disabled type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[2] + '</label><div class="col-md-5"><input class="form-control" name="import[local]" value="" disabled="" placeholder="' + MESSAGES[25] + '" "type="text"/></div></div><div class="form-group"><div class="col-md-7 col-md-offset-3"><span class="btn btn-default btn-file btn-aqua">' + MESSAGES[23] + ' <input class="form-control" name="import[file]" value="" type="file"></span> <button type="submit" class="btn btn-aqua">' + MESSAGES[24] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
	logger(1, 'DEBUG: popping up the import form.');
	addModal(MESSAGES[9], html, '');
	validateImport();
}

// Add a new lab
function printFormLab(action, values) {
	var path = (values['path'] != null) ? values['path'] : '';
	var name = (values['name'] != null) ? values['name'] : '';
	var version = (values['version'] != null) ? values['version'] : '';
	var author = (values['author'] != null) ? values['author'] : '';
	var description = (values['description'] != null) ? values['description'] : '';
	var body = (values['body'] != null) ? values['body'] : '';
	
	var html = '<form id="form-lab-' + action + '" class="form-horizontal form-lab-' + action + '"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="lab[path]" value="' + path + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control autofocus" name="lab[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[26] + '</label><div class="col-md-5"><input class="form-control" name="lab[version]" value="' + version + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Author</label><div class="col-md-5"><input class="form-control" name="lab[author]" value="' + author + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[27] + '</label><div class="col-md-5"><textarea class="form-control" name="lab[description]">' + description + '</textarea></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[88] + '</label><div class="col-md-5"><textarea class="form-control" name="lab[body]">' + body + '</textarea></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
	logger(1, 'DEBUG: popping up the lab-add form.');
	addModal(MESSAGES[5], html, '');
	validateLabInfo();
}

// Network Form
function printFormNetwork(action, values) {
	var id = (values == null || values['id'] == null) ? '' : values['id']; 
	var left = (values == null || values['left'] == null) ? '' : values['left']; 
	var name = (values == null || values['name'] == null) ? 'Net' : values['name']; 
	var top = (values == null || values['top'] == null) ? '' : values['top']; 
	var type = (values == null || values['type'] == null) ? '' : values['type'];
	var title = (action == 'add') ? MESSAGES[89] : MESSAGES[90];
	
	$.when(getNetworkTypes()).done(function(network_types) {
		// Read privileges and set specific actions/elements
		var html = '<form id="form-network-' + action + '" class="form-horizontal">';
		if (action == 'add') {
			// If action == add -> print the nework count input
			html += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[114] + '</label><div class="col-md-5"><input class="form-control" name="network[count]" value="1" type="text"/></div></div>';
		} else {
			// If action == edit -> print the network ID
			html += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[92] + '</label><div class="col-md-5"><input class="form-control" disabled name="network[id]" value="' + id + '" type="text"/></div></div>';
		}
		html += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[103] + '</label><div class="col-md-5"><input class="form-control autofocus" name="network[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[95] + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="network[type]" data-live-search="true" data-style="selectpicker-button">';
		$.each(network_types, function(key, value) {
			// Print all network types
			var type_selected = (key == type) ? 'selected ' : '';
			html += '<option ' + type_selected + 'value="' + key + '">' + value + '</option>';
		});
		html += '</select></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[93] + '</label><div class="col-md-5"><input class="form-control" name="network[left]" value="' + left + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[94] + '</label><div class="col-md-5"><input class="form-control" name="network[top]" value="' + top + '" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form></form>';
		
		// Show the form
		addModal(title, html, '');
		$('.selectpicker').selectpicker();
		$('.autofocus').focus();
	});
}

// Node form
function printFormNode(action, values) {
	var id = (values == null || values['id'] == null) ? null : values['id']; 
	var left = (values == null || values['left'] == null) ? null : values['left']; 
	var top = (values == null || values['top'] == null) ? null : values['top']; 
	var template = (values == null || values['template'] == null) ? null : values['template']; 
	
	var title = (action == 'add') ? MESSAGES[85] : MESSAGES[86];
	var template_disabled = (values == null || values['template'] == null) ? '' : 'disabled ';
	
	$.when(getTemplates(null)).done(function(templates) {
		var html = '';
		html += '<form id="form-node-' + action + '" class="form-horizontal"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[84] + '</label><div class="col-md-5"><select id="form-node-template" class="selectpicker form-control" name="node[template]" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[102] + '</option>';
		$.each(templates, function(key, value) {
			// Adding all templates
			html += '<option value="' + key + '">' + value + '</option>';
		});
		html += '</select></div></div><div id="form-node-data"></div><div id="form-node-buttons"></div></form>';
		
		// Show the form
		addModal(title, html, '');
		$('.selectpicker').selectpicker();
		
		$('#form-node-template').change(function(e2) {
			template = $(this).find("option:selected").val();
			if (template != '') {
				// Getting template only if a valid option is selected (to avoid requests during typewriting)
				$.when(getTemplates(template), getNodes(id)).done(function(template_values, node_values) {
					// TODO: this event is called twice
					id = (id == null)? '' : id;
					var html_data = '<input name="node[type]" value="' + template_values['type'] + '" type="hidden"/>';
					if (action == 'add') {
						// If action == add -> print the nework count input
						html_data += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[113] + '</label><div class="col-md-5"><input class="form-control" name="node[count]" value="1" type="text"/></div></div>';
					} else {
						// If action == edit -> print the network ID
						html_data += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[92] + '</label><div class="col-md-5"><input class="form-control" disabled name="node[id]" value="' + id + '" type="text"/></div></div>';
					}
					$.each(template_values['options'], function(key, value) {
						// Print all options form template
						var value_set = (node_values != null && node_values[key]) ? node_values[key] : value['value'];
						if (value['type'] == 'list') {
							// Option is a list
							html_data += '<div class="form-group"><label class="col-md-3 control-label">' + value['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="node[' + key + ']" data-style="selectpicker-button">';
							$.each(value['list'], function(list_key, list_value) {
								var selected = (list_key == value_set)? 'selected ' : '';
								html_data += '<option ' + selected + 'value="' + list_key + '">' + list_value + '</option>';
							});
							html_data += '</select></div>';
							html_data += '</div>';
						} else {
							// Option is standard
							html_data += '<div class="form-group"><label class="col-md-3 control-label">' + value['name'] + '</label><div class="col-md-5"><input class="form-control' + ((key == 'name') ? ' autofocus' : '') + '" name="node[' + key + ']" value="' + value_set + '" type="text"/></div></div>';
						}
					});
					html_data += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[93] + '</label><div class="col-md-5"><input class="form-control" name="node[left]" value="' + left + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[94] + '</label><div class="col-md-5"><input class="form-control" name="node[top]" value="' + top + '" type="text"/></div></div>';
					
					// Show the buttons
					$('#form-node-buttons').html('<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div>');
					
					// Show the form
					$('#form-node-data').html(html_data);
					$('.selectpicker').selectpicker();
					$('.autofocus').focus();
					validateNode();
				}).fail(function(message1, message2) {
					// Cannot get data
					if (message1 != null) {
						addModalError(message1);
					} else {
						addModalError(message2)
					};
				});
			}
		});
		
		if (action == 'edit') {
			// If editing a node, disable the select and trigger
			$('#form-node-template').prop('disabled', 'disabled');
			$('#form-node-template').val(template).change();
		}
		
	}).fail(function(message) {
		// Cannot get data
		addModalError(message);
	});
}

// Node interfaces
function printFormNodeInterfaces(values) {
	$.when(getLabLinks()).done(function(links) {
		var html = '<form id="form-node-connect" class="form-horizontal">';
		html += '<input name="node_id" value="' + values['node_id'] + '" type="hidden"/>';
		if (values['sort'] == 'iol') {
			// IOL nodes need to reorder interfaces
			// i = x/y with x = i % 16 and y = (i - x) / 16
			var iol_interfc = {};
			$.each(values['ethernet'], function(interfc_id, interfc) {
				var x = interfc_id % 16;
				var y = (interfc_id - x) / 16;
				iol_interfc[4 * x + y] = '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
				$.each(links['ethernet'], function(link_id, link) {
					var link_selected = (interfc['network_id'] == link_id) ? 'selected ' : '';
					iol_interfc[4 * x + y] += '<option ' + link_selected + 'value="' + link_id + '">' + link + '</option>';
				});
				iol_interfc[4 * x + y] += '</select></div></div>';
			});
			$.each(iol_interfc, function(key, value) {
				html += value;
			});
		} else {
			$.each(values['ethernet'], function(interfc_id, interfc) {
				html += '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
				$.each(links['ethernet'], function(link_id, link) {
					var link_selected = (interfc['network_id'] == link_id) ? 'selected ' : '';
					html += '<option ' + link_selected + 'value="' + link_id + '">' + link + '</option>';
				});
				html += '</select></div></div>';
			});
		}
		if (values['sort'] == 'iol') {
			// IOL nodes need to reorder interfaces
			// i = x/y with x = i % 16 and y = (i - x) / 16
			var iol_interfc = {};
			$.each(values['serial'], function(interfc_id, interfc) {
				var x = interfc_id % 16;
				var y = (interfc_id - x) / 16;
				iol_interfc[4 * x + y] = '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
				$.each(links['serial'], function(node_id, serial_link) {
					if (values['node_id'] != node_id) {
						$.each(serial_link, function(link_id, link) {
							var link_selected = (interfc['remote_id'] + ':' + interfc['remote_if'] == node_id + ':' + link_id) ? 'selected ' : '';
							iol_interfc[4 * x + y] += '<option ' + link_selected + 'value="' + node_id + ':' + link_id + '">' + link + '</option>';
						});
					}
				});
				iol_interfc[4 * x + y] += '</select></div></div>';
			});
			$.each(iol_interfc, function(key, value) {
				html += value;
			});
		} else {
			$.each(values['serial'], function(interfc_id, interfc) {
				html += '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
				$.each(links['serial'], function(node_id, serial_link) {
					if (values['node_id'] != node_id) {
						$.each(serial_link, function(link_id, link) {
							var link_selected = '';
							html += '<option ' + link_selected + 'value="' + link_id + '">' + link + '</option>';
						});
					}
				});
				html += '</select></div></div>';
			});
		}
		
		html += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
		
		addModal(MESSAGES[116], html, '');
		$('.selectpicker').selectpicker();
	}).fail(function(message) {
		// Cannot get data
		addModalError(message);
	});
}

// User form
function printFormUser(action, values) {
	$.when(getRoles()).done(function(roles) {
		// Got data
		var username = (values['username'] != null) ? values['username'] : '';
		var name = (values['name'] != null) ? values['name'] : '';
		var email = (values['email'] != null) ? values['email'] : '';
		var role = (values['role'] != null) ? values['role'] : '';
		var expiration = (values['expiration'] != null && values['expiration'] != -1) ? $.datepicker.formatDate('yy-mm-dd', new Date(values['expiration'] * 1000)) : '';
		var pod = (values['pod'] != null && values['pod'] != -1) ? values['pod'] : '';
		var pexpiration = (values['pexpiration'] != null && values['pexpiration'] != -1) ? $.datepicker.formatDate('yy-mm-dd', new Date(values['pexpiration'] * 1000)) : '';
		var submit = (action == 'add') ? MESSAGES[17] : MESSAGES[47];
		var title = (action == 'add') ? MESSAGES[34] : MESSAGES[48] + ' ' + username;
		var user_disabled = (action == 'add') ? '' : 'disabled ';
		var html = '<form id="form-user-' + action + '" class="form-horizontal form-user-' + action + '"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[44] + '</label><div class="col-md-5"><input class="form-control autofocus" ' + user_disabled + 'name="user[username]" value="' + username + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control" name="user[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[28] + '</label><div class="col-md-5"><input class="form-control" name="user[email]" value="' + email+ '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[45] + '</label><div class="col-md-5"><input class="form-control" name="user[password]" value="" type="password"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[29] + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="user[role]" data-live-search="true">';
		$.each(roles, function(key, value) {
			var role_selected = (role == key) ? 'selected ' : '';
			html += '<option ' + role_selected + 'value="' + key + '">' + value + '</option>';
		});
		html += '</select></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[30] + '</label><div class="col-md-5"><input class="form-control" name="user[expiration]" value="' + expiration + '" type="text"/></div></div><h4>' + MESSAGES[46] + '</h4><div class="form-group"><label class="col-md-3 control-label">POD</label><div class="col-md-5"><input class="form-control" name="user[pod]" value="' + pod + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[30] + '</label><div class="col-md-5"><input class="form-control" name="user[pexpiration]" value="' + pexpiration + '" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + submit + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
		addModal(title, html, '');
		validateUser();
	}).fail(function(message) {
		// Cannot get data
		addModalError(message);
	});
}

// Print lab preview section
function printLabPreview(lab_filename) {
	$.when(getLabInfo(lab_filename)).done(function(lab) {
		var html = '<h1>' + lab['name'] + ' v' + lab['version'] + '</h1>';
		if (lab['author'] != null) {
			html += '<h2>by ' + lab['author'] + '</h2>';
		}
		html += '<p><code>' + lab['id'] + '</code></p>';
		if (lab['description'] != null) {
			html += '<p>' + lab['description'] + '</p>';
		}
		html += '<button class="action-labopen btn btn-aqua" type="button" data-path="' + lab_filename + '">' + MESSAGES[22] + '</button>';
		$('#list-title-info span').html(lab['filename'].replace(/\\/g,'/').replace(/.*\//, ''));
		$('#list-info').html(html);
	}).fail(function(message) {
		addModalError(message);
	});
}

// Print lab topology
function printLabTopology() {
	var lab_filename = $('#lab-viewport').attr('data-path');
	$('#lab-viewport').empty();
	$.when(getNetworks(null), getNodes(null), getTopology()).done(function(networks, nodes, topology) {
		$.each(networks, function(key, value) {
			if (value['type'] != 'cloud') {
				var icon = 'lan.png';
			} else {
				var icon = 'cloud.png';
			}
			$('#lab-viewport').append('<div id="network' + value['id'] + '" class="context-menu network network' + value['id'] + ' network_frame unused" style="top: ' + value['top'] + 'px; left: ' + value['left'] + 'px" data-path="' + value['id'] + '" data-name="' + value['name'] + '"><img src="/images/' + icon + '"/><div class="network_name">' + value['name'] + '</div></div>');
		});
		$.each(nodes, function(key, value) {
			$('#lab-viewport').append('<div id="node' + value['id'] + '" class="context-menu node node' + value['id'] + ' node_frame" style="top: ' + value['top'] + 'px; left: ' + value['left'] + 'px;" data-path="' + value['id'] + '" data-name="' + value['name'] + '"><a href="' + value['url'] + '"><img src="/images/icons/' + value['icon'] + '"/></a><div class="node_name"><i class="node' + value['id'] + '_status"></i> ' + value['name'] + '</div></div>');
		});
		
		// Drawing topology
		jsPlumb.ready(function() {
			// Defaults
			jsPlumb.importDefaults({
				Anchor: 'Continuous',
				Connector: ['Straight'],
				Endpoint: 'Blank',
				PaintStyle: {lineWidth: 2, strokeStyle: '#58585a'},
				cssClass: 'link'
			});
			
			// Create jsPlumb topology
			var lab_topology = jsPlumb.getInstance();

			// Read privileges and set specific actions/elements
			if (ROLE == 'admin' || ROLE == 'editor') {
				// Nodes and networks are draggable within a grid
				lab_topology.draggable($('.node_frame, .network_frame'), { grid: [20, 20] });
			}
			
			$.each(topology, function(id, link) {
				var type = link['type'];
				var source = link['source'];
				var source_label = link['source_label'];
				var destination = link['destination'];
				var destination_label = link['destination_label'];

				if (type == 'ethernet') {
					if (source_label != '') {
						var src_label = [ "Label", { label: source_label, location: 0.15, cssClass: 'node_interface ' + source + ' ' + destination } ];
					} else {
						var src_label = [ "Label", Object() ];
					}
					if (destination_label != '') {
						var dst_label = [ "Label", { label: destination_label, location: 0.85, cssClass: 'node_interface ' + source + ' ' + destination } ];
					} else {
						var dst_label = [ "Label", Object() ];
					}
					
					jsPlumb.connect({
						source: source,       // Must attach to the IMG's parent or not printed correctly
						target: destination,  // Must attach to the IMG's parent or not printed correctly
						cssClass: source + ' ' + destination + ' frame_ethernet',
						overlays: [ src_label, dst_label ],
					});
				} else {
					var src_label = [ "Label", { label: source_label, location: 0.15, cssClass: 'node_interface ' + source + ' ' + destination } ];
					var dst_label = [ "Label", { label: destination_label, location: 0.85, cssClass: 'node_interface ' + source + ' ' + destination } ];
					
					jsPlumb.connect({
						source: source,       // Must attach to the IMG's parent or not printed correctly
						target: destination,  // Must attach to the IMG's parent or not printed correctly
						cssClass: source + " " + destination + ' frame_serial',
						paintStyle : { lineWidth : 2, strokeStyle : "#ffcc00" },
						overlays: [ src_label, dst_label ]
					});
				}

				// If destination is a network, remove the 'unused' class
				if (destination.substr(0, 7) == 'network') {
					$('.' + destination).removeClass('unused');
				}
			});

			// Remove unused elements
			// $('.unused').remove();

			// Move elements under the topology node
			$('._jsPlumb_connector, ._jsPlumb_overlay, ._jsPlumb_endpoint_anchor_').detach().appendTo('#lab-viewport');
		});
	}).fail(function(message1, message2, message3) {
		if (message1 != null) {
			addModalError(message1);
		} else if (message2 != null) {
			addModalError(message2)
		} else {
			addModalError(message3)
		};
	});
}

// Display lab status
function printLabStatus() {
	logger(1, 'DEBUG: updating node status');
	$.when(getNodes(null)).done(function(nodes) {
		$.each(nodes, function(node_id, node) {
			if (node['status'] == 0) {
				// Stopped
				$('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-stop');
			} else if (node['status'] == 1) {
				// Started
				$('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-play');
			} else if (node['status'] == 2) {
				// Building
				$('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-flash');
			}
		});
	}).fail(function(message) {
		addMessage('danger', message);
	});
}

// Display all networks in a table
function printListNetworks(networks) {
	logger(1, 'DEBUG: printing network list');
	var body = '<div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[92] + '</th><th>' + MESSAGES[19] + '</th><th>' + MESSAGES[95] + '</th><th>' + MESSAGES[97] + '</th><th>' + MESSAGES[99] + '</th></tr></thead><tbody>';
	$.each(networks, function(key, value) {
		body += '<tr class="network' + value['id'] + '"><td>' + value['id'] + '</td><td>' + value['name'] + '</td><td>' + value['type'] + '</td><td>' + value['count'] + '</td><td><a class="action-networkedit" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="#" title="' + MESSAGES[71] + '"><i class="glyphicon glyphicon-edit"></i></a><a class="action-networkdelete" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="#" title="' + MESSAGES[65] + '"><i class="glyphicon glyphicon-trash"></i></a></td></tr>';
	});
	body += '</tbody></table></div>';
	addModalWide(MESSAGES[96], body, '');
}

// Display all nodes in a table
function printListNodes(nodes) {
	logger(1, 'DEBUG: printing node list');
	var body = '<div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[92] + '</th><th>' + MESSAGES[19] + '</th><th>' + MESSAGES[111] + '</th><th>' + MESSAGES[119] + '</th><th>' + MESSAGES[105] + '</th><th>' + MESSAGES[106] + '</th><th>' + MESSAGES[107] + '</th><th>' + MESSAGES[108] + '</th><th>' + MESSAGES[109] + '</th><th>' + MESSAGES[110] + '</th><th>' + MESSAGES[112] + '</th><th>' + MESSAGES[99] + '</th></tr></thead><tbody>';
	$.each(nodes, function(key, value) {
		var cpu = (value['cpu'] != null) ? value['cpu'] : '';
		var ethernet = (value['ethernet'] != null) ? value['ethernet'] : '';
		var idlepc = (value['idlepc'] != null) ? value['idlepc'] : '';
		var image = (value['image'] != null) ? value['image'] : '';
		var nvram = (value['nvram'] != null) ? value['nvram'] : '';
		var serial = (value['serial'] != null) ? value['serial'] : '';
		body += '<tr class="node' + value['id'] + '"><td>' + value['id'] + '</td><td>' + value['name'] + '</td><td>' + value['template'] + '</td><td>' + value['image'] + '</td><td>' + cpu + '</td><td>' + idlepc + '</td><td>' + nvram + '</td><td>' + value['ram'] + '</td><td>' + ethernet + '</td><td>' + serial + '</td><td>' + value['console'] + '</td><td><a class="action-nodeedit" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="#" title="' + MESSAGES[71] + '"><i class="glyphicon glyphicon-edit"></i></a><a class="action-nodedelete" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="#" title="' + MESSAGES[65] + '"><i class="glyphicon glyphicon-trash"></i></a></td></tr>';
	});
	body += '</tbody></table></div>';
	addModalWide(MESSAGES[118], body, '');
}

// Print Authentication Page
function printPageAuthentication() {
	var html = '<div class="row full-height"><div class="col-md-5 col-lg-5 full-height" id="auth-left"><div class="middle"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img class="response" alt="Logo RR" src="/themes/default/images/logo-rr.png" /></div></div><!-- <div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img class="response" alt="Signup Icon" src="/themes/default/images/button-signup.png"></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">to access more features</div></div> --><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2 white">Existing user...</div></div><form id="form-login"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[username]" placeholder="USERNAME" type="text" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[password]" placeholder="PASSWORD" type="password" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input alt="Login Icon" src="/themes/default/images/button-login.png" type="image" /></div></div></form></div></div><div class="col-md-7 col-lg-7" id="auth-right"><div id="logo-angular"><img class="response" alt="Logo Angular" src="/themes/default/images/logo-angular.png" /></div><div id="logo-ad"><img class="response" alt="Logo AD" src="/themes/default/images/logo-ad.png" /></div><div id="logo-text"><h1>Unified Networking Lab</h1><p>UNetLab can be considered the next major version of<br>iou-web, but the software has been rewritten from<br>scratch. The major advantage over GNS3 and<br>iou-web itself is about multi-hypervisor<br>support within a single entity. UNetLab<br>allows to design labs using IOU, Dy-<br>namips and QEMU nodes without<br>dealing with multi virtual ma-<br>chines: everything run in-<br>side a UNetLab host,<br>and a lab is a single<br>file including all<br>information<br>needed.</p></div></div></div>'
	$('#body').html(html);
}

// Print lab list page
function printPageLabList(folder) {
	var html = '';
	var url = '/api/folders' + folder;
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: folder "' + folder + '" found.');
				
				// Navbar: top
				html += '<nav id="navbar-top" class="hidden-xs hidden-sm navbar navbar-static-top"><div class="container col-md-12 col-lg-12"><div id="logo-main" class="col-md-3 col-lg-3"><img alt="Logo" class="img-responsive" src="/themes/default/images/logo_rr.png"/></div><div class="navbar-collapse collapse"><ul class="nav navbar-nav navbar-right"><li class="navbar-item-aqua"><a href="https://unetlab.freshdesk.com/support/tickets/new" target="_blank"">Help</a></li><li class="navbar-item-grey"><a href="http://www.unetlab.com/" target="_blank">About</a></li><li class="navbar-item-grey"><a href="http://forum.802101.com/forum39.html" target="_blank">Forum</a></li></ul></div></div></nav>';

				// Navbar: main
				html += '<nav id="navbar-main" class="navbar navbar-static-top"><div class="container col-md-12 col-lg-12"><div id="navbar-main-text" class="hidden-xs hidden-sm col-md-3 col-lg-3">by Andrea Dainese</div><div id="navbar-main-spacer" class="hidden-xs hidden-sm"></div><div class="navbar-collapse collapse"><ul class="col-md-9 col-lg-9 nav navbar-nav"><li class="item-first lab-list"><a class="action-lablist" href="#">' + MESSAGES[11] + '</a></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Actions <span class="caret"></span></a><ul id="actions-menu" class="dropdown-menu"><li><a href="#">&lt;' + MESSAGES[3] + '&gt;</a></li></ul></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item usermgmt"><a class="action-usermgmt" href="#">' + MESSAGES[12] + '</a></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item sysstatus"><a class="action-sysstatus" href="#">' + MESSAGES[13] + '</a></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item"><a class="action-logout item" href="#"><i class="glyphicon glyphicon-log-out"></i> ' + MESSAGES[14] + '</a></li></ul></div></div></nav>';

				// Main: title
				html += '<div id="main-title" class="container col-md-12 col-lg-12"><div class="row row-eq-height"><div id="list-title-folders" class="col-md-3 col-lg-3"><span title="' + folder + '">' + MESSAGES[0] + ' ' + folder + '</span></div><div id="list-title-labs" class="col-md-3 col-lg-3"><span>' + MESSAGES[1] + '</span></div><div id="list-title-info" class="col-md-6 col-lg-6"><span></span></div></div></div>';
				
				// Main
				html += '<div id="main" class="container col-md-12 col-lg-12"><div class="fill-height row row-eq-height"><div id="list-folders" class="col-md-3 col-lg-3" data-path="' + folder + '"><ul></ul></div><div id="list-labs" class="col-md-3 col-lg-3"><ul></ul></div><div id="list-info" class="col-md-6 col-lg-6"></div></div></div>';
				
				// Footer
				html += '';
				
				// Adding to the page
				$('#body').html(html);
				
				// Adding all folders
				$.each(data['data']['folders'], function(id, object) {
					$('#list-folders > ul').append('<li><a class="folder action-folderopen" data-path="' + object['path'] + '" href="#" title="Double click to open, single click to select.">' + object['name'] + '</a></li>');
				});

				// Adding all labs
				$.each(data['data']['labs'], function(id, object) {
					$('#list-labs > ul').append('<li><a class="lab action-labpreview" data-path="' + object['path'] + '" href="#" title="Double click to open, single click to select.">' + object['file'] + '</a></li>');
				});
				
				// Extend height to the bottom if shorter
				if ($('#main').height() < window.innerHeight - $('#main').offset().top) {
					$('#main').height(function(index, height) {
						return window.innerHeight - $(this).offset().top;
					});
				}
				
				// Read privileges and set specific actions/elements
				if (ROLE == 'admin' || ROLE == 'editor') {
					// Adding actions
					$('#actions-menu').empty();
					$('#actions-menu').append('<li><a class="action-folderadd" href="#"><i class="glyphicon glyphicon-folder-close"></i> ' + MESSAGES[4] + '</a></li>');
					$('#actions-menu').append('<li><a class="action-labadd" href="#"><i class="glyphicon glyphicon-file"></i> ' + MESSAGES[5] + '</a></li>');
					$('#actions-menu').append('<li><a class="action-selectedclone" href="#"><i class="glyphicon glyphicon-copy"></i> ' + MESSAGES[6] + '</a></li>');
					$('#actions-menu').append('<li><a class="action-selecteddelete" href="#"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[7] + '</a></li>');
					$('#actions-menu').append('<li><a class="action-selectedexport" href="#"><i class="glyphicon glyphicon-export"></i> ' + MESSAGES[8] + '</a></li>');
					$('#actions-menu').append('<li><a class="action-import" href="#"><i class="glyphicon glyphicon-import"></i> ' + MESSAGES[9] + '</a></li>');
					$('#actions-menu').append('<li><a class="action-folderrename" href="#"><i class="glyphicon glyphicon-pencil"></i> ' + MESSAGES[10] + '</a></li>');
					
					// Make labs draggable (to move inside folders)
					$('.lab').draggable({
						appendTo: '#body',
						helper: 'clone',
						revert: 'invalid',
						scroll: false,
						snap: '.folder',
						stack: '.folder'
					});
					
					// Make folders draggable (to move inside folders)
					$('.folder').draggable({
						appendTo: '#body',
						helper: 'clone',
						revert: 'invalid',
						scroll: false,
						snap: '.folder',
						stack: '.folder'
					});
					
					// Make folders draggable (to receive labs and folders)
					$('.folder').droppable({
						drop: function(e, o) {
							var object = o['draggable'].attr('data-path');
							var path = $(this).attr('data-path');
							logger(1, 'DEBUG: moving "' + object + '" to "' + path + '".');
							if (o['draggable'].hasClass('lab')) {
								$.when(moveLab(object, path)).done(function(data) {
									logger(1, 'DEBUG: "' + object + '" moved to "' + path + '".');
									o['draggable'].fadeOut(300, function() { o['draggable'].remove(); })
								}).fail(function(data) {
									logger(1, 'DEBUG: failed to move "' + object + '" into "' + path + '".');
									addModal('ERROR', '<p>' + data + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
								});
							} else if (o['draggable'].hasClass('folder')) {
								$.when(moveFolder(object, path)).done(function(data) {
									logger(1, 'DEBUG: "' + object + '" moved to "' + path + '".');
									o['draggable'].fadeOut(300, function() { o['draggable'].remove(); })
								}).fail(function(data) {
									logger(1, 'DEBUG: failed to move "' + object + '" into "' + path + '".');
									addModal('ERROR', '<p>' + data + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
								});
							} else {
								// Should not be here
								logger(1, 'DEBUG: cannot move unknown object.');
							}

						}
					});
				} else {
					$('#actions-menu').empty();
					$('#actions-menu').append('<li><a href="#">&lt;' + MESSAGES[3] + '&gt;</a></li>');
				}
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				addModal('ERROR', '<p>' + data['message'] + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			addModal('ERROR', '<p>' + message + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
		}
	});
}

// Print lab open page
function printPageLabOpen(lab) {
	var html = '';
	
	// Navbar: main
	html += '<nav id="navbar-lab" class="navbar navbar-static-top"><div class="container col-md-12 col-lg-12"><div class="navbar-collapse collapse"><ul class="col-md-9 col-lg-9 nav navbar-nav"><li class="item dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Actions <span class="caret"></span></a><ul id="actions-menu" class="dropdown-menu"><li><a href="#">&lt;' + MESSAGES[3] + '&gt;</a></li></ul></li><li class="item"><a class="action-logout item" href="#"><i class="glyphicon glyphicon-log-out"></i> ' + MESSAGES[14] + '</a></li></ul></div></div></nav>';
	
	// Main
	html += '<div id="lab-sidebar"><ul></ul></div>';
	html += '<div id="lab-viewport" data-path="' + lab + '"></div>';
	
	$('#body').html(html);
	
	// Print topology
	printLabTopology();
	
	// Clearing actions (navbar)
	$('#actions-menu').empty();
	
	// Clearing actions (sidebar)
	$('#lab-sidebar ul').empty();
	
	// Read privileges and set specific actions/elements
	if (ROLE == 'admin' || ROLE == 'editor') {
		$('#lab-sidebar ul').append('<li><a class="action-labobjectadd" href="#" title="' + MESSAGES[56] + '"><i class="glyphicon glyphicon-plus"></i></a></li>');
		$('#lab-sidebar ul').append('<li><a class="action-nodelink" href="#" title="' + MESSAGES[115] + '"><i class="glyphicon glyphicon-link"></i></a></li>');
	}
	
	$('#lab-sidebar ul').append('<li><a class="action-labbodyget" href="#" title="' + MESSAGES[64] + '"><i class="glyphicon glyphicon-list-alt"></i></a></li>');
	$('#lab-sidebar ul').append('<li><a class="action-nodesget" href="#" title="' + MESSAGES[62] + '"><i class="glyphicon glyphicon-hdd"></i></a></li>');
	$('#lab-sidebar ul').append('<li><a class="action-networksget" href="#" title="' + MESSAGES[61] + '"><i class="glyphicon glyphicon-transfer"></i></a></li>');
	$('#lab-sidebar ul').append('<li><a class="action-configsget" href="#" title="' + MESSAGES[58] + '"><i class="glyphicon glyphicon-align-left"></i></a></li>');
	$('#lab-sidebar ul').append('<li><a class="action-picturesget" href="#" title="' + MESSAGES[59] + '"><i class="glyphicon glyphicon-picture"></i></a></li>');
	$('#lab-sidebar ul').append('<li><a class="action-labtopologyrefresh" href="#" title="' + MESSAGES[57] + '"><i class="glyphicon glyphicon-refresh"></i></a></li>');
	$('#lab-sidebar ul').append('<li><a class="action-labclose" href="#" title="' + MESSAGES[60] + '"><i class="glyphicon glyphicon-off"></i></a></li>');
	
	// Read privileges and set specific actions/elements
	if (ROLE == 'admin' || ROLE == 'editor') {
		// Adding actions (navbar)
		$('#actions-menu').append('<li><a class="action-labedit" href="#" title="' + MESSAGES[87] + '"><i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[87] + '</a></li>');
	}
}

// Print user management section
function printUserManagement() {
	$.when(getUsers(null)).done(function(data) {
		var html = '<div class="row"><div id="users" class="col-md-12 col-lg-12"><div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[44] + '</th><th>' + MESSAGES[19] + '</th><th>' + MESSAGES[28] + '</th><th>' + MESSAGES[29] + '</th><th>' + MESSAGES[30] + '</th><th>' + MESSAGES[31] + '</th><th>' + MESSAGES[32] + '</th></tr></thead><tbody></tbody></table></div></div></div>';
		html += '<div class="row"><div id="pods" class="col-md-12 col-lg-12"><div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[44] + '</th><th>' + MESSAGES[32] + '</th><th>' + MESSAGES[33] + '</th><th>' + MESSAGES[63] + '</th></tr></thead><tbody></tbody></table></div></div></div>';
		$('#main-title').hide();
		$('#main').html(html);
	
		// Read privileges and set specific actions/elements
		if (ROLE == 'admin') {
			// Adding actions
			$('#actions-menu').empty();
			$('#actions-menu').append('<li><a class="action-useradd" href="#"><i class="glyphicon glyphicon-plus"></i> ' + MESSAGES[34] + '</a></li>');
			$('#actions-menu').append('<li><a class="action-selecteddelete" href="#"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[35] + '</a></li>');
		} else {
			$('#actions-menu').empty();
			$('#actions-menu').append('<li><a href="#">&lt;' + MESSAGES[3] + '&gt;</a></li>');
		}
	
		// Adding all users
		$.each(data, function(id, object) {
			var username = object['username'];
			var name = object['name'];
			var email = object['email'];
			var role = object['role'];
			if (object['lab'] == null) {
				var lab = 'none';
			} else {
				var lab = object['lab'];
			}
			if (object['pod'] == -1) {
				var pod = 'none';
			} else {
				var pod = object['pod'];
			}
			if (object['expiration'] <= 0) {
				var expiration = MESSAGES[54];
			} else {
				var d = new Date(object['expiration'] * 1000);
				expiration = d.toLocaleDateString(); 
			}
			if (object['session'] <= 0) {
				var session = MESSAGES[53];
			} else {
				var d = new Date(object['session'] * 1000);
				session = d.toLocaleDateString() + ' ' + d.toLocaleTimeString() + ' from ' + object['ip']; 
			}
			if (object['pexpiration'] <= 0) {
				var pexpiration = MESSAGES[54];
			} else {
				var d = new Date(object['pexpiration'] * 1000);
				pexpiration = d.toLocaleDateString(); 
			}
			$('#users tbody').append('<tr class="action-useredit user" data-path="' + username + '"><td class="username">' + username + '</td><td class="class="name">' + name + '</td><td class="email">' + email + '</td><td class="role">' + role + '</td><td class="expiration">' + expiration + '</td><td class="session">' + session + '</td><td class="pod">' + pod + '</td></tr>');
			if (object['pod'] >= 0) {
				$('#pods tbody').append('<tr class="action-useredit user" data-path="' + username + '"><td class="username">' + username + '</td><td class="pod">' + pod + '</td><td class="pexpiration">' + pexpiration + '</td><td class="lab">' + lab + '</td></tr>');
			}
		});
	}).fail(function(message) {
		addModalError(message);
	});
}

// Print system stats
function printSystemStats() {
	$.when(getSystemStats()).done(function(data) {
		// Main: title
		var html_title = '<div class="row row-eq-height"><div id="list-title-folders" class="col-md-3 col-lg-3"><span title="' + MESSAGES[13] + '">' + MESSAGES[13] + '</span></div><div id="list-title-labs" class="col-md-3 col-lg-3"><span></span></div><div id="list-title-info" class="col-md-6 col-lg-6"><span></span></div></div>';
		
		// Main
		var html = '<div id="main" class="container col-md-12 col-lg-12"><div class="fill-height row row-eq-height"><div id="stats-text" class="col-md-3 col-lg-3"><ul></ul></div><div id="stats-graph" class="col-md-9 col-lg-9"><ul></ul></div></div></div>';
		
		// Footer
		html += '</div>';
		
		$('#main-title').html(html_title);
		$('#main-title').show();
		$('#main').html(html);
		
		// Read privileges and set specific actions/elements
		$('#actions-menu').empty();
		$('#actions-menu').append('<li><a class="action-sysstatus" href="#"><i class="glyphicon glyphicon-refresh"></i> ' + MESSAGES[40] + '</a></li>');
		$('#actions-menu').append('<li><a class="action-stopall" href="#"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[50] + '</a></li>');
		
		// Adding all stats
		
		// Text
		$('#stats-text ul').append('<li>' + MESSAGES[39] + ': <code>' + data['version'] + '</code></li>');
		$('#stats-text ul').append('<li>' + MESSAGES[49] + ': <code>' + data['qemu_version'] + '</code></li>');
		$('#stats-text ul').append('<li>' + MESSAGES[29] + ': <code>' + ROLE + '</code></li>');
		$('#stats-text ul').append('<li>' + MESSAGES[32] + ': <code>' + ((TENANT == -1) ? 'none' : TENANT) + '</code></li>');
		
		// CPU usage
		$('#stats-graph ul').append('<li><div class="circle circle-cpu col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[36] + '</span></div></li>');
		$('.circle-cpu').circleProgress({
			arcCoef: 0.7,
			value: data['cpu'],
			thickness: 10,
			startAngle: -Math.PI / 2,
			fill: {	gradient: ['#46a6b6'] }
		}).on('circle-animation-progress', function(event, progress) {
			if (progress > data['cpu']) {
				$(this).find('strong').html(parseInt(100 * data['cpu']) + '%');
			} else {
				$(this).find('strong').html(parseInt(100 * progress) + '%');
			}
		});
		
		// Memory usage
		$('#stats-graph ul').append('<li><div class="circle circle-memory col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[37] + '</span></div></li>');
		$('.circle-memory').circleProgress({
			arcCoef: 0.7,
			value: data['mem'],
			thickness: 10,
			startAngle: -Math.PI / 2,
			fill: {	gradient: ['#46a6b6'] }
		}).on('circle-animation-progress', function(event, progress) {
			if (progress > data['mem']) {
				$(this).find('strong').html(parseInt(100 * data['mem']) + '%');
			} else {
				$(this).find('strong').html(parseInt(100 * progress) + '%');
			}
		});
		
		// Swap usage
		$('#stats-graph ul').append('<li><div class="circle circle-swap col-md-3 col-lg-3"><strong></strong><br/><span>Swap usage</span></div></li>');
		$('.circle-swap').circleProgress({
			arcCoef: 0.7,
			value: data['swap'],
			thickness: 10,
			startAngle: -Math.PI / 2,
			fill: {	gradient: ['#46a6b6'] }
		}).on('circle-animation-progress', function(event, progress) {
			if (progress > data['swap']) {
				$(this).find('strong').html(parseInt(100 * data['swap']) + '%');
			} else {
				$(this).find('strong').html(parseInt(100 * progress) + '%');
			}
		});

		// Disk usage
		$('#stats-graph ul').append('<li><div class="circle circle-disk col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[38]+ '</span></div></li>');		
		$('.circle-disk').circleProgress({
			arcCoef: 0.7,
			value: data['disk'],
			thickness: 10,
			startAngle: -Math.PI / 2,
			fill: {	gradient: ['#46a6b6'] }
		}).on('circle-animation-progress', function(event, progress) {
			if (progress > data['disk']) {
				$(this).find('strong').html(parseInt(100 * data['disk']) + '%');
			} else {
				$(this).find('strong').html(parseInt(100 * progress) + '%');
			}
		});
		
		// IOL running nodes
		$('#stats-graph ul').append('<li><div class="count count-iol col-md-4 col-lg-4"></div>');
		$('.count-iol').html('<strong>' + data['iol'] + '</strong><br/><span>' + MESSAGES[41] + '</span></li>');
		
		// Dynamips running nodes
		$('#stats-graph ul').append('<li><div class="count count-dynamips col-md-4 col-lg-4"></div></li>');	
		$('.count-dynamips').html('<strong>' + data['dynamips'] + '</strong><br/><span>' + MESSAGES[42] + '</span>');
		
		// QEMU running nodes
		$('#stats-graph ul').append('<li><div class="count count-qemu col-md-4 col-lg-4"></div></li>');	
		$('.count-qemu').html('<strong>' + data['qemu'] + '</strong><br/><span>' + MESSAGES[43] + '</span>');
	}).fail(function(message) {
		addModalError(message);
	});
}
