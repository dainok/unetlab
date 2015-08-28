// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/light/js/new-validate.js
 *
 * User's input validation scripts
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
 * @version 20150819
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