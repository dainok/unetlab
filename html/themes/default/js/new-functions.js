// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/light/js/functions.js
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
 * @version 20150522
 */

// Add Modal
function addModal(title, body, footer) {
	var html = '<div aria-hidden="false" style="display: block;" class="modal fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">' + body + '</div><div class="modal-footer">' + footer + '</div></div></div></div>';
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
	var message = '';
	try {
		message = JSON.parse(response)['message'];
	} catch(e) {
		message = 'Undefined message, see logs under "/opt/unetlab/data/Logs/".';
	}
	return message;
}

// Return Authentication Page
function printPageAuthentication() {
	var html = '<div class="row full-height"><div class="col-md-5 col-lg-5 full-height" id="auth-left"><div class="middle"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img alt="Logo RR" src="/themes/default/images/logo-rr.png" /></div></div><!-- <div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><img alt="Signup Icon" src="/themes/default/images/button-signup.png"></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">to access more features</div></div> --><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2">Existing user...</div></div><form id="form-login"><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[username]" placeholder="USERNAME" type="text" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input name="login[password]" placeholder="PASSWORD" type="password" /></div></div><div class="row"><div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2"><input alt="Login Icon" src="/themes/default/images/button-login.png" type="image" /></div></div></form></div></div><div class="col-md-7 col-lg-7" id="auth-right"><div id="logo-angular"><img alt="Logo Angular" src="/themes/default/images/logo-angular.png" /></div><div id="logo-ad"><img alt="Logo AD" src="/themes/default/images/logo-ad.png" /></div><div id="logo-text"><h1>Unified Networking Lab</h1><p>UNetLab can be considered the next major version of<br>iou-web, but the software has been rewritten from<br>scratch. The major advantage over GNS3 and<br>iou-web itself is about multi-hypervisor<br>support within a single entity. UNetLab<br>allows to design labs using IOU, Dy-<br>namips and QEMU nodes without<br>dealing with multi virtual ma-<br>chines: everything run in-<br>side a UNetLab host,<br>and a lab is a single<br>file including all<br>information<br>needed.</p></div></div></div>'
	$('#body').html(html);
}

// Return Lab List page
function printPageLabList() {
	var html = '';

html += '<div id="navbar-list" class="navbar" role="navigation">';
html += '<div class="container-fluid">';
html += '<div class="navbar-header" style="background-color: #46a6b6; padding: 20px 58px 20px 58px;"><img height=100" src="/themes/default/images/logo-rr.png" width="266"/></div>'; 
html += '<div class="collapse navbar-collapse navbar-menubuilder">';
html += '<ul class="nav navbar-nav navbar-left">';
html += '<li><a href="#">Home</a></li>';
html += '<li><a href="#">User Menu</a></li>';
html += '<li><a href="#">Lab</a></li>';
html += '<li><a href="#">System Status</a></li>';
html += '<li><a href="#">Logout</a></li>';
html += '</ul>';
html += '</div>';
html += '</div>';
html += '</div>';
	
html += '<div class="row full-height" style="background-color: #ffffff;">';
html += '<div class="col-md-3 col-lg-3 full-height" id="list_folders">folders</div>';
html += '<div class="col-md-3 col-lg-3 full-height" id="list_labs">labs</div>';
html += '<div class="col-md-6 col-lg-6 full-height" id="preview_lab">lab</div>';
html += '</div>';

	$('#body').html(html);
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
				deferred.resolve(data);
			} else {
				logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
				deferred.reject(data);
			}
		},
		error: function(data) {
			var message = getJsonMessage(data['responseText']);
			logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
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
