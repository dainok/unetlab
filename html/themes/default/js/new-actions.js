// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/new-actions.js
 *
 * Actions for HTML elements
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

// Logout button
$(document).on('click', '.button-logout', function(e) {
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
				printPageAuthentication();
			} else {
				// Authentication error
				logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				addModal('ERROR', '<p>' + data['message'] + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
			}
		},
		error: function(data) {
			// Authentication error
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			addModal('ERROR', '<p>' + message + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
		}
	});
});

// Accept privacy
$(document).on('click', '#privacy', function () {
	$.cookie('privacy', 'true', {
		expires: 90,
		path: '/'
	});
	if ($.cookie('privacy') == 'true') {
		window.location.reload();
	}
});

// Select user, folder or lab
$(document).on('click', 'a.folder, a.lab, tr.user', function(e) {
	logger(1, 'DEBUG: selected "' + $(this).attr('data-path') + '".');
	if ($(this).hasClass('selected')) {
		// Already selected -> unselect it
		$(this).removeClass('selected');
	} else {
		// Selected it
		$(this).addClass('selected');
	}
});

// Display folder-add form
$(document).on('click', 'a.folder-add', function(e) {
	var html = '<form id="form-folder-add" class="form-horizontal form-folder-add"><div class="form-group"><label class="col-md-3 control-label">Path</label><div class="col-md-5"><input class="form-control" name="folder[path]" value="' + $('#list-folders').attr('data-path') + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input class="form-control autofocus" name="folder[name]" value="" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">Add</button> <button type="button" class="btn btn-grey" data-dismiss="modal">Cancel</button></div></div></form>';
	logger(1, 'DEBUG: popping up the folder-add form.');
	addModal('Add a new folder', html, '');
	validateFolder();
});

// Display folder-rename form
$(document).on('click', 'a.folder-rename', function(e) {
	var html = '<form id="form-folder-rename" class="form-horizontal form-folder-rename"><div class="form-group"><label class="col-md-3 control-label">Path</label><div class="col-md-5"><input class="form-control" name="folder[path]" value="' + $('#list-folders').attr('data-path') + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input class="form-control autofocus" name="folder[name]" value="" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">Rename</button> <button type="button" class="btn btn-grey" data-dismiss="modal">Cancel</button></div></div></form>';
	logger(1, 'DEBUG: popping up the folder-rename form.');
	addModal('Rename current folder', html, '');
	validateFolder();
});

// Display import form
$(document).on('click', 'a.import', function(e) {
	var html = '<form id="form-import" class="form-horizontal form-import"><div class="form-group"><label class="col-md-3 control-label">Path</label><div class="col-md-7"><input class="form-control" name="import[path]" value="' + $('#list-folders').attr('data-path') + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">File</label><div class="col-md-7"><span class="btn btn-default btn-file btn-aqua">Browse <input class="form-control" name="import[file]" value="" type="file"></span></div></div><div class="form-group"><div class="col-md-7 col-md-offset-3"><button type="submit" class="btn btn-aqua">Import</button> <button type="button" class="btn btn-grey" data-dismiss="modal">Cancel</button></div></div></form>';
	logger(1, 'DEBUG: popping up the import form.');
	addModal('Import labs', html, '');
	validateImport();
});

// Display lab-add form
$(document).on('click', 'a.lab-add', function(e) {
	var html = '<form id="form-lab-add" class="form-horizontal form-lab-add"><div class="form-group"><label class="col-md-3 control-label">Path</label><div class="col-md-5"><input class="form-control" name="lab[path]" value="' + $('#list-folders').attr('data-path') + '" disabled="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input class="form-control autofocus" name="lab[name]" value="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Version</label><div class="col-md-5"><input class="form-control" name="lab[version]" value="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Author</label><div class="col-md-5"><input class="form-control" name="lab[author]" value="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Description</label><div class="col-md-5"><textarea class="form-control" name="lab[description]"></textarea></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">Add</button> <button type="button" class="btn btn-grey" data-dismiss="modal">Cancel</button></div></div></form>';
	logger(1, 'DEBUG: popping up the lab-add form.');
	addModal('Add a new lab', html, '');
	validateLabInfo();
});

