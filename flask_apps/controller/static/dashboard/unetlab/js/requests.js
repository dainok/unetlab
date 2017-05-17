/* UNetLabv2 UI - AJAX requests
 * ================
 * @author    Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright Andrea Dainese <andrea.dainese@gmail.com>
 * @license   https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
 * @revision  2.3.8
 */

var DEMO = false;
var TIMEOUT = 3000

// GET Url
function getUrl(url) {
	var deferred = $.Deferred();
	if (DEMO) {
        console.log('not implemented');
	} else {
		$.ajax({
			dataType: 'json',
			timeout: TIMEOUT,
			type: 'GET',
			url: url,
            headers: {'Authorization': 'Basic ' + btoa(localStorage.getItem('username') + ':' + localStorage.getItem('password'))}
		}).done(function(data) {
            if (data['status'] == 'success') {
                deferred.resolve(data);
            } else {
                deferred.reject(data);
            }
		}).fail(function(jqXHR, textStatus, errorThrown) {
			deferred.reject({
				status: 'fail',
				code: '500',
				message: textStatus
			});
		});
	}
	return deferred.promise();
}

// PATCH Url
function patchUrl(url, form_data) {
	var deferred = $.Deferred();
	if (DEMO) {
        console.log('not implemented');
	} else {
		$.ajax({
			contentType: 'application/json',
            data: JSON.stringify(form_data),
			dataType: 'json',
			timeout: TIMEOUT,
			type: 'PATCH',
			url: url,
            headers: {'Authorization': 'Basic ' + btoa(localStorage.getItem('username') + ':' + localStorage.getItem('password'))}
		}).done(function(data) {
            if (data['status'] == 'success') {
                deferred.resolve(data);
            } else {
                deferred.reject(data);
            }
		}).fail(function(jqXHR, textStatus, errorThrown) {
			deferred.reject({
				status: 'fail',
				code: jqXHR.status,
				message: jqXHR.responseJSON.message
			});
		});
	}
	return deferred.promise();
}

// POST Url
function postUrl(url, form_data) {
	var deferred = $.Deferred();
	if (DEMO) {
        console.log('not implemented');
	} else {
		$.ajax({
			contentType: 'application/json',
            data: JSON.stringify(form_data),
			dataType: 'json',
			timeout: TIMEOUT,
			type: 'POST',
			url: url,
            headers: {'Authorization': 'Basic ' + btoa(localStorage.getItem('username') + ':' + localStorage.getItem('password'))}
		}).done(function(data) {
            if (data['status'] == 'success') {
                deferred.resolve(data);
            } else {
                deferred.reject(data);
            }
		}).fail(function(jqXHR, textStatus, errorThrown) {
			deferred.reject({
				status: 'fail',
				code: jqXHR.status,
				message: jqXHR.responseJSON.message
			});
		});
	}
	return deferred.promise();
}

