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

// Attach files
$('body').on('change', 'input[type=file]', function(e) {
    ATTACHMENTS = e.target.files;
});

// Add the selectef filename to the proper input box
$('body').on('change', 'input[name="import[file]"]', function(e) {
	$('input[name="import[local]"]').val($(this).val());
	console.log($(this).val())
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

// Select folders, labs or users
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
	printLabPreview($(this).attr('data-path'));
});

// Remove modal on close
$(document).on('hide.bs.modal', '.modal', function () {
    $(this).remove();
});

// Set autofocus on show modal
$(document).on('shown.bs.modal', '.modal', function () {
    $('.autofocus').focus();
});

/***************************************************************************
 * Actions links
 **************************************************************************/
// Add a new folder
$(document).on('click', '.action-folderadd', function(e) {
	logger(1, 'DEBUG: action = folderadd');
	printFormFolderAdd($('#list-folders').attr('data-path'));
});

// Rename an existent folder
$(document).on('click', '.action-folderrename', function(e) {
	logger(1, 'DEBUG: action = folderrename');
	printFormFolderRename($('#list-folders').attr('data-path'));
});

// Import labs
$(document).on('click', '.action-import', function(e) {
	logger(1, 'DEBUG: action = import');
	printFormImport($('#list-folders').attr('data-path'));
});

// Add a new lab
$(document).on('click', '.action-labadd', function(e) {
	logger(1, 'DEBUG: action = labadd');
	printFormLabAdd($('#list-folders').attr('data-path'));
});

// List all labs
$(document).on('click', '.action-lablist', function(e) {
	logger(1, 'DEBUG: action = lablist');
	printPageLabList(FOLDER);
});

// Open a lab
$(document).on('click', '.action-labopen', function(e) {
	logger(1, 'DEBUG: action = labopen');
});

// Logout
$(document).on('click', '.action-logout', function(e) {
	logger(1, 'DEBUG: action = logout');
	$.when(logoutUser()).done(function() {
		printPageAuthentication();
	}).fail(function(message) {
		addModalError(message);
	});
});

// Clone selected labs
$(document).on('click', '.action-selectedclone', function(e) {
	if ($('.selected').size() > 0) {
		logger(1, 'DEBUG: action = selectedclone');
		$('.selected').each(function(id, object) {
			form_data = {};
			form_data['name'] = 'Copy of ' + $(this).text().slice(0, -4);
			form_data['source'] = $(this).attr('data-path');
			$.when(cloneLab(form_data)).done(function() {
				// Lab cloned -> reload the folder
				printPageLabList($('#list-folders').attr('data-path'));
			}).fail(function(message) {
				// Error on clone
				addModalError(message);
			});
		});
	}
}); 
 
// Delete selected folders and labs
$(document).on('click', '.action-selecteddelete', function(e) {
	if ($('.selected').size() > 0) {
		logger(1, 'DEBUG: action = selecteddelete');
		$('.selected').each(function(id, object) {
			var path = $(this).attr('data-path');
			if ($(this).hasClass('folder')) {
				$.when(deleteFolder(path)).done(function() {
					// Folder deleted
					$('.folder[data-path="' + path + '"]').fadeOut(300, function() {
						$(this).remove();
					});
				}).fail(function(message) {
					// Cannot delete folder
					addModalError(message);
				});
			} else if ($(this).hasClass('lab')) {
				$.when(deleteLab(path)).done(function() {
					// Lab deleted
					$('.lab[data-path="' + path + '"]').fadeOut(300, function() {
						$(this).remove();
					});
				}).fail(function(message) {
					// Cannot delete lab
					addModalError(message);
				});
			} else if ($(this).hasClass('user')) {
				$.when(deleteUser(path)).done(function() {
					// User deleted
					$('.user[data-path="' + path + '"]').fadeOut(300, function() {
						$(this).remove();
					});
				}).fail(function(message) {
					// Cannot delete user
					addModalError(message);
				});
			} else {
				// Invalid object
				logger(1, 'DEBUG: cannot delete, invalid object.');
				return;
			}
		});
	}
});

// Export selected folders and labs
$(document).on('click', '.action-selectedexport', function(e) {
	if ($('.selected').size() > 0) {
		logger(1, 'DEBUG: action = selectedexport');
		var form_data = {};
		var i = 0;
		form_data['path'] = $('#list-folders').attr('data-path')
		$('.selected').each(function(id, object) {
			form_data[i] = $(this).attr('data-path');
			i++;
		});
		$.when(exportObjects(form_data)).done(function(url) {
			// Export done
			window.location = url;
		}).fail(function(message) {
			// Cannot export objects
			addModalError(message);
		});
	}
 });

// Load user management page
$(document).on('click', '.action-usermgmt', function(e) {
	logger(1, 'DEBUG: action = usermgmt');
	printUserManagement();
}); 

// Load system status page
$(document).on('click', '.action-sysstatus', function(e) {
	printSystemStats();
});

/***************************************************************************
 * Submit
 **************************************************************************/







 
 
 
 
 
 

 
 
 
 

 
 
 


	

	
	
	
	
	
	


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
					printPageLabList(FOLDER);
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