// Clone selected labs
$(document).on('click', '.selected-clone', function(e) {
	var type = 'POST'
	var url = '/api/labs';
	var path = {};
	$('.selected').each(function(id, object) {
		form_data = {};
		form_data['name'] = 'Copy of ' + $(this).text().slice(0, -4);
		form_data['source'] = $(this).attr('data-path');
		$.ajax({
			timeout: TIMEOUT,
			type: type,
			url: encodeURI(url),
			dataType: 'json',
			data: JSON.stringify(form_data),
			success: function(data) {
				if (data['status'] == 'success') {
					logger(1, 'DEBUG: created lab "' + form_data['name'] + '" from "' + form_data['source'] + '".');
				} else {
					// Application error
					logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				}
			},
			error: function(data) {
				// Server error
				var message = getJsonMessage(data['responseText']);
				logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
				logger(1, 'DEBUG: ' + message);
			}
		});
	});
	if ($('.selected').size() > 0) {
		printPageLabList($('#list-folders').attr('data-path'));
	}
});

// Delete selected objects
$(document).on('click', '.selected-delete', function(e) {
	var type = 'DELETE'
	$('.selected').each(function(id, object) {
		var name = $(this).attr('data-path');
		if ($(this).hasClass('folder')) {
			var object = 'folder';
			var path = 'folders/' + $(this).attr('data-path');
		} else if ($(this).hasClass('lab')) {
			var object = 'lab';
			var path = 'labs/' + $(this).attr('data-path');
		} else if ($(this).hasClass('user')) {
			var object = 'user';
			var path = 'users/' + $(this).attr('data-path');
		} else {
			logger(1, 'DEBUG: cannot delete, invalid object.');
			return;
		}
		var url = '/api/' + path;
		console.log(url);

		$.ajax({
			timeout: TIMEOUT,
			type: type,
			url: encodeURI(url),
			dataType: 'json',
			success: function(data) {
				if (data['status'] == 'success') {
					logger(1, 'DEBUG: ' + object + ' "' + name + '" deleted.');
					// Remove object
					$('.' + object + '[data-path="' + name + '"]').fadeOut(300, function() { $(this).remove(); })
				} else {
					// Application error
					logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				}
			},
			error: function(data) {
				// Server error
				var message = getJsonMessage(data['responseText']);
				logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
				logger(1, 'DEBUG: ' + message);
			}
		});
	});
});

