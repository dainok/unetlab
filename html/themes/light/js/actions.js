// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/light/js/actions.js
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
 * @version 20150522
 */

// Clear field content on login form
$(document).on('focus', 'input[name^="login["]', function(e) {
	$(this).removeAttr('value');
});

// Submit login form
$(document).on('submit', '#form-login', function(e) {
	e.preventDefault();  // Prevent default behaviour
	var form_data = form2Array('login');
	var url = '/api/auth/login';
    var type = 'POST'
	$.ajax({
		timeout: TIMEOUT,
		type: type,
		url: encodeURI(url),
		dataType: 'json',
		data: JSON.stringify(form_data),
		success: function(data) {
			if (data['status'] == 'success') {
                logger(1, 'DEBUG: user is authenticated.');
				raiseMessage('SUCCESS', data['message']);
				$('body').html(getPageHome());
			} else {
				// Authentication error
                logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				raisePermanentMessage('ERROR', data['status']);
			}
		},
		error: function(data) {
			// Authentication error
			var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			raisePermanentMessage('ERROR', message);
		}
	});
    return false;  // Stop to avoid POST
});

// Logout button
$(document).on('click', '#button-logout', function(e) {
	e.preventDefault();  // Prevent default behaviour
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
				raiseMessage('SUCCESS', data['message']);
				$('body').html(getPageAuthentication());
			} else {
				// Authentication error
                logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				raisePermanentMessage('ERROR', data['status']);
			}
		},
		error: function(data) {
			// Authentication error
			var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
			logger(1, 'DEBUG: ' + message);
			raisePermanentMessage('ERROR', message);
		}
	});
    return false;
});

// Close button
$(document).on('click', '.close', function(e) {
	closeCenterBox($(this));
});

// Key-up event
$(document).keyup(function(e) {
	if (e.keyCode == 27) {
		// ESC
		$('.close').each(function() {
			closeCenterBox($(this));
		});
	}
});

// Click away from center box
$(document).on('click', '.box-center-content', function(e) {
	// Do not close if click is on content
	e.stopPropagation();
});
$(document).on('click', '.box-center-container', function(e) {
	// Click is on container, close the box
	$('.close').each(function() {
		closeCenterBox($(this));
	});
});

// Open a folder
$(document).on('click', '.folder-link', function(e) {
	var folder_path = $(this).attr('data-path');
	$.when(getFolderContent(folder_path)).done(function(data) {
		// Folder loaded
		logger(1, 'DEBUG: folder "' + folder_path + '" loaded.');
		$('#main').html(getPageHome(data['data']['folders'], data['data']['labs']));
	}).fail(function(data) {
		// Cannot load folder content
		var message = getJsonMessage(data['responseText']);
		logger(1, 'DEBUG: cannot load folder "' + folder_path + '".');
		raisePermanentMessage('ERROR', message);
	});;
});

// Preview a lab
$(document).on('click', '.lab-link', function(e) {
	var lab_path = $(this).attr('data-path');
	$.when(getLabPreview(lab_path)).done(function(data) {
		// Lab loaded
		logger(1, 'DEBUG: lab "' + lab_path + '" loaded.');
		//$('#main').html(getPageHome(data['data']['folders'], data['data']['labs']));
	}).fail(function(data) {
		// Cannot preview lab
		var message = getJsonMessage(data['responseText']);
		logger(1, 'DEBUG: cannot preview lab "' + lab_path + '".');
		raisePermanentMessage('ERROR', message);
	});;
});
