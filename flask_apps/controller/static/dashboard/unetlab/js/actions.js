/* UNetLabv2 UI - actions
 * ================
 * @author    Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright Andrea Dainese <andrea.dainese@gmail.com>
 * @license   https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
 * @revision  2.3.8
 */

$('body').on('click', '[data-editable]', function(event) {
    // Loading data from elements
    var $element = $(this);
    var url = $element.parents('tr').attr('data-url');
    var name = $element.attr('data-name');
    var type = $element.attr('data-type');

    if (type == 'password') {
        // If input type is password, give a blank item
        var value = '';
    } else {
        var value = $element.text();
    }

    // Create and insert form elements
    var $div = $('<div class="input-group input-group-sm"/>');
    var $input = $('<input name="' + name + '" type="' + type + '" class="form-control"/>').val(value);
    $element.empty()
    $div.append($input);
    $element.append($div);

    // What to do when abort
    var abort = function() {
        if (type == 'password' && $input.val() == '') {
            $element.text('**********');
        } else {
            $element.text(value);
        }
    };

    // What to do when save
    var save = function() {
        form_data = {};
        form_data[name] = $input.val();
        $.when(patchUrl(url, form_data)).done(function(data) {
            if (type == 'password' && $input.val() == '') {
                $element.text('**********');
            } else {
                $element.text($input.val());
            }
        }).fail(function(data) {
            notifyUser('error', data.message);
            abort();
        });
    };

    // Trigger actions
    $input.one('blur', abort).focus();
    $input.keydown(function(event) {
        var key = event.charCode ? event.charCode : event.keyCode ? event.keyCode : 0;
        if (key == 13) {
            save();
            event.preventDefault();
        } else if (key == 27) {
            // TODO: trigger modal close
            abort();
            event.preventDefault();
        }
    });
});

$('body').on('click', '[data-selectable]', function(event) {
    // Loading data from elements
    var $element = $(this);
    var url = $element.parents('tr').attr('data-url');
    var name = $element.attr('data-name');
    var $select = $element.find('select');
    //var value = $element.find('option:selected').text();
    var value = $select.val();

    // What to do when abort
    var abort = function() {
        $element.val(value);
    };

    // What to do when save
    var save = function() {
        form_data = {};
        new_value = $select.val()
        if (new_value == 'true') {
            // Set true as boolean
            form_data[name] = true;
        } else if (new_value == 'false') {
            // Set false as boolean
            form_data[name] = false;
        } else {
            form_data[name] = new_value;
        }
        $.when(patchUrl(url, form_data)).fail(function(data) {
            notifyUser('error', data.message);
            abort();
        });
    };

    // Trigger actions
    $select.one('blur', abort).focus();
    $select.one('change', save);
});

$('#form-login').on('submit', function(event) {
	form_data = formToJSON($(this));
    localStorage.setItem('username', form_data['username']);
    localStorage.setItem('password', form_data['password']);
	$.when(getUrl('/api/v1/auth')).done(function(data) {
        $.each(data.data.roles, function(key, value) {
            if (value == 'admin') {
                localStorage.setItem('isadmin', true);
            }
        });
		$(window.location).attr('href', 'home.html');
	}).fail(function(data) {
		$('#form-login, input').val('');
		notifyUser('error', data.message);
        localStorage.removeItem('username');
        localStorage.removeItem('password');
        localStorage.removeItem('isadmin');
	});
	event.preventDefault()
});

$('#form-profile').on('submit', function(event) {
	form_data = formToJSON($(this));
	$.when(patchUrl('/api/v1/auth', form_data)).done(function(data) {
		notifyUser('info', data['message']);
        $('#modal-profile').modal('toggle');
        if (form_data['password'] != '') {
          // Update the cached password
          localStorage.setItem('password', form_data['password']);
          // Remove password from form
          $('#form-profile input[type=password]').val('');
        }
        // Update data
        setUserData();
    }).fail(function(data) {
        $('#form-login, input').val('');
        notifyUser('error', data.message);
    });
	event.preventDefault()
});

$('.action-logout').on('click', function(event) {
    localStorage.removeItem('username');
    localStorage.removeItem('password');
    localStorage.removeItem('isadmin');
    $(window.location).attr('href', 'login.html');
    event.preventDefault()
});

/**********************************************************************
 * Roles
 *********************************************************************/

$('.action-roles').on('click', function(event) {
    roleTable.clear().draw();
	$.when(getUrl('/api/v1/roles')).done(function(data) {
        $.each(data.data, function(key, value) {
            insertRoleTable(value);
        });
        $('#modal-roles').modal('toggle');
    }).fail(function(data) {
        notifyUser('error', data.message);
    });
    event.preventDefault()
});

$('.action-role-add').on('click', function(event) {
    $('#modal-role-add').modal('toggle');
    event.preventDefault()
});

$('#form-role').on('submit', function(event) {
	form_data = formToJSON($(this));
	$.when(postUrl('/api/v1/roles', form_data)).done(function(data) {
        $(this).parents('form').find("input,textarea").val('');
        $('#modal-role-add').modal('toggle');
        insertRoleTable(value);
    }).fail(function(data) {
        notifyUser('error', data.message);
    });
    event.preventDefault()
});

/**********************************************************************
 * Users
 *********************************************************************/

$('.action-users').on('click', function(event) {
    $('#table-users tbody').empty();
	$.when(getUrl('/api/v1/users')).done(function(data) {
        $.each(data.data, function(key, value) {
            $('#table-users tbody').append('<tr data-url="/api/v1/users/' + value.username + '"><td>' + value.username + '</td><td data-editable data-name="password" data-type="password">**********</td><td data-editable data-name="name" data-type="text">' + value.name + '</td><td data-editable data-name="email" data-type="email">' + value.email + '</td><td data-editable data-name="labels" data-type="text">' + value.labels + '</td></tr>');
        });
        $('#modal-users').modal('toggle');
    }).fail(function(data) {
        notifyUser('error', data.message);
    });
    event.preventDefault()
});

$('.action-user-add').on('click', function(event) {
    $('#modal-user-add').modal('toggle');
    event.preventDefault()
});

$('#form-user').on('submit', function(event) {
	form_data = formToJSON($(this));
	$.when(postUrl('/api/v1/users', form_data)).done(function(data) {
        $(this).parents('form').find("input,textarea").val('');
        $('#modal-user-add').modal('toggle');
        $('#table-users tbody').prepend('<tr data-url="/api/v1/users/' + form_data.username + '"><td>' + form_data.username + '</td><td data-editable data-name="password" data-type="password">**********</td><td data-editable data-name="name" data-type="text">' + form_data.name + '</td><td data-editable data-name="email" data-type="email">' + value.email + '</td><td data-editable data-name="labels" data-type="text">' + form_data.labels + '</td></tr>');
    }).fail(function(data) {
        notifyUser('error', data.message);
    });
    event.preventDefault()
});

