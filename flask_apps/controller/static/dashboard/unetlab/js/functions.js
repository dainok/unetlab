// Convert form data into JSON 
function formToJSON($form) {
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};
	$.map(unindexed_array, function(n, i){
		indexed_array[n['name']] = n['value'];
	});
	return indexed_array;
}

// Check if a user is authenticated
function isAuthenticated() {
	username = localStorage.getItem('username');
	password = localStorage.getItem('password');
	if (username !== null && password !== null) {
		$.when(getAuth(username, password)).done(function(data) {
			return true;
		}).fail(function(data) {
			return true;
		});
	} else {
		return false;
	}
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