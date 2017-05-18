/* UNetLabv2 UI - functions
 * ================
 * @author    Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright Andrea Dainese <andrea.dainese@gmail.com>
 * @license   https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
 * @revision  2.3.8
 */

// Convert form data into JSON 
function formToJSON(form) {
    var form_array = {}
    var key = null;
    var value = null;
    $.each(form.serializeArray(), function(object_id, object) {
        $.each(object, function(field, data) {
            if (key == null) {
                key = data;
            } else {
                value = data;
                form_array[key] = value;
                value = null;
                key = null;
            }
        });
    });
    return form_array;
}

// Insert role in DataTable
function insertRoleTable(role) {
    roleTable.row.add($('<tr data-url="/api/v1/roles/' + role.role + '"><td>' + role.role + '</td><td data-editable data-name="access_to" data-type="text">' + role.access_to + '</td><td data-editable data-name="can_write" data-type="select" data-options="{&quot;true&quot;:true,&quot;false&quot;:false}">' + role.can_write + '</td></tr>')[0]).draw();
}

// Check if a user is authenticated
function isAuthenticated() {
    var deferred = $.Deferred();
    var username = localStorage.getItem('username');
    var password = localStorage.getItem('password')
    if (username != null && password != null) {
        $.when(getUrl('/api/v1/auth')).done(function(data) {
            if (data.status == 'success') {
                deferred.resolve(true);
            } else {
                deferred.reject(false);
                localStorage.removeItem('username');
                localStorage.removeItem('password');
                localStorage.removeItem('isadmin');
                rc = false;
            }
        }).fail(function(data) {
            deferred.reject(false);
            localStorage.removeItem('username');
            localStorage.removeItem('password');
            localStorage.removeItem('isadmin');
        });
    } else {
        deferred.reject(false);
    }
    return deferred.promise();
}

// Notify a message to a user
function notifyUser(priority, message) {
	priority = priority.toUpperCase();
	if (!('Notification' in window) || Notification.permission !== 'granted') {
		// Browser does not support notification or not granted
		alert(priority + ': ' + message);
	} else {
		if (priority === 'error') {
			timeout = 5000;
		} else {
			timeout = 3000;
		}
		var notification = new Notification(priority + ': ' + message);
		setTimeout(notification.close.bind(notification), timeout); 
	}
}

// Set data-user
function setUserData() {
    var username = localStorage.getItem('username');
    var password = localStorage.getItem('password')
    // Setting user's profile
    $.when(getUrl('/api/v1/auth')).done(function(data) {
        $.each(data.data, function(key, value) {
            $('.data-user-' + key).each(function() {
                if ($(this).get(0).tagName == 'INPUT') {
                    $(this).val(value);
                } else {
                    $(this).text(value);
                }
            });
        });
    });
    // Setting admin functions
    if (localStorage.getItem('isadmin') != null) {
        $('.admin-item').each(function() {
            $(this).removeClass('hidden');
        });
    }
}
