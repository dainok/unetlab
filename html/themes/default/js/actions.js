// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/actions.js
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

// Add the selected filename to the proper input box
$('body').on('change', 'input[name="import[file]"]', function(e) {
	$('input[name="import[local]"]').val($(this).val());
});

// Select node template
$('body').on('change', '#form-node-add, #form-node-edit', function(e) {
	var node_template = $(this).find('option:selected').val();
	
	printFormNodeData(node_template);
    var deferred = $.Deferred();
    var node_template = $(this).find("option:selected").val();

    if (node_template != '') {
        // Getting template only if a valid option is selected (to avoid requests during typewriting)
        $.when(displayNodeFormFromTemplate(node_template, false)).done(function(form_template) {
            // Add the form to the HTML page
            $('#form-node_add').html(form_template);

            // Validate values and set autofocus
            $('.selectpicker').selectpicker();
            validateLabNode();

            deferred.resolve();
        }).fail(function() {
            deferred.reject();
        });
    }
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

// Remove modal on close
$(document).on('hide.bs.modal', '.modal', function () {
    $(this).remove();
});

// Set autofocus on show modal
$(document).on('shown.bs.modal', '.modal', function () {
    $('.autofocus').focus();
});

// After node/network move
$(document).on('dragstop', '.node_frame, .network_frame', function(e) {
	var lab_filename = $('#lab-viewport').attr('data-path');
	var offset = $(this).offset();
	var left = Math.round(offset.left - 30 + $('#lab-viewport').scrollLeft());	// 30 is the sidebar
	var top = Math.round(offset.top - 30 + $('#lab-viewport').scrollTop());		// 30 is the topbar
	var id = $(this).attr('data-path');

	if ($(this).hasClass('node_frame')) {
		logger(1, 'DEBUG: setting node' + id + ' position.');
		$.when(setNodePosition(lab_filename, id, left, top)).done(function() {
			// Position saved -> redraw topology
			jsPlumb.repaintEverything();
		}).fail(function(message) {
			// Error on save
			addModalError(message);
		});
	} else if ($(this).hasClass('network_frame')) {
		logger(1, 'DEBUG: setting network' + id + ' position.');
		$.when(setNetworkPosition(lab_filename, id, left, top)).done(function() {
			// Position saved -> redraw topology
			jsPlumb.repaintEverything();
		}).fail(function(message) {
			// Error on save
			addModalError(message);
		});
	} else {
		logger(1, 'DEBUG: unknown object.');
	}
});

// Close all context menu
$(document).on('mousedown', '*', function(e) {
	if (!$(e.target).is('#context-menu, #context-menu *')) {
		// If click outside context menu, remove the menu
		e.stopPropagation();
		$('#context-menu').remove();
	}
});

// Prevent default context menu on viewport
$(document).on('contextmenu', '*', function(e) {
	e.preventDefault();  // Prevent default behaviour
});

// Open context menu block
$(document).on('click', '.menu-collapse, .menu-collapse i', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var item_class = $(this).attr('data-path');
	$('.' + item_class).slideToggle('slow');
});

// Manage context menu
$(document).on('contextmenu', '.context-menu', function(e) {
	e.preventDefault();  // Prevent default behaviour
	
	if ($(this).hasClass('node_frame')) {
		logger(1, 'DEBUG: opening node context menu');
		var node_id = $(this).attr('data-path');
		var title = $(this).attr('data-name');
		var body = '<li><a class="menu-collapse" data-path="menu-manage" href="#"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[75] + '</a></li><li><a class="action-nodestart menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-play"></i> ' + MESSAGES[66] + '</a></li><li><a class="action-nodestop menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[67] + '</a></li><li><a class="action-nodewipe menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[68] + '</a></li><li><a class="action-nodeexport menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-save"></i> ' + MESSAGES[69] + '</a></li><li role="separator" class="divider"></li><li><a class="menu-collapse" data-path="menu-interface" href="#"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[70] + '</a></li><li><a class="action-nodecapture menu-interface" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-search"></i> TEST</a></li><li role="separator" class="divider"></li>';

		// Read privileges and set specific actions/elements
		if (ROLE == 'admin' || ROLE == 'editor') {
			body += '<li><a class="menu-collapse" data-path="menu-edit" href="#"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[73] + '</a></li><li><a class="action-nodeinterfaces menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[72] + '</a></li><li><a class="action-nodeedit menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[71] + '</a></li><li><a class="action-nodedelete menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[65] + '</a></li>'
		};
	} else {
		// Context menu not defined for this object
		return false;
	}
	
	printContextMenu(title, body, e.pageX, e.pageY);
});

// Window resize
$(window).resize(function(){
	if ($('#lab-viewport').length ) {
        // Update topology on window resize
        jsPlumb.repaintEverything();
    }
});

/***************************************************************************
 * Actions links
 **************************************************************************/
// Add a new folder
$(document).on('click', '.action-folderadd', function(e) {
	logger(1, 'DEBUG: action = folderadd');
	var data = {};
	data['path'] = $('#list-folders').attr('data-path');
	printFormFolder('add', data);
});

// Open an existent folder
$(document).on('dblclick', '.action-folderopen', function(e) {
	logger(1, 'DEBUG: opening folder "' + $(this).attr('data-path') + '".');
	printPageLabList($(this).attr('data-path'));
});

// Rename an existent folder
$(document).on('click', '.action-folderrename', function(e) {
	logger(1, 'DEBUG: action = folderrename');
	var data = {};
	data['path'] = dirname($('#list-folders').attr('data-path'));
	data['name'] = basename($('#list-folders').attr('data-path'));
	printFormFolder('rename', data);
});

// Import labs
$(document).on('click', '.action-import', function(e) {
	logger(1, 'DEBUG: action = import');
	printFormImport($('#list-folders').attr('data-path'));
});

// Add a new lab
$(document).on('click', '.action-labadd', function(e) {
	logger(1, 'DEBUG: action = labadd');
	var values = {};
	values['path'] = $('#list-folders').attr('data-path');
	printFormLab('add', values);
});

// Print lab body
$(document).on('click', '.action-labbodyget', function(e) {
	logger(1, 'DEBUG: action = labbodyget');
	$.when(getLabInfo($('#lab-viewport').attr('data-path')), getLabBody($('#lab-viewport').attr('data-path'))).done(function(info, body) {
		addModalWide(MESSAGES[64], '<h1>' + info['name'] + '</h1>' + '<p>' + info['description'] + '</p>' + body, '')
	}).fail(function(message1, message2) {
		if (message1 != null) {
			addModalError(message1);
		} else {
			addModalError(message2)
		};
	});
});

// Print lab network
$(document).on('click', '.action-labnetworkget', function(e) {
	logger(1, 'DEBUG: action = labnetworkget');
	var id = $(this).attr('data-path');
	var lab_filename = $('#lab-viewport').attr('data-path');
	$.when(getNetworks(lab_filename, id)).done(function(values) {
		values['id'] = id;
		printFormNetwork('edit', values)
	}).fail(function(message) {
		addModalError(message);
	});
	$('#context-menu').remove();
});

// Print lab networks
$(document).on('click', '.action-labnetworksget', function(e) {
	logger(1, 'DEBUG: action = labnetworksget');
	$.when(getNetworks($('#lab-viewport').attr('data-path'), null)).done(function(networks) {
		var body = '';
		$.each(networks, function(key, value) {
			body += '<li><a class="action-labnetworkget" data-path="' + value['id'] + '" href="#" title="network' + value['id'] + '"><i class="glyphicon glyphicon-transfer"></i> ' + value['name'] + ' <code>[ID:' + value['id'] + ']</code></a></li>';
		});
		printContextMenu(MESSAGES[62], body, e.pageX, e.pageY);
	}).fail(function(message) {
		addModalError(message);
	});
});

// Print lab nodes
$(document).on('click', '.action-labnodesget', function(e) {
	logger(1, 'DEBUG: action = labnodesget');
	$.when(getNodes($('#lab-viewport').attr('data-path'), null)).done(function(nodes) {
		var body = '';
		$.each(nodes, function(key, value) {
			body += '<li><a class="action-labnodeget" data-path="' + value['id'] + '" href="#" title="node' + value['id'] + '"><i class="glyphicon glyphicon-hdd"></i> ' + value['name'] + ' <code>[ID:' + value['id'] + ']</code></a></li>';
		});
		printContextMenu(MESSAGES[62], body, e.pageX, e.pageY);
	}).fail(function(message) {
		addModalError(message);
	});
});

// Lab close
$(document).on('click', '.action-labclose', function(e) {
	logger(1, 'DEBUG: action = labclose');
	$.when(closeLab()).done(function() {
		postLogin();
	}).fail(function(message) {
		addModalError(message);
	});
});

// Edit a lab
$(document).on('click', '.action-labedit', function(e) {
	logger(1, 'DEBUG: action = labedit');
	$.when(getLabInfo($('#lab-viewport').attr('data-path'))).done(function(values) {
		values['path'] = $('#lab-viewport').attr('data-path');
		printFormLab('edit', values);
	}).fail(function(message) {
		addModalError(message);
	});
});

// List all labs
$(document).on('click', '.action-lablist', function(e) {
	logger(1, 'DEBUG: action = lablist');
	printPageLabList(FOLDER);
});

// Open a lab
$(document).on('click', '.action-labopen', function(e) {
	logger(1, 'DEBUG: action = labopen');
	printPageLabOpen($(this).attr('data-path'));
	
});

// Preview a lab
$(document).on('dblclick', '.action-labpreview', function(e) {
	logger(1, 'DEBUG: opening a preview of lab "' + $(this).attr('data-path') + '".');
	$('.lab-opened').each(function() {
		// Remove all previous selected lab
		$(this).removeClass('lab-opened');
	});
	$(this).addClass('lab-opened');
	printLabPreview($(this).attr('data-path'));
});

// Redraw topology
$(document).on('click', '.action-labtopologyrefresh', function(e) {
	logger(1, 'DEBUG: action = labtopologyrefresh');
	printLabTopology($('#lab-viewport').attr('data-path'))
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

// Add object in lab_view
$(document).on('click', '.action-labobjectadd', function(e) {
	logger(1, 'DEBUG: action = labobjectadd');
	var body = '';
	body += '<li><a class="action-nodeadd" data-path="' + $('#lab-viewport').attr('data-path')+ '" href="#"><i class="glyphicon glyphicon-hdd"></i> ' + MESSAGES[81] + '</a></li>';
	body += '<li><a class="action-networkadd" data-path="' + $('#lab-viewport').attr('data-path')+ '" href="#"><i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[82] + '</a></li>';
	body += '<li><a class="action-pictureadd" data-path="' + $('#lab-viewport').attr('data-path') + '" href="#"><i class="glyphicon glyphicon-picture"></i> ' + MESSAGES[83] + '</a></li>';
	printContextMenu(MESSAGES[80], body, e.pageX, e.pageY);
});

// Add node
$(document).on('click', '.action-nodeadd', function(e) {
	logger(1, 'DEBUG: action = nodeadd');
	printFormNode($(this).attr('data-path'), 'add', null);
	$('#context-menu').remove();
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

// Export a config
$(document).on('click', '.action-nodeexport', function(e) {
	logger(1, 'DEBUG: action = nodeexport');
	var lab_filename = $('#lab-viewport').attr('data-path');
	var node_id = $(this).attr('data-path');
	var node_name = $(this).attr('data-name');
	$.when(cfg_export(lab_filename, node_id)).done(function() {
		// Config exported -> print a small green message
		addMessage('success', node_name + ': ' + MESSAGES[79])
	}).fail(function(message) {
		// Cannot export
		addMessage('danger', node_name + ': ' + message);
	});
	$('#context-menu').remove();
});
 
// Start a node
$(document).on('click', '.action-nodestart', function(e) {
	logger(1, 'DEBUG: action = nodestart');
	var lab_filename = $('#lab-viewport').attr('data-path');
	var node_id = $(this).attr('data-path');
	var node_name = $(this).attr('data-name');
	$.when(start(lab_filename, node_id)).done(function() {
		// Node started -> print a small green message
		addMessage('success', node_name + ': ' + MESSAGES[76])
	}).fail(function(message) {
		// Cannot start
		addMessage('danger', node_name + ': ' + message);
	});
	$('#context-menu').remove();
});

// Stop a node
$(document).on('click', '.action-nodestop', function(e) {
	logger(1, 'DEBUG: action = nodestop');
	var lab_filename = $('#lab-viewport').attr('data-path');
	var node_id = $(this).attr('data-path');
	var node_name = $(this).attr('data-name');
	$.when(stop(lab_filename, node_id)).done(function() {
		// Node stopped -> print a small green message
		addMessage('success', node_name + ': ' + MESSAGES[77])
	}).fail(function(message) {
		// Cannot stop
		addMessage('danger', node_name + ': ' + message);
	});
	$('#context-menu').remove();
});

// Wipe a node
$(document).on('click', '.action-nodewipe', function(e) {
	logger(1, 'DEBUG: action = nodewipe');
	var lab_filename = $('#lab-viewport').attr('data-path');
	var node_id = $(this).attr('data-path');
	var node_name = $(this).attr('data-name');
	$.when(wipe(lab_filename, node_id)).done(function() {
		// Node wiped -> print a small green message
		addMessage('success', node_name + ': ' + MESSAGES[78])
	}).fail(function(message) {
		// Cannot wipe
		addMessage('danger', node_name + ': ' + message);
	});
	$('#context-menu').remove();
});
 
// Stop all nodes
$(document).on('click', '.action-stopall', function(e) {
	logger(1, 'DEBUG: action = stopall');
	$.when(stopAll()).done(function() {
		// Stopped all nodes -> reload status page
		printSystemStats();
	}).fail(function(message) {
		// Cannot stop all nodes
		addModalError(message);
	});
});

// Load system status page
$(document).on('click', '.action-sysstatus', function(e) {
	logger(1, 'DEBUG: action = sysstatus');
	printSystemStats();
});
 
// Add a user
$(document).on('click', '.action-useradd', function(e) {
	logger(1, 'DEBUG: action = useradd');
	printFormUser('add', {});
});

// Edit a user
$(document).on('dblclick', '.action-useredit', function(e) {
	logger(1, 'DEBUG: action = useredit');
	$.when(getUsers($(this).attr('data-path'))).done(function(user) {
		// Got user
		printFormUser('edit', user);
	}).fail(function(message) {
		// Cannot get user
		addModalError(message);
	});
});

// Load user management page
$(document).on('click', '.action-usermgmt', function(e) {
	logger(1, 'DEBUG: action = usermgmt');
	printUserManagement();
}); 

/***************************************************************************
 * Submit
 **************************************************************************/

// Submit folder form
$(document).on('submit', '#form-folder-add, #form-folder-rename', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('folder');
	if ($(this).attr('id') == 'form-folder-add') {
		logger(1, 'DEBUG: posting form-folder-add form.');
		var url = '/api/folders';
		var type = 'POST';
	} else {
		logger(1, 'DEBUG: posting form-folder-rename form.');
		form_data['path'] = (form_data['path'] == '/') ? '/' + form_data['name'] : form_data['path'] + '/' + form_data['name'];
		var url = '/api/folders' + form_data['original'];
		var type = 'PUT';
	}
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
		
// Submit lab form
$(document).on('submit', '#form-lab-add, #form-lab-edit', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('lab');
	if ($(this).attr('id') == 'form-lab-add') {
		logger(1, 'DEBUG: posting form-lab-add form.');
		var url = '/api/labs';
		var type = 'POST';
	} else {
		logger(1, 'DEBUG: posting form-lab-edit form.');
		var url = '/api/labs' + form_data['path'];
		var type = 'PUT';
	}
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: lab "' + form_data['name'] + '" saved.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				if ($(this).attr('id') == 'form-lab-add') {
					// Reload the lab list
					printPageLabList(form_data['path']);
				} else if (basename($('#lab-viewport').attr('data-path')) != form_data['name'] + '.unl') {
					// Lab has been renamed, need to close it.
					logger(1, 'DEBUG: lab "' + form_data['name'] + '" renamed.');
					$.when(closeLab()).done(function() {
						postLogin();
					}).fail(function(message) {
						addModalError(message);
					});
				} else {
					addMessage(data['status'], data['message']);
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
	return false;  // Stop to avoid POST
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
					logger(1, 'DEBUG: user authenticated.');
					postLogin();
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

// Submit user form
 $(document).on('submit', '#form-user-add, #form-user-edit', function(e) {
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
	
	var username = form_data['username'];
	if ($(this).attr('id') == 'form-user-add') {
		logger(1, 'DEBUG: posting form-user-add form.');
		var url = '/api/users';
		var type = 'POST';
	} else {
		logger(1, 'DEBUG: posting form-user-edit form.');
		var url = '/api/users/' + username;
		var type = 'PUT';
	}
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: user "' + username + '" saved.');
				// Close the modal
				$(e.target).parents('.modal').modal('hide');
				// Reload the user list
				printUserManagement();
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
