/* UNetLabv2 UI - actions
 * ================
 * @author    Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright Andrea Dainese <andrea.dainese@gmail.com>
 * @license   https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
 * @revision  2.3.8
 */

$('#form-login').on('submit', function(event) {
	form_data = formToJSON($(this));
	$.when(getAuth(form_data['username'], form_data['password'])).done(function(data) {
		localStorage.setItem('username', form_data['username']);
		localStorage.setItem('password', form_data['password']);
		$(window.location).attr('href', 'home.html');
	}).fail(function(data) {
		$('#form-login, input').val('');
		notifyUser('error', data['message']);
	});
	event.preventDefault()
});

$('#form-profile').on('submit', function(event) {
	form_data = formToJSON($(this));
	$.when(patchAuth(form_data)).done(function(data) {
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
		notifyUser('error', data['message']);
	});
	event.preventDefault()
});

$('.action-logout').on('click', function(event) {
    localStorage.removeItem('username');
    localStorage.removeItem('password');
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
    console.log('here');
    $('#modal-users').modal('toggle');
    event.preventDefault()
});