// Clone selected labs
$(document).on('click', '.selected-export', function(e) {
	var type = 'POST'
	var url = '/api/export';
	var form_data = {};
	var i = 0;
	form_data['path'] = $('#list-folders').attr('data-path')
	$('.selected').each(function(id, object) {
		form_data[i] = $(this).attr('data-path');
		i++;
	});
	
	if ($('.selected').size() > 0) {
		$.ajax({
			timeout: TIMEOUT,
			type: type,
			url: encodeURI(url),
			dataType: 'json',
			data: JSON.stringify(form_data),
			success: function(data) {
				if (data['status'] == 'success') {
					logger(1, 'DEBUG: objects exported into "' + data['data'] + '".');
					window.location = data['data'];
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
});

// Open lab-list page
$(document).on('click', '.lab-list', function(e) {
	printPageLabList('/');
});

// Open system status page
$(document).on('click', '.sysstatus', function(e) {
	var html = '<div class="row"><div class="version col-md-12 col-lg-12"></div></div><div class="row"><div class="circle circle-cpu col-md-3 col-lg-3"><strong></strong><br/><span>CPU usage</span></div><div class="circle circle-memory col-md-3 col-lg-3"><strong></strong><br/><span>Memory usage</span></div><div class="circle circle-swap col-md-3 col-lg-3"><strong></strong><br/><span>Swap usage</span></div><div class="circle circle-disk col-md-3 col-lg-3"><strong></strong><br/><span>Disk usage on /</span></div></div><div class="row"><div class="count count-iol col-md-4 col-lg-4"></div><div class="count count-dynamips col-md-4 col-lg-4"></div><div class="count count-qemu col-md-4 col-lg-4"></div>';
	var url = '/api/status';
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got system status data.');
                version = data['data']['version'];
                cpu_percent = data['data']['cpu'] / 100;
                disk_percent = data['data']['disk'] / 100;
                mem_percent = data['data']['mem'] / 100;
                cached_percent = data['data']['cached'] / 100;
                swap_percent = data['data']['swap'] / 100;
                qemu_count = data['data']['qemu'];
                dynamips_count = data['data']['dynamips'];
                iol_count = data['data']['iol'];

				$('#main-body').html(html);
				$('.version').html('Unified Networking Lab version is: <code>' + version + '</code>');
				$('.circle-cpu').circleProgress({
					arcCoef: 0.7,
					value: cpu_percent,
					thickness: 10,
					startAngle: -Math.PI / 2,
					fill: {	gradient: ['#46a6b6'] }
				}).on('circle-animation-progress', function(event, progress) {
					if (progress > cpu_percent) {
						$(this).find('strong').html(parseInt(100 * cpu_percent) + '%');
					} else {
						$(this).find('strong').html(parseInt(100 * progress) + '%');
					}
				});
				
				$('.circle-memory').circleProgress({
					arcCoef: 0.7,
					value: mem_percent,
					thickness: 10,
					startAngle: -Math.PI / 2,
					fill: {	gradient: ['#46a6b6'] }
				}).on('circle-animation-progress', function(event, progress) {
					if (progress > mem_percent) {
						$(this).find('strong').html(parseInt(100 * mem_percent) + '%');
					} else {
						$(this).find('strong').html(parseInt(100 * progress) + '%');
					}
				});
				
				$('.circle-swap').circleProgress({
					arcCoef: 0.7,
					value: swap_percent,
					thickness: 10,
					startAngle: -Math.PI / 2,
					fill: {	gradient: ['#46a6b6'] }
				}).on('circle-animation-progress', function(event, progress) {
					if (progress > swap_percent) {
						$(this).find('strong').html(parseInt(100 * swap_percent) + '%');
					} else {
						$(this).find('strong').html(parseInt(100 * progress) + '%');
					}
				});
				
				$('.circle-disk').circleProgress({
					arcCoef: 0.7,
					value: disk_percent,
					thickness: 10,
					startAngle: -Math.PI / 2,
					fill: {	gradient: ['#46a6b6'] }
				}).on('circle-animation-progress', function(event, progress) {
					if (progress > disk_percent) {
						$(this).find('strong').html(parseInt(100 * disk_percent) + '%');
					} else {
						$(this).find('strong').html(parseInt(100 * progress) + '%');
					}
				});
				
				$('.count-iol').html('<strong>' + iol_count + '</strong><br/><span>running IOL nodes</span>');
				$('.count-dynamips').html('<strong>' + dynamips_count + '</strong><br/><span>running Dynamips nodes</span>');
				$('.count-qemu').html('<strong>' + qemu_count + '</strong><br/><span>running QEMU nodes</span>');
				$('#actions-menu').html('<li><a class="sysstatus" href="#"><i class="glyphicon glyphicon-refresh"></i> Refresh</a></li>');

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
});

// Open user management page
$(document).on('click', '.usermgmt', function(e) {
	printPageUserManagement();
});

// Add a user
$(document).on('click', 'a.user-add', function(e) {
	$.when(getRoles()).done(function(roles) {
		// Got data
		var html = '<form id="form-user-add" class="form-horizontal form-user-edit"><div class="form-group"><label class="col-md-3 control-label">Username</label><div class="col-md-5"><input class="form-control autofocus" name="user[username]" value="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input class="form-control" name="user[name]" value="" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Email</label><div class="col-md-5"><input class="form-control" name="user[email]" value="" type="text"/></div></div>';
		html += '<div class="form-group"><label class="col-md-3 control-label">Password</label><div class="col-md-5"><input class="form-control" name="user[password]" value="" type="password"/></div></div>';
		html += '<div class="form-group"><label class="col-md-3 control-label">Role</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="user[role]" data-live-search="true">';
		$.each(roles, function(r, d) {
			html += '<option value="' + r + '">' + d + '</option>';
		});
		html += '</select></div></div>';
		html += '<div class="form-group"><label class="col-md-3 control-label">Expiration</label><div class="col-md-5"><input class="form-control" name="user[expiration]" value="" type="text"/></div></div>';
		html += '<h4>Assigned POD</h4>';
		html += '<div class="form-group"><label class="col-md-3 control-label">POD</label><div class="col-md-5"><input class="form-control" name="user[pod]" value="" type="text"/></div></div>';
		html += '<div class="form-group"><label class="col-md-3 control-label">Expiration</label><div class="col-md-5"><input class="form-control" name="user[pexpiration]" value="" type="text"/></div></div>';




		html += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">Save</button> <button type="button" class="btn btn-grey" data-dismiss="modal">Cancel</button></div></div></form>';
		addModal('Add a new user', html, '');
		validateUser()
	});
});	


// Open folder
$(document).on('dblclick', 'a.folder', function(e) {
	logger(1, 'DEBUG: opening folder "' + $(this).attr('data-path') + '".');
	printPageLabList($(this).attr('data-path'));
});

// Preview lab
$(document).on('dblclick', 'a.lab', function(e) {
	logger(1, 'DEBUG: opening a preview of lab "' + $(this).attr('data-path') + '".');
	$('.lab-opened').each(function() {
		// Remove all previous selected lab
		$(this).removeClass('lab-opened');
	});
	$(this).addClass('lab-opened');
	printPageLabPreview($(this).attr('data-path'));
});

// Edit a user
$(document).on('dblclick', 'tr.user', function(e) {
	var username = $(this).attr('data-path');
	var url = '/api/users/' + $(this).attr('data-path');
	var type = 'GET'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: got UNetLab user.');
				if (data['data']['expiration'] == -1) {
					var expiration = '';
				} else {
					var expiration = $.datepicker.formatDate('yy-mm-dd', new Date(data['data']['expiration'] * 1000));
				}
				if (data['data']['pod'] == -1) {
					var pod = '';
				} else {
					var pod = data['data']['pod'];
				}
				if (data['data']['pexpiration'] == -1) {
					var pexpiration = '';
				} else {
					var pexpiration = $.datepicker.formatDate('yy-mm-dd', new Date(data['data']['pexpiration'] * 1000));
				}
				$.when(getRoles()).done(function(roles) {
					// Got data
					var html = '<form data-path="' + username + '" id="form-user-edit" class="form-horizontal form-user-edit"><div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input class="form-control autofocus" name="user[name]" value="' + data['data']['name'] + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">Email</label><div class="col-md-5"><input class="form-control" name="user[email]" value="' + data['data']['email'] + '" type="text"/></div></div>';
					html += '<div class="form-group"><label class="col-md-3 control-label">Password</label><div class="col-md-5"><input class="form-control" name="user[password]" value="" type="password"/></div></div>';
					html += '<div class="form-group"><label class="col-md-3 control-label">Role</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="user[role]" data-live-search="true">';
					$.each(roles, function(r, d) {
						var role_selected = '';
						if (data['data']['role'] == r) {
							role_selected = ' selected';
						}
						html += '<option' + role_selected + ' value="' + r + '">' + d + '</option>';
					});
					html += '</select></div></div>';
					html += '<div class="form-group"><label class="col-md-3 control-label">Expiration</label><div class="col-md-5"><input class="form-control" name="user[expiration]" value="' + expiration + '" type="text"/></div></div>';
					html += '<h4>Assigned POD</h4>';
					html += '<div class="form-group"><label class="col-md-3 control-label">POD</label><div class="col-md-5"><input class="form-control" name="user[pod]" value="' + pod + '" type="text"/></div></div>';
					html += '<div class="form-group"><label class="col-md-3 control-label">Expiration</label><div class="col-md-5"><input class="form-control" name="user[pexpiration]" value="' + pexpiration + '" type="text"/></div></div>';



				
					html += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">Save</button> <button type="button" class="btn btn-grey" data-dismiss="modal">Cancel</button></div></div></form>';
					addModal('Edit user "' + data['data']['username'] + '"', html, '');
					validateUser()
				}).fail(function(error) {
					// Failed to get data
					addModal('ERROR', '<p>' + error + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
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
});	
	
// Remove modal on close
$(document).on('hide.bs.modal', '.modal', function () {
    $(this).remove();
});

// Set autofocus on show modal
$(document).on('shown.bs.modal', '.modal', function () {
    $('.autofocus').focus();
});

// Submit login form
$(document).on('submit', '#form-login', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('login');
	var url = '/api/auth/login';
	var type = 'POST';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user is authenticated.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				$.when(getUserInfo()).done(function() {
					// User is authenticated
					logger(1, 'DEBUG: loading home page.');
					printPageLabList('/');
				}).fail(function() {
					// User is not authenticated, or error on API
					logger(1, 'DEBUG: loading authentication page.');
					printPageAuthentication();
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
	return false;  // Stop to avoid POST
});

// Submit folder-add form
$(document).on('submit', '#form-folder-add', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('folder');
	var url = '/api/folders';
	var type = 'POST';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: folder "' + form_data['name'] + '" added.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				// Reload the folder list
				printPageLabList(form_data['path']);
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
	return false;  // Stop to avoid POST
});

// Submit import form
$(document).on('submit', '#form-import', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = new FormData();
	var form_name = 'import';
	var url = '/api/import';
	var type = 'POST';
	// Setting options: cannot use form2Array() because not using JSON to send data
	$('form :input[name^="' + form_name + '["]').each(function(id, object) {
		// INPUT name is in the form of "form_name[value]", get value only
		form_data.append($(this).attr('name').substr(form_name.length + 1, $(this).attr('name').length - form_name.length - 2), $(this).val());
	});
	// Add attachments
    $.each(ATTACHMENTS, function(key, value) {
        form_data.append(key, value);
    });
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
        contentType: false, // Set content type to false as jQuery will tell the server its a query string request
        processData: false, // Don't process the files
		dataType: 'json',
		data: form_data,
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: labs imported.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				// Reload the folder list
				printPageLabList($('#list-folders').attr('data-path'));
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
	return false;  // Stop to avoid POST
});

// Submit lab-add form
$(document).on('submit', '#form-lab-add', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('lab');
	var url = '/api/labs';
	var type = 'POST';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab "' + form_data['name'] + '" added.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				// Reload the lab list
				printPageLabList(form_data['path']);
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
	return false;  // Stop to avoid POST
});

// Submit user-edit form
$(document).on('submit', '#form-user-edit', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('user');
	// Converting data
	if (form_data['expiration'] == '') {
		form_data['expiration'] = -1;
	} else {
		form_data['expiration'] = Math.floor($.datepicker.formatDate('@', new Date(form_data['expiration'])) / 1000);
	}
	if (form_data['pexpiration'] == '') {
		form_data['pexpiration'] = -1;
	} else {
		form_data['pexpiration'] = Math.floor($.datepicker.formatDate('@', new Date(form_data['pexpiration'])) / 1000);
	}
	if (form_data['pod'] == '') {
		form_data['pod'] = -1;
	}
	var edit_username = $(this).attr('data-path')
	var url = '/api/users/' + edit_username;
	var type = 'PUT';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user "' + edit_username + '" saved.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				if (edit_username == USERNAME) {
					// Editing self
					// TODO -> should logout and login
				}
				// Reload the user list
				printPageUserManagement();
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
	return false;  // Stop to avoid POST
});

// Submit user-add form
$(document).on('submit', '#form-user-add', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('user');
	// Converting data
	if (form_data['expiration'] == '') {
		form_data['expiration'] = -1;
	} else {
		form_data['expiration'] = Math.floor($.datepicker.formatDate('@', new Date(form_data['expiration'])) / 1000);
	}
	if (form_data['pexpiration'] == '') {
		form_data['pexpiration'] = -1;
	} else {
		form_data['pexpiration'] = Math.floor($.datepicker.formatDate('@', new Date(form_data['pexpiration'])) / 1000);
	}
	if (form_data['pod'] == '') {
		form_data['pod'] = -1;
	}
	var url = '/api/users';
	var type = 'POST';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user "' + form_data['username'] + '" added.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				// Reload the user list
				printPageUserManagement();
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
	return false;  // Stop to avoid POST
});
