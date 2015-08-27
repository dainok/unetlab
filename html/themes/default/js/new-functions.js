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
 * @version 20150820
 */

// Add Modal
function addModal(title, body, footer) {
	var html = '<div aria-hidden="false" style="display: block;" class="modal fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">' + body + '</div><div class="modal-footer">' + footer + '</div></div></div></div>';
	$('body').append(html);
	$('body > .modal').modal('show');
	setAutofocus();
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
	} catch(e) {
		if (response != '') {
			message = response;
		} else {
			message = 'Undefined message, check if the UNetLab VM is powered on. If it is, see <a href="/Logs" target="_blank">logs</a>.';
		}
	}
	return message;
}

// Return Authentication Page
function printPageAuthentication() {
	var html = '<div class="row full-height"><div class="col-md-5 col-lg-5 full-height" id="auth-left"><div class="middle"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img alt="Logo RR" src="/themes/default/images/logo-rr.png" /></div></div><!-- <div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img alt="Signup Icon" src="/themes/default/images/button-signup.png"></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">to access more features</div></div> --><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">Existing user...</div></div><form id="form-login"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[username]" placeholder="USERNAME" type="text" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[password]" placeholder="PASSWORD" type="password" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input alt="Login Icon" src="/themes/default/images/button-login.png" type="image" /></div></div></form></div></div><div class="col-md-7 col-lg-7" id="auth-right"><div id="logo-angular"><img alt="Logo Angular" src="/themes/default/images/logo-angular.png" /></div><div id="logo-ad"><img alt="Logo AD" src="/themes/default/images/logo-ad.png" /></div><div id="logo-text"><h1>Unified Networking Lab</h1><p>UNetLab can be considered the next major version of<br>iou-web, but the software has been rewritten from<br>scratch. The major advantage over GNS3 and<br>iou-web itself is about multi-hypervisor<br>support within a single entity. UNetLab<br>allows to design labs using IOU, Dy-<br>namips and QEMU nodes without<br>dealing with multi virtual ma-<br>chines: everything run in-<br>side a UNetLab host,<br>and a lab is a single<br>file including all<br>information<br>needed.</p></div></div></div>'
	$('#body').html(html);
}

