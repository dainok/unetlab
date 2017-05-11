$('#form-login').on('submit', function (event) {
	form_data = formToJSON($(this));
	$.when(getAuth(form_data['username'], form_data['password'])).done(function(data) {
		localStorage.setItem('username', form_data['username']);
		localStorage.setItem('password', form_data['password']);
		notifyUser('info', data['message']);
		$(window.location).attr('href', 'home.html');
	}).fail(function(data) {
		$('#form-login, input').val('');
		notifyUser('error', data['message']);
	});
	event.preventDefault()
});
