/* UNetLabv2 UI - actions
 * ================
 * @author    Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright Andrea Dainese <andrea.dainese@gmail.com>
 * @license   https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
 * @revision  2.3.8
 */

$('body').on('click', '[data-editable]', function() {
    var $element = $(this);
    var table = $element.parents('table').attr('data-table');
    var id = $element.parents('tr').attr('data-id');
    var name = $element.attr('data-name');
    var type = $element.attr('data-type');
    if (type == 'password') {
        var value = '';
    } else {
        var value = $element.text();
    }
    var $input = $('<input/>').val(value);
    $input.attr('name', name);
    $input.attr('type', type);
    $element.empty()
    $element.append($input);

    var save = function(){
        data = {};
        if (type == 'password' && $input.val() == '') {
            $element.text('**********');
        } else {
            data[name] = $input.val();
            console.log('PATCH');
            console.log('/api/v1/' + table + '/' + id);
            console.log(data);
            $element.text($input.val());
        }
    };

    $input.one('blur', save).focus();
    $input.keydown( function(event) {
        var key = event.charCode ? event.charCode : event.keyCode ? event.keyCode : 0;
        if(key == 13) {
            event.preventDefault();
            save();
        }
    });
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

$('.action-repositories').on('click', function(event) {
    $('#modal-repositories').modal('toggle');
    event.preventDefault()
});

$('.action-roles').on('click', function(event) {
    $('#modal-roles').modal('toggle');
    event.preventDefault()
});

$('.action-users').on('click', function(event) {
    $('#table-users tbody').empty();
	$.when(getUrl('/api/v1/users')).done(function(data) {
        $.each(data.data, function(key, value) {
            $('#table-users tbody').append('<tr data-id=' + value.username + ' data-type="text"><td>' + value.username + '</td><td data-editable data-name="password" data-type="password">**********</td><td data-editable data-name="name" data-type="text">' + value.name + '</td><td data-editable data-name="email" data-type="email">' + value.email + '</td><td data-editable data-name="labels" data-type="text">' + value.labels + '</td></tr>');
        });
        $('#modal-users').modal('toggle');
    }).fail(function(data) {
        notifyUser('error', data.message);
    });
    event.preventDefault()
});

