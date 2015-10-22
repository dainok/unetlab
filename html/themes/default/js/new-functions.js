// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/new-functions.js
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
				FOLDER = data['data']['folder'];
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

/***************************************************************************
 * Print forms and pages
 **************************************************************************/
// Folder add form
function printFormFolderAdd(path) {
	var html = '<form id="form-folder-add" class="form-horizontal form-folder-add"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="folder[path]" value="' + path + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control autofocus" name="folder[name]" value="" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[17] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
	logger(1, 'DEBUG: popping up the folder-add form.');
	addModal(MESSAGES[4], html, '');
}

// Folder rename folder
function printFormFolderRename(folder) {
	var html = '<form id="form-folder-rename" class="form-horizontal form-folder-rename"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="folder[path]" value="' + folder + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control autofocus" name="folder[name]" value="" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[21] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
	logger(1, 'DEBUG: popping up the folder-rename form.');
	addModal(MESSAGES[10], html, '');
	validateFolder();
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
		$('#list-title-info span').html(lab['filename'].replace(/\\/g,'/').replace(/.*\//, ''));
		$('#list-info').html(html);
	}).fail(function(message) {
		addModalError(message);
	});
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
				html += '<div id="body"><nav id="navbar-top" class="hidden-xs hidden-sm navbar navbar-static-top"><div class="container col-md-12 col-lg-12"><div id="logo-main" class="col-md-3 col-lg-3"><img alt="Logo" class="img-responsive" src="/themes/default/images/logo_rr.png"/></div><div class="navbar-collapse collapse"><ul class="nav navbar-nav navbar-right"><li class="navbar-item-aqua"><a href="https://unetlab.freshdesk.com/support/tickets/new" target="_blank"">Help</a></li><li class="navbar-item-grey"><a href="http://www.unetlab.com/" target="_blank">About</a></li><li class="navbar-item-grey"><a href="http://forum.802101.com/forum39.html" target="_blank">Forum</a></li></ul></div></div></nav>';

				// Navbar: main
				html += '<nav id="navbar-main" class="navbar navbar-static-top"><div class="container col-md-12 col-lg-12"><div id="navbar-main-text" class="hidden-xs hidden-sm col-md-3 col-lg-3">by Andrea Dainese</div><div id="navbar-main-spacer" class="hidden-xs hidden-sm"></div><div class="navbar-collapse collapse"><ul class="col-md-9 col-lg-9 nav navbar-nav"><li class="item-first lab-list"><a class="action-lablist" href="#">' + MESSAGES[11] + '</a></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Actions <span class="caret"></span></a><ul id="actions-menu" class="dropdown-menu"><li><a href="#">&lt;' + MESSAGES[3] + '&gt;</a></li></ul></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item usermgmt"><a class="action-usermgmt" href="#">' + MESSAGES[12] + '</a></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item sysstatus"><a class="action-sysstatus" href="#">' + MESSAGES[13] + '</a></li><li class="separator hidden-xs hidden-sm"><img alt="Spacer" src="/themes/default/images/vertical_dots.gif"/></li><li class="item"><a class="action-logout item" href="#">' + MESSAGES[14] + '</a></li></ul></div></div></nav>';

				// Main: title
				html += '<div id="main-title" class="container col-md-12 col-lg-12"><div class="row row-eq-height"><div id="list-title-folders" class="col-md-3 col-lg-3"><span title="' + folder + '">' + MESSAGES[0] + '</span></div><div id="list-title-labs" class="col-md-3 col-lg-3"><span>' + MESSAGES[1] + '</span></div><div id="list-title-info" class="col-md-6 col-lg-6"><span></span></div></div></div>';
				
				// Main
				html += '<div id="main" class="container col-md-12 col-lg-12"><div class="fill-height row row-eq-height"><div id="list-folders" class="col-md-3 col-lg-3" data-path="' + folder + '"><ul></ul></div><div id="list-labs" class="col-md-3 col-lg-3"><ul></ul></div><div id="list-info" class="col-md-6 col-lg-6"></div></div></div>';
				
				// Footer
				html += '</div>';
				
				// Adding to the page
				$('#body').html(html);
				
				// Adding all folders
				$.each(data['data']['folders'], function(id, object) {
					$('#list-folders > ul').append('<li><a class="folder" data-path="' + object['path'] + '" href="#" title="Double click to open, single click to select.">' + object['name'] + '</a></li>');
				});

				// Adding all labs
				$.each(data['data']['labs'], function(id, object) {
					$('#list-labs > ul').append('<li><a class="lab" data-path="' + object['path'] + '" href="#" title="Double click to open, single click to select.">' + object['file'] + '</a></li>');
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
					
					// Make folders draggable (to receive labs)
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
	console.log(response);
	var message = '';
	try {
		message = JSON.parse(response)['message'];
		code = JSON.parse(response)['code'];
		if (code == 401) {
			// User is no more authenticated
			//location.reload();
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

// Print Authentication Page
function printPageAuthentication() {
	var html = '<div class="row full-height"><div class="col-md-5 col-lg-5 full-height" id="auth-left"><div class="middle"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img alt="Logo RR" src="/themes/default/images/logo-rr.png" /></div></div><!-- <div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img alt="Signup Icon" src="/themes/default/images/button-signup.png"></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">to access more features</div></div> --><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">Existing user...</div></div><form id="form-login"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[username]" placeholder="USERNAME" type="text" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[password]" placeholder="PASSWORD" type="password" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input alt="Login Icon" src="/themes/default/images/button-login.png" type="image" /></div></div></form></div></div><div class="col-md-7 col-lg-7" id="auth-right"><div id="logo-angular"><img alt="Logo Angular" src="/themes/default/images/logo-angular.png" /></div><div id="logo-ad"><img alt="Logo AD" src="/themes/default/images/logo-ad.png" /></div><div id="logo-text"><h1>Unified Networking Lab</h1><p>UNetLab can be considered the next major version of<br>iou-web, but the software has been rewritten from<br>scratch. The major advantage over GNS3 and<br>iou-web itself is about multi-hypervisor<br>support within a single entity. UNetLab<br>allows to design labs using IOU, Dy-<br>namips and QEMU nodes without<br>dealing with multi virtual ma-<br>chines: everything run in-<br>side a UNetLab host,<br>and a lab is a single<br>file including all<br>information<br>needed.</p></div></div></div>'
	$('#body').html(html);
}





// Print user management section
function printPageUserManagement() {
	var html = '<div id="users" class="col-md-12 col-lg-12"><div class="table-responsive"><table class="table"><thead><tr><th>Username</th><th>Name</th><th>Email</th><th>Role</th><th>Expiration</th><th>Last seen</th><th>POD</th><th>POD Expiration</th></tr></thead><tbody></tbody></table></div></div>';
	var url = '/api/users/';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got UNetLab users.');
				$('#main-body').html(html);

				// Adding all data rows
				$.each(data['data'], function(id, object) {
					var username = object['username'];
					var name = object['name'];
					var email = object['email'];
					var role = object['role'];
					if (object['pod'] == -1) {
						var pod = 'none';
					} else {
						var pod = object['pod'];
					}
					if (object['expiration'] <= 0) {
						var expiration = 'never';
					} else {
						var d = new Date(object['expiration'] * 1000);
						expiration = d.toLocaleDateString(); 
					}
					if (object['session'] <= 0) {
						var session = 'never';
					} else {
						var d = new Date(object['session'] * 1000);
						session = d.toLocaleDateString() + ' ' + d.toLocaleTimeString() + ' from ' + object['ip']; 
					}
					if (object['pexpiration'] <= 0) {
						var pexpiration = 'never';
					} else {
						var d = new Date(object['pexpiration'] * 1000);
						pexpiration = d.toLocaleDateString(); 
					}
					$('#main-body .table tbody').append('<tr class="user" data-path="' + username + '"><td>' + username + '</td><td>' + name + '</td><td>' + email + '</td><td>' + role + '</td><td>' + expiration + '</td><td>' + session + '</td><td>' + pod + '</td><td>' + pexpiration + '</td></tr>');
					$('#actions-menu').html('<li><a class="user-add" href="#"><i class="glyphicon glyphicon-plus"></i> Add a new user</a></li><li><a class="selected-delete" href="#"><i class="glyphicon glyphicon-trash"></i> Delete selected users</a></li>');
				});
			} else {
				// Application error
				logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				addModal('ERROR', '<p>' + data['message'] + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
			}
		},
		error: function(data) {
			// Server error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			addModal('ERROR', '<p>' + message + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
		}
	});
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
