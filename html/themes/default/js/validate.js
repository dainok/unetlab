// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/validate.js
 *
 * User's input validation scripts
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

$.validator.setDefaults({
    debug: true,
    success: "valid"
});

// Validate an interger
$.validator.addMethod('integer', function(value) {
    return /^[0-9]+$/.test(value); 
}, 'Must be interger ([0-9] chars).');

// Validate a lab name
$.validator.addMethod('lab_name', function(value) {
    return /^[A-Za-z0-9_\-\s]+$/.test(value); 
}, 'Use only [A-Za-z0-9_- ] chars.');


// Validate a username
$.validator.addMethod('username', function(value) {
    return /^[A-Za-z0-9]+$/.test(value); 
}, 'Must be alphanumeric ([A-Za-z0-9] chars).');

// Validate a ISO date
$.validator.addMethod('date', function(value) {
    return /(?:^$|^[0-9]{4}-[0-9]{2}-[0-9]{2}$)/.test(value); 
}, 'Must be empty or an ISO date (YYYY-MM-DD).');

// Validate folder form
function validateFolder() {
	$('#form-folder-add').validate({
		rules: {
			'folder[name]': {
				required: true,
				lab_name: true
			}
		}
	});
	$('#form-folder-rename').validate({
		rules: {
			'folder[name]': {
				required: true,
				lab_name: true
			}
		}
	});
}

// Validate import form
function validateImport() {
	$('#form-import').validate({
		rules: {
			'import[file]': {
				required: true,
			}
		}
	});
}

// Validate lab info form
function validateLabInfo() {
	$('#form-lab-add').validate({
		rules: {
			'lab[name]': {
				required: true,
				lab_name: true
			},
			'lab[version]': {
				required: false,
				integer: true
			}
		}
	});
}

// Validate user form
function validateUser() {
	$('#form-user-add, #form-user-edit').validate({
		rules: {
			'user[username]': {
				required: true,
				username: true
			},
			'user[email]': {
				required: true,
				email: true
			},
			'user[expiration]': {
				required: false,
				date: true
			},
			'user[pexpiration]': {
				required: false,
				date: true
			},
			'user[pod]': {
				required: false,
				range: [0, 255]
			}
		}
	});
}

// Validate node form
function validateNode() {
	$('#form-node-add, #form-node-edit').validate({
		rules: {
			'node[nvram]': {
				range: [128, 1024]
			},
			'node[email]': {
				required: true,
				email: true
			},
			'node[expiration]': {
				required: false,
				date: true
			},
			'node[pexpiration]': {
				required: false,
				date: true
			},
			'node[pod]': {
				required: false,
				range: [0, 255]
			}
		}
	});
}

// Validate lab picture form
function validateLabPicture() {
    $('.form-picture').validate({
        rules: {
            'picture[name]': {
                required: true
            }
        }
    });
}
