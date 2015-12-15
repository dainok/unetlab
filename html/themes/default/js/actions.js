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

// On escape remove mouse_frame
$(document).on('keydown', 'body', function(e){
	if('27' == e.which){
		$('#mouse_frame').remove();
		$('#lab-viewport').removeClass('lab-viewport-click-catcher');
	};
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
$(document).on('hide.bs.modal', '.modal', function (e) {
	$(this).remove();
	if(!$(this).attr('skipRedraw')){
		printLabTopology();
	}
	$(this).attr('skipRedraw', false);
});

// Set autofocus on show modal
$(document).on('shown.bs.modal', '.modal', function () {
	$('.autofocus').focus();
});

// After node/network move
$(document).on('dragstop', '.node_frame, .network_frame', function(e) {
	var that = this,
		offset = $(this).offset(),
		left = Math.round(offset.left - 30 + $('#lab-viewport').scrollLeft()),	// 30 is the sidebar
		top = Math.round(offset.top + $('#lab-viewport').scrollTop()),
		id = $(this).attr('data-path');
	if (left >= 0 && top >= 0) {
		if ($(this).hasClass('node_frame')) {
			logger(1, 'DEBUG: setting node' + id + ' position.');
			$.when(setNodePosition(id, left, top)).done(function() {
				// Position saved -> redraw topology
				jsPlumb.repaint(that);
			}).fail(function(message) {
				// Error on save
				addModalError(message);
			});
		} else if ($(this).hasClass('network_frame')) {
			logger(1, 'DEBUG: setting network' + id + ' position.');
			$.when(setNetworkPosition(id, left, top)).done(function() {
				// Position saved -> redraw topology
				jsPlumb.repaint(that);
			}).fail(function(message) {
				// Error on save
				addModalError(message);
			});
		} else {
			logger(1, 'DEBUG: unknown object.');
		}
	} else {
		addMessage('warning', MESSAGES[124]);
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
	$('.context-collapsible').slideUp('slow');
	$('.' + item_class).slideToggle('slow');
});

// Manage context menu
$(document).on('contextmenu', '.context-menu', function(e) {
	e.preventDefault();  // Prevent default behaviour

	if ($(this).hasClass('node_frame')) {
		logger(1, 'DEBUG: opening node context menu');
		var node_id = $(this).attr('data-path');
		var title = $(this).attr('data-name');
		var body = '<li><a class="menu-collapse" data-path="menu-manage" href="#"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[75] + '</a></li><li><a class="action-nodestart context-collapsible menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-play"></i> ' + MESSAGES[66] + '</a></li><li><a class="action-nodestop context-collapsible menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[67] + '</a></li><li><a class="action-nodewipe context-collapsible menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-erase"></i> ' + MESSAGES[68] + '</a></li><li role="separator" class="divider"></li><li><a class="menu-collapse" data-path="menu-interface" href="#"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[70] + '</a></li><li><a class="action-nodecapture context-collapsible menu-interface" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-search"></i> TEST</a></li>';

		// Read privileges and set specific actions/elements
		if (ROLE == 'admin' || ROLE == 'editor') {
			body += '<li role="separator" class="divider"></li><li><a class="menu-collapse" data-path="menu-edit" href="#"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[73] + '</a></li><li><a class="action-nodeexport context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-save"></i> ' + MESSAGES[69] + '</a></li><li><a class="action-nodeinterfaces context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[72] + '</a></li><li><a class="action-nodeedit context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[71] + '</a></li><li><a class="action-nodedelete context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[65] + '</a></li>'
		};
	} else if ($(this).hasClass('network_frame')) {
		if (ROLE == 'admin' || ROLE == 'editor') {
			logger(1, 'DEBUG: opening network context menu');
			var network_id = $(this).attr('data-path');
			var title = $(this).attr('data-name');
			var body = '<li><a class="context-collapsible  action-networkedit" data-path="' + network_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[71] + '</a></li><li><a class="context-collapsible  action-networkdelete" data-path="' + network_id + '" data-name="' + title + '" href="#"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[65] + '</a></li>';
		}
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
		// Update picture map on window resize
		$('map').imageMapResize();
	}
});

/***************************************************************************
 * Actions links
 **************************************************************************/

// startup-config menu
$(document).on('click', '.action-configsget', function(e) {
	logger(1, 'DEBUG: action = configsget');
	$.when(getNodeConfigs(null)).done(function(configs) {
		var body = '<div class="row"><div class="config-list col-md-2 col-lg-2"><ul>';
		$.each(configs, function(key, config) {
			var title = (config['config'] == 0)? MESSAGES[122] : MESSAGES[121];
			body += '<li><a class="action-configget" data-path="' + key + '" href="#" title="' + title + '">' + config['name'];
			if (config['config'] == 1) {
				body += ' <i class="glyphicon glyphicon-pushpin"></i>';
			}
			body += '</a></li>';
		});
		body += '</ul></div><div id="config-data" class="col-md-10 col-lg-10"></div></div>';
		addModalWide(MESSAGES[120], body, '');
	}).fail(function(message) {
		addModalError(message);
	});
});

// Get startup-config
$(document).on('click', '.action-configget', function(e) {
	logger(1, 'DEBUG: action = configget');
	var id = $(this).attr('data-path');
	$.when(getNodeConfigs(id)).done(function(config) {
		printFormNodeConfigs(config);
	}).fail(function(message) {
		addModalError(message);
	});
	$('#context-menu').remove();
});

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
	$.when(getLabInfo($('#lab-viewport').attr('data-path')), getLabBody()).done(function(info, body) {
		addModalWide(MESSAGES[64], '<h1>' + info['name'] + '</h1><p>' + info['description'] + '</p><p><code>ID: ' + info['id'] + '</code></p>' + body, '')
	}).fail(function(message1, message2) {
		if (message1 != null) {
			addModalError(message1);
		} else {
			addModalError(message2)
		};
	});
});

// Edit/print lab network
$(document).on('click', '.action-networkedit', function(e) {
	logger(1, 'DEBUG: action = action-networkedit');
	var id = $(this).attr('data-path');
	$.when(getNetworks(id)).done(function(values) {
		values['id'] = id;
		printFormNetwork('edit', values)
	}).fail(function(message) {
		addModalError(message);
	});
});

// Print lab networks
$(document).on('click', '.action-networksget', function(e) {
	logger(1, 'DEBUG: action = networksget');
	$.when(getNetworks(null)).done(function(networks) {
		printListNetworks(networks);
	}).fail(function(message) {
		addModalError(message);
	});
});

// Delete lab network
$(document).on('click', '.action-networkdelete', function(e) {
	logger(1, 'DEBUG: action = action-networkdelete');
	var id = $(this).attr('data-path');
	$.when(deleteNetwork(id)).done(function(values) {
		$('.network' + id).remove();
	}).fail(function(message) {
		addModalError(message);
	});
	$('#context-menu').remove();
});

// Delete lab node
$(document).on('click', '.action-nodedelete', function(e) {
	logger(1, 'DEBUG: action = action-nodedelete');
	var id = $(this).attr('data-path');
	$.when(deleteNode(id)).done(function(values) {
		$('.node' + id).remove();
	}).fail(function(message) {
		addModalError(message);
	});
	$('#context-menu').remove();
});

// Edit/print node interfaces
$(document).on('click', '.action-nodeinterfaces', function(e) {
	logger(1, 'DEBUG: action = action-nodeinterfaces');
	var id = $(this).attr('data-path');
	$.when(getNodeInterfaces(id)).done(function(values) {
		values['node_id'] = id;
		printFormNodeInterfaces(values)
	}).fail(function(message) {
		addModalError(message);
	});
	$('#context-menu').remove();
});


// Edit/print lab node
$(document).on('click', '.action-nodeedit', function(e) {
	logger(1, 'DEBUG: action = action-nodeedit');
	var id = $(this).attr('data-path');
	$.when(getNodes(id)).done(function(values) {
		values['id'] = id;
		printFormNode('edit', values)
	}).fail(function(message) {
		addModalError(message);
	});
	$('#context-menu').remove();
});

// Print lab nodes
$(document).on('click', '.action-nodesget', function(e) {
	logger(1, 'DEBUG: action = nodesget');
	$.when(getNodes(null)).done(function(nodes) {
		printListNodes(nodes);
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
		values['path'] = dirname($('#lab-viewport').attr('data-path'));
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

// Action menu
$(document).on('click', '.action-moreactions', function(e) {
	logger(1, 'DEBUG: action = moreactions');
	var body = '';
	body += '<li><a class="action-nodesstart" href="#"><i class="glyphicon glyphicon-play"></i> ' + MESSAGES[126] + '</a></li>';
	body += '<li><a class="action-nodesstop" href="#"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[127] + '</a></li>';
	body += '<li><a class="action-nodeswipe href="#"><i class="glyphicon glyphicon-erase"></i> ' + MESSAGES[128] + '</a></li>';
	if (ROLE == 'admin' || ROLE == 'editor') {
		body += '<li><a class="action-nodesexport" href="#"><i class="glyphicon glyphicon-save"></i> ' + MESSAGES[129] + '</a></li>';
		body += '<li><a class="action-labedit" href="#"><i class="glyphicon glyphicon-pencil"></i> ' + MESSAGES[87] + '</a></li>';
	}
	printContextMenu(MESSAGES[125], body, e.pageX, e.pageY);
});

// Redraw topology
$(document).on('click', '.action-labtopologyrefresh', function(e) {
	logger(1, 'DEBUG: action = labtopologyrefresh');
	printLabTopology();
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
	body += '<li><a class="action-nodeplace" href="#"><i class="glyphicon glyphicon-hdd"></i> ' + MESSAGES[81] + '</a></li>';
	body += '<li><a class="action-networkplace" href="#"><i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[82] + '</a></li>';
	body += '<li><a class="action-pictureadd" href="#"><i class="glyphicon glyphicon-picture"></i> ' + MESSAGES[83] + '</a></li>';
	printContextMenu(MESSAGES[80], body, e.pageX, e.pageY);
});

// Add network
$(document).on('click', '.action-networkadd', function(e) {
	logger(1, 'DEBUG: action = networkadd');
	printFormNetwork('add', null);
});

// Place an object
$(document).on('click', '.action-nodeplace, .action-networkplace', function(e) {
	logger(1, 'DEBUG: action = nodeplace');
	var target = $(this);
	$('#context-menu').remove();

	if ($(this).hasClass('action-nodeplace')) {
		var object = 'node';
		var frame = '<div id="mouse_frame" class="context-menu node_frame"><img src="/images/icons/Router.png"/></div>';
		$("#lab-viewport").addClass('lab-viewport-click-catcher');
	} else if ($(this).hasClass('action-networkplace')) {
		var object = 'network';
		var frame = '<div id="mouse_frame" class="context-menu network_frame"><img src="/images/lan.png"/></div>';
		$("#lab-viewport").addClass('lab-viewport-click-catcher');
	} else {
		return false;
	}

	addMessage('info', MESSAGES[100])
	if (!$('#mouse_frame').length) {
		// Add the frame container if not exists
		$('#lab-viewport').append(frame);
	} else {
		$('#mouse_frame').remove();
		$('#lab-viewport').append(frame);
	}

	// On mouse move, adjust css
	$('#lab-viewport').mousemove(function(e1) {
		$('#mouse_frame').css({
			'left': e1.pageX - 30,
			'top': e1.pageY
		});
	});

	// On click open the form
	$('.lab-viewport-click-catcher').click(function(e2) {
		if ($(e2.target).is('#lab-viewport, #lab-viewport *')) {
			// Click is within viewport
			if ($('#mouse_frame').length > 0) {
				// ESC not pressed
				var values = {};
				values['left'] = e2.pageX - 30;
				values['top'] = e2.pageY;
				if (object == 'node') {
					printFormNode('add', values);
				} else if (object == 'network') {
					printFormNetwork('add', values);
				}

				$('#mouse_frame').remove();
			}
			$('#mouse_frame').remove();
			$('.lab-viewport-click-catcher').off();
		} else {
			addMessage('warning', MESSAGES[101])
			$('#mouse_frame').remove();
			$('.lab-viewport-click-catcher').off();
		}

	});
});

// Add picture
$(document).on('click', '.action-pictureadd', function(e) {
	logger(1, 'DEBUG: action = pictureadd');
	$('#context-menu').remove();
	printFormPicture('add', null);
});

// Edit picture
$(document).on('click', '.action-pictureedit', function(e) {
	logger(1, 'DEBUG: action = pictureedit');
	$('#context-menu').remove();
	var picture_id = $(this).attr('data-path');
	$.when(getPictures(picture_id)).done(function(picture) {
		picture['id'] = picture_id;
		printFormPicture('edit', picture);
	}).fail(function(message) {
		addModalError(message);
	});
});

// Get picture
$(document).on('click', '.action-pictureget', function(e) {
	logger(1, 'DEBUG: action = pictureget');
	$('#context-menu').remove();
	var picture_id = $(this).attr('data-path');
	var picture_url = '/api/labs' + $('#lab-viewport').attr('data-path') + '/pictures/' + picture_id + '/data';

	$.when(getPictures(picture_id)).done(function(picture) {
		var picture_map = picture['map'];
		picture_map = picture_map.replace(/{{IP}}/g, location.hostname);
		picture_map = picture_map.replace(/{{NODE[0-9]+}}/g, function(e) { return parseInt(e.substr(6, e.length - 8)) + 32768 + 128 * TENANT});
		// Read privileges and set specific actions/elements
		var body = '<div id="lab_picture"><img usemap="#picture_map" src="' + picture_url + '" alt="' + picture['name'] + '" title="' + picture['name'] + '" width="' + picture['width'] + '" height="' + picture['height'] + '"/><map name="picture_map">' + picture_map + '</map></div>'
		if (ROLE == 'admin' || ROLE == 'editor') {
			var footer = '<button type="button" class="btn btn-aqua action-pictureedit" data-dismiss="modal" data-path="' + picture_id + '">Edit</button>';
		} else {
			var footer = '';
		}
		addModalWide(picture['name'], body, footer);
		$('map').imageMapResize();
	}).fail(function(message) {
		addModalError(message);
	});
});

// Get picture list
$(document).on('click', '.action-picturesget', function(e) {
	logger(1, 'DEBUG: action = picturesget');
	$.when(getPictures()).done(function(pictures) {
		if (!$.isEmptyObject(pictures)) {
			var body = '';
			$.each(pictures, function(key, picture) {
				body += '<li><a class="action-pictureget" data-path="' + key + '" href="#" title="' + picture['name'] + '"><i class="glyphicon glyphicon-picture"></i> ' + picture['name'] + '</a></li>';
			});
			printContextMenu(MESSAGES[59], body, e.pageX, e.pageY);
		} else {
			addMessage('info', MESSAGES[134]);
		}
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

// Export a config
$(document).on('click', '.action-nodeexport, .action-nodesexport', function(e) {
	$('#context-menu').remove();
	if ($(this).hasClass('action-nodeexport')) {
		logger(1, 'DEBUG: action = nodeexport');
		var node_id = $(this).attr('data-path');
	} else {
		logger(1, 'DEBUG: action = nodesexport');
		var node_id = null;
	}

	$.when(getNodes(null)).done(function(nodes) {
		if (node_id != null) {
			$.when(cfg_export(node_id)).done(function() {
				// Node exported -> print a small green message
				addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[79])
			}).fail(function(message) {
				// Cannot export
				addMessage('danger', nodes[node_id]['name'] + ': ' + message);
			});
		} else {
			$.each(nodes, function(key, values) {
				$.when(setTimeout(function() { cfg_export(key); }, values['delay'] * 10)).done(function() {
					// Node exported -> print a small green message
					addMessage('success', values['name'] + ': ' + MESSAGES[79])
				}).fail(function(message) {
					// Cannot exported
					addMessage('danger', values['name'] + ': ' + message);
				});
			});
		}
	}).fail(function(message) {
		addModalError(message);
	});
});

// Start a node
$(document).on('click', '.action-nodestart, .action-nodesstart', function(e) {
	$('#context-menu').remove();
	if ($(this).hasClass('action-nodestart')) {
		logger(1, 'DEBUG: action = nodestart');
		var node_id = $(this).attr('data-path');
	} else {
		logger(1, 'DEBUG: action = nodesstart');
		var node_id = null;
	}

	$.when(getNodes(null)).done(function(nodes) {
		if (node_id != null) {
			$.when(start(node_id)).done(function() {
				// Node started -> print a small green message
				addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[76])
				printLabStatus();
			}).fail(function(message) {
				// Cannot start
				addMessage('danger', nodes[node_id]['name'] + ': ' + message);
			});
		} else {
			var nodeLenght = Object.keys(nodes).length;
			$.each(nodes, function(key, values) {
				$.when(start(key)).done(function() {
					// Node started -> print a small green message
					addMessage('success', values['name'] + ': ' + MESSAGES[76])
					nodeLenght--;
					if(nodeLenght < 1){
						printLabStatus();
					};
				}).fail(function(message) {
					// Cannot start
					addMessage('danger', values['name'] + ': ' + message);
					nodeLenght--;
					if(nodeLenght < 1){
						printLabStatus();
					};
				});
			});
		}
	}).fail(function(message) {
		addModalError(message);
	});
});

// Stop a node
$(document).on('click', '.action-nodestop, .action-nodesstop', function(e) {
	$('#context-menu').remove();
	if ($(this).hasClass('action-nodestop')) {
		logger(1, 'DEBUG: action = nodestop');
		var node_id = $(this).attr('data-path');
	} else {
		logger(1, 'DEBUG: action = nodesstop');
		var node_id = null;
	}

	$.when(getNodes(null)).done(function(nodes) {
		if (node_id != null) {
			$.when(stop(node_id)).done(function() {
				// Node stopped -> print a small green message
				addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[77])
				printLabStatus();
			}).fail(function(message) {
				// Cannot stop
				addMessage('danger', nodes[node_id]['name'] + ': ' + message);
			});
		} else {
			var nodeLenght = Object.keys(nodes).length;
			$.each(nodes, function(key, values) {
				$.when(stop(key)).done(function() {
					// Node stopped -> print a small green message
					addMessage('success', values['name'] + ': ' + MESSAGES[77])
					nodeLenght--;
					if(nodeLenght < 1){
						setTimeout(printLabStatus, 1000);
					};
				}).fail(function(message) {
					// Cannot stopped
					addMessage('danger', values['name'] + ': ' + message);
					nodeLenght--;
					if(nodeLenght < 1){
						setTimeout(printLabStatus, 1000);
					};
				});
			});
		}
	}).fail(function(message) {
		addModalError(message);
	});
});

// Wipe a node
$(document).on('click', '.action-nodewipe, .action-nodeswipe', function(e) {
	$('#context-menu').remove();
	if ($(this).hasClass('action-nodewipe')) {
		logger(1, 'DEBUG: action = nodewipe');
		var node_id = $(this).attr('data-path');
	} else {
		logger(1, 'DEBUG: action = nodeswipe');
		var node_id = null;
	}

	$.when(getNodes(null)).done(function(nodes) {
		if (node_id != null) {
			$.when(wipe(node_id)).done(function() {
				// Node wiped -> print a small green message
				addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[78])
			}).fail(function(message) {
				// Cannot wipe
				addMessage('danger', nodes[node_id]['name'] + ': ' + message);
			});
		} else {
			$.each(nodes, function(key, values) {
				$.when(setTimeout(function() { wipe(key); }, values['delay'] * 10)).done(function() {
					// Node wiped -> print a small green message
					addMessage('success', values['name'] + ': ' + MESSAGES[78])
				}).fail(function(message) {
					// Cannot wiped
					addMessage('danger', values['name'] + ': ' + message);
				});
			});
		}
	}).fail(function(message) {
		addModalError(message);
	});
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
$(document).on('click', '.action-update', function(e) {
	logger(1, 'DEBUG: action = update');
	addMessage('info', MESSAGES[133]);
	$.when(update()).done(function(message) {
		// Got user
		addMessage('success', message);
	}).fail(function(message) {
		// Cannot get user
		addMessage('alert', message);
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
				$(e.target).parents('.modal').attr('skipRedraw', true);
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
				$(e.target).parents('.modal').attr('skipRedraw', true);
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
	var lab_filename = $('#lab-viewport').attr('data-path');
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

	if ($(this).attr('id') == 'form-node-add') {
		// If adding need to manage multiple add
		if (form_data['count'] > 1) {
			form_data['postfix'] = 1;
		} else {
			form_data['postfix'] = 0;
		}
	} else {
		// If editing need to post once
		form_data['count'] = 1;
		form_data['postfix'] = 0;
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
				$(e.target).parents('.modal').attr('skipRedraw', true);
				$(e.target).parents('.modal').modal('hide');
				if (type == 'POST') {
					// Reload the lab list
					printPageLabList(form_data['path']);
				} else if (basename(lab_filename) != form_data['name'] + '.unl') {
					// Lab has been renamed, need to close it.
					logger(1, 'DEBUG: lab "' + form_data['name'] + '" renamed.');
					$.when(closeLab()).done(function() {
						printPageLabOpen(dirname(form_data['path']) + '/' + form_data['name'] + '.unl');
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

// Submit network form
$(document).on('submit', '#form-network-add, #form-network-edit', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var lab_filename = $('#lab-viewport').attr('data-path');
	var form_data = form2Array('network');
	var promises = [];
	if ($(this).attr('id') == 'form-network-add') {
		logger(1, 'DEBUG: posting form-network-add form.');
		var url = '/api/labs' + lab_filename + '/networks';
		var type = 'POST';
	} else {
		logger(1, 'DEBUG: posting form-network-edit form.');
		var url = '/api/labs' + lab_filename + '/networks/' + form_data['id'];
		var type = 'PUT';
	}

	if ($(this).attr('id') == 'form-network-add') {
		// If adding need to manage multiple add
		if (form_data['count'] > 1) {
			form_data['postfix'] = 1;
		} else {
			form_data['postfix'] = 0;
		}
	} else {
		// If editing need to post once
		form_data['count'] = 1;
		form_data['postfix'] = 0;
	}

	for (var i = 0; i < form_data['count']; i++) {
		form_data['left'] = parseInt(form_data['left']) + i * 10;
		form_data['top'] = parseInt(form_data['top']) + i * 10;
		var request = $.ajax({
			timeout: TIMEOUT,
			type: type,
			url: encodeURI(url),
			dataType: 'json',
			data: JSON.stringify(form_data),
			success: function(data) {
				if (data['status'] == 'success') {
					logger(1, 'DEBUG: network "' + form_data['name'] + '" saved.');
					// Close the modal
					$('body').children('.modal').attr('skipRedraw', true);
					$('body').children('.modal').modal('hide');
					addMessage(data['status'], data['message']);
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
		promises.push(request);
	}

	$.when.apply(null, promises).done(function() {
		printLabTopology();
	});
	return false;  // Stop to avoid POST
});

// Submit node interfaces form
$(document).on('submit', '#form-node-connect', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var lab_filename = $('#lab-viewport').attr('data-path');
	var form_data = form2Array('interfc');
	var node_id = $('form :input[name="node_id"]').val();
	var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/interfaces';
	var type = 'PUT';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: node "' + node_id + '" saved.');
				// Close the modal
				$('body').children('.modal').attr('skipRedraw', true);
				$('body').children('.modal').modal('hide');
				addMessage(data['status'], data['message']);
				printLabTopology();
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
});

// Submit node form
$(document).on('submit', '#form-node-add, #form-node-edit', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var lab_filename = $('#lab-viewport').attr('data-path');
	var form_data = form2Array('node');
	var promises = [];
	if ($(this).attr('id') == 'form-node-add') {
		logger(1, 'DEBUG: posting form-node-add form.');
		var url = '/api/labs' + lab_filename + '/nodes';
		var type = 'POST';
	} else {
		logger(1, 'DEBUG: posting form-node-edit form.');
		var url = '/api/labs' + lab_filename + '/nodes/' + form_data['id'];
		var type = 'PUT';
	}

	if ($(this).attr('id') == 'form-node-add') {
		// If adding need to manage multiple add
		if (form_data['count'] > 1) {
			form_data['postfix'] = 1;
		} else {
			form_data['postfix'] = 0;
		}
	} else {
		// If editing need to post once
		form_data['count'] = 1;
		form_data['postfix'] = 0;
	}

	for (var i = 0; i < form_data['count']; i++) {
		form_data['left'] = parseInt(form_data['left']) + i * 10;
		form_data['top'] = parseInt(form_data['top']) + i * 10;
		var request = $.ajax({
			timeout: TIMEOUT,
			type: type,
			url: encodeURI(url),
			dataType: 'json',
			data: JSON.stringify(form_data),
			success: function(data) {
				if (data['status'] == 'success') {
					logger(1, 'DEBUG: node "' + form_data['name'] + '" saved.');
					// Close the modal
					$('body').children('.modal').attr('skipRedraw', true);
					$('body').children('.modal').modal('hide');
					addMessage(data['status'], data['message']);
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

	$.when.apply(null, promises).done(function() {
		printLabTopology();
	});
	return false;  // Stop to avoid POST
});

// Submit config form
$(document).on('submit', '#form-node-config', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var lab_filename = $('#lab-viewport').attr('data-path');
	var form_data = form2Array('config');
	var url = '/api/labs' + lab_filename + '/configs/' + form_data['id'];
	var type = 'PUT';
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
				logger(1, 'DEBUG: config saved.');
				// Close the modal
				$('body').children('.modal').attr('skipRedraw', true);
				$('body').children('.modal').modal('hide');
				addMessage(data['status'], data['message']);
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
				$(e.target).parents('.modal').attr('skipRedraw', true);
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
				$(e.target).parents('.modal').attr('skipRedraw', true);
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