// Return Lab List page
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
				html += '<div id="main-navbar" class="navbar" role="navigation"><div class="container-fluid"><div class="col-md-3 col-lg-3 navbar-header"><img height=100" src="/themes/default/images/logo-rr.png"/></div><div class="collapse navbar-collapse navbar-menubuilder"><ul class="nav navbar-nav navbar-right"><li class="navbar-item"><a class="item lab-list" href="#">Home</a></li><li><img src="/themes/default/images/vertical_dots.gif"></li><li class="dropdown navbar-item"><a class="dropdown-toggle item" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Actions <span class="caret"></span></a><ul id="actions-menu" class="dropdown-menu"><li><a class="folder-add" href="#"><i class="glyphicon glyphicon-folder-close"></i> Add a new folder</a></li><li><a class="lab-add" href="#"><i class="glyphicon glyphicon-file"></i> Add a new lab</a></li><li><a class="selected-clone" href="#"><i class="glyphicon glyphicon-copy"></i> Clone selected labs</a></li><li><a class="selected-delete" href="#"><i class="glyphicon glyphicon-trash"></i> Delete selected objects</a></li><li><a class="selected-export" href="#"><i class="glyphicon glyphicon-export"></i> Export selected objects</a></li><li><a class="import" href="#"><i class="glyphicon glyphicon-import"></i> Import external objects</a></li><!--<li><a class="folder-rename" href="#"><i class="glyphicon glyphicon-pencil"></i> Rename current folder</a></li>--></ul></li><li><img src="/themes/default/images/vertical_dots.gif"></li><li class="navbar-item"><a class="sysstatus item" href="#">System&nbsp;Status</a></li><li><img src="/themes/default/images/vertical_dots.gif"></li><li class="navbar-item"><a class="usermgmt item" href="#">Users</a></li><li><img src="/themes/default/images/vertical_dots.gif"></li><li class="navbar-item"><a class="item" href="http://www.unetlab.com/" target="_blank">Help</a></li><li><img src="/themes/default/images/vertical_dots.gif"></li><li class="navbar-item"><a class="button-logout item" href="#">Logout</a></li></ul></div></div></div><div id="main-body" class="full-height"><div id="list-title"><div id="list-title-folders" class="col-md-3 col-lg-3">Folders in <span>' + folder + '</span></div><div id="list-title-labs" class="col-md-3 col-lg-3" style="margin-left: 10px; margin-right: 10px;">Labs</div><div id="list-title-info" class="col-md-6 col-lg-6" style="margin-right: -20px; padding-right: 20px;"></div></div><div id="list-body" class="full-height"><div class="col-md-3 col-lg-3 full-height" id="list-folders" data-path="' + folder + '"><ul>';

				$.each(data['data']['folders'], function(id, object) {
					// Adding all folders
					html += '<li><a class="folder" data-path="' + object['path'] + '" href="#" title="Double click to open, single click to select.">' + object['name'] + '</a></li>';
				});

				html += '</ul></div><div class="col-md-3 col-lg-3 full-height" id="list-labs"><ul>';
			
				$.each(data['data']['labs'], function(id, object) {
					// Adding all labs
					html += '<li><a class="lab" data-path="' + object['path'] + '" href="#" title="Double click to open, single click to select.">' + object['file'] + '</a></li>';
				});

				html += '</ul></div><div class="col-md-6 col-lg-6 full-height" id="list-info"></div></div></div>';
				$('#body').html(html);
				$('.lab').draggable({
					appendTo: '#body',
					helper: 'clone',
					revert: 'invalid',
					scroll: false,
					snap: '.folder',
					stack: '.folder'
				});
				$('.folder').droppable({
					drop: function(e, o) {
						var lab = o['draggable'].attr('data-path');
						var path = $(this).attr('data-path');
						logger(1, 'DEBUG: moving "' + lab + '" to "' + path + '".');
						$.when(moveLab(lab, path)).done(function(data) {
							logger(1, 'DEBUG: "' + lab + '" moved to "' + path + '".');
							o['draggable'].fadeOut(300, function() { o['draggable'].remove(); })
						}).fail(function(data) {
							logger(1, 'DEBUG: failed to move "' + lab + '" into "' + path + '".');
							addModal('ERROR', '<p>' + data + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
						});
					}
				});
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

// Return Lab preview section
function printPageLabPreview(lab) {
	var html = '';
	var url = '/api/labs' + lab;
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab "' + lab + '" found.');
// TODO
html += '<ul>';
html += '<li>Name: ' + data['data']['name'] + '</li>';
html += '<li>ID: <code>' + data['data']['id'] + '</code></li>';
html += '<li>Version: <code>' + data['data']['version'] + '</code></li>';
html += '<li>Author: ' + data['data']['author'] + '</li>';
html += '<li>Description:<br/>' + data['data']['description'] + '</li>';
html += '<li><a href="/lab_open.php?filename=' + lab + '&tenant=' + TENANT + '">Load this lab</a></li>';
html += '</ul>';
	$('#list-title-info').html('FILE: ' + lab.replace(/\\/g,'/').replace(/.*\//, ''));
	$('#list-info').html(html);
	
				
				
				
				
				
				
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
				USERNAME = data['data']['username'];
				EMAIL = data['data']['email'];
				TENANT = data['data']['tenant'];
				NAME = data['data']['name'];
				deferred.resolve();
			} else {
				// Application error
				logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject();
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			deferred.reject();
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

// Move lab inside a folder
function moveLab(lab, path) {
	var deferred = $.Deferred();
	var form_data = {};
	form_data['path'] = path;
	var url = '/api/labs' + lab + '/move';
	var type = 'PUT';
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

// Set focus on right input element
function setAutofocus() {
	$('.autofocus').each(function(id, object) {
		$(this).focus();
	});
	//$(this).find('.autofocus').focus();
}