// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/javascript.js
 *
 * Startup scripts
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

// Custom vars
var DEBUG = 5;
var TIMEOUT = 30000;
var LONGTIMEOUT = 600000;
var STATUSINTERVAL = 5000;

// Global vars
var EMAIL;
var FOLDER;
var LAB;
var LANG;
var NAME;
var ROLE;
var TENANT;
var USERNAME;
var ATTACHMENTS;
var UPDATEID;


$(document).ready(function() {
	if ($.cookie('privacy') != 'true') {
		// Cookie is not set, show a modal with privacy policy
		logger(1, 'DEBUG: need to accept privacy.');
		addModal('Privacy Policy', '<p>We use cookies on this site for our own business purposes including collecting aggregated statistics to analyze how our site is used, integrating social networks and forums and to show you ads tailored to your interests. Find out our <a href="http://www.unetlab.com/about/privacy.html" title="Privacy Policy">privacy policy</a> for more information.</p><p>By continuing to browse the site, you are agreeing to our use of cookies.</p>', '<button id="privacy" type="button" class="btn btn-aqua" data-dismiss="modal">Accept</button>');
	} else {
		// Privacy policy already been accepted, check if user is already authenticated
		$.when(getUserInfo()).done(function() {
			// User is authenticated
			logger(1, 'DEBUG: loading language.');
			$.getScript('/themes/default/js/messages_' + LANG + '.js')
				.done(function() {
					postLogin();
				})
				.fail(function() {
					logger(1, 'DEBUG: error loading language.');
				});
		}).fail(function(data) {
			// User is not authenticated, or error on API
			logger(1, 'DEBUG: loading authentication page.');
			printPageAuthentication();
		});
	}
});
