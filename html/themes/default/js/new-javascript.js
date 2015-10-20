// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/new-javascript.js
 *
 * Startup scripts
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
 * @version 20150907
 */

// Custom vars
var DEBUG = 5;
var TIMEOUT = 30000;

// Global vars, defined on getUserInfo()
var EMAIL;
var FOLDER;
var LAB;
var LANG;
var NAME;
var ROLE;
var TENANT;
var USERNAME;

$(document).ready(function() {
	if ($.cookie('privacy') != 'true') {
		// Cookie is not set, show a modal with privacy policy
		logger(1, 'DEBUG: need to accept privacy.');
		addModal(MESSAGES[0], MESSAGES[1], '<button id="privacy" type="button" class="btn btn-aqua" data-dismiss="modal">' + MESSAGES[2] + '</button>');
	} else {
		// Privacy policy already been accepted, check if user is already authenticated
		$.when(getUserInfo()).done(function() {
			// User is authenticated
			logger(1, 'DEBUG: loading home page.');
			printPageLabList(FOLDER);
		}).fail(function() {
			// User is not authenticated, or error on API
			logger(1, 'DEBUG: loading authentication page.');
			printPageAuthentication();
		});
	}
});

// Attach files
var ATTACHMENTS;
$('body').on('change', 'input[type=file]', function(e) {
    ATTACHMENTS = e.target.files;
});
