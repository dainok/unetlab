// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/light/js/elements.js
 *
 * Functions for get HTML elements
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

// Get authentication page
function getPageAuthentication() {
	var page = '<div id="main"><div id="frame-auth-lx"><div class="center" id="box-img-rr"><img src="/themes/light/images/logo-rr.png"/></div><div class="center" id="box-img-signup"><a href="#"><img src="/themes/light/images/button-signup.png"/></a><div id="text-signup">to access more features</div></div><div class="center" id="box-img-login"><form id="form-login"><div id="text-login">Existing user...</div><div><input name="login[username]" type="text" value="USERNAME"/></div><div><input name="login[password]" type="password" value="PASSWORD"/></div><input src="/themes/light/images/button-login.png" type="image"/></form></div></div><div id="frame-auth-rx"><div id="box-img-angular"><img src="/themes/light/images/logo-angular.png"/></div><div id="box-img-ad"><img src="/themes/light/images/logo-ad.png"/></div><div id="box-text-info"><h1>Unified Networking Lab</h1><p>UNetLab can be considered the next major version of<br/>iou-web, but the software has been rewritten from<br/>scratch. The major advantage over GNS3 and<br/>iou-web itself is about multi-hypervisor<br/>support within a single entity. UNetLab<br/>allows to design labs using IOU, Dy-<br/>namips and QEMU nodes without<br/>dealing with multi virtual ma-<br/>chines: everything run in-<br/>side a UNetLab host,<br/>and a lab is a single<br/>file including all<br/>information<br/>needed.</p></div></div></div>';
	return page;
}

// Get home page
function getPageHome(folders, labs) {
	var page = '';
	page = '<div id="frame-list-top">';
	page += '<div id="frame-list-top-logo"><div id="box-img-rr"><img src="/themes/light/images/logo-rr.png"/></div></div>';
	page += '<div id="frame-list-top-menu">';
	page += '<a href="#"><div class="box-menu-item">Home</div></a>';
	page += '<div class="box-menu-spacer">&nbsp;</div>';
	page += '<a href="#"><div class="box-menu-item">User Menu</div></a>';
	page += '<div class="box-menu-spacer">&nbsp;</div>';
	page += '<a href="#"><div class="box-menu-item">Lab</div></a>';
	page += '<div class="box-menu-spacer">&nbsp;</div>';
	page += '<a href="#"><div class="box-menu-item">System Status</div></a>';
	page += '<div class="box-menu-spacer">&nbsp;</div>';
	page += '<a href="#" id="button-logout"><div class="box-menu-item">Logout</div></a>';
	page += '</div>';
	page += '</div>';
	page += '<div id="frame-list-main">';
	page += '<div id="frame-list-folders"><ul>';
	$.each(folders, function(id, object) {
		page += '<li><a class="folder-link" data-path="' + object['path'] + '" href="#">' + object['name'] + '</a></li>';
	});
	page += '</ul></div>';
	page += '<div id="frame-list-labs"><ul>';
	$.each(labs, function(id, object) {
		page += '<li><a class="lab-link" data-path="' + object['path'] + '" href="#">' + object['file'] + '</a></li>';
	});
	page += '</ul></div>';
	page += '<div id="frame-list-info">';
	page += '<div id="frame-list-thumbnail"></div>';
	page += '<div id="frame-list-desc"></div>';
	page += '</div>';
	page += '</div>';
	page += '<div id="frame-list-main-title">';
	page += '<div id="title-folders">Folders</div>';
	page += '<div id="title-labs">Labs</div>';
	page += '<div id="title-info">Info</div>';
	page += '</div>';
	return page;
}

// Get center box
function getCenterBox(title, content, buttons, height, width) {
	var style = '';
	if (height != undefined) {
		style += 'height:' + height + '%;';
	}
	if (width != undefined) {
		style += 'width:' + width + '%;';
	}
	if (buttons != undefined) {
		buttons = '<div class="box-center-buttons">' + buttons + '</div>';
	} else {
		buttons = '';
	}

	//page = '<div class="box-center-container"><div class="box-center-content" style="' + style + '"><div class="box-close"><a class="close" href="#"><img alt="Close" class="top" src="/themes/light/images/close.gif"/></a></div><div class="box-center-head"><img alt="Triangle" src="/themes/light/images/triangle.gif"/> ' + title + '</div><div class="box-center-body">' + content + '</div><div class="box-center-buttons"><input class="button-blue" type="submit" value="OK"/>&nbsp;<input class="button-grey" type="submit" value="Cancel"/></div></div></div> TODO';
	var page = '<div class="box-center-container"><div class="box-center-content" style="' + style + '"><div class="box-close"><a class="close" href="#"><img alt="Close" class="top" src="/themes/light/images/close.gif"/></a></div><div class="box-center-head"><img alt="Triangle" src="/themes/light/images/triangle.gif"/><div>' + title + '</div></div><div class="box-center-body">' + content + '</div>' + buttons + '</div></div>';
	page = '<div class="box-center-container"><div class="box-center-content" style="' + style + '"><div class="box-close"><a class="close" href="#"><img alt="Close" class="top" src="/themes/light/images/close.gif"/></a></div><div class="box-center-head"><img alt="Triangle" src="/themes/light/images/triangle.gif"/><div>' + title + '</div></div><div class="box-center-body">' + content + '</div>' + buttons + '</div></div>';
	return page;
}
