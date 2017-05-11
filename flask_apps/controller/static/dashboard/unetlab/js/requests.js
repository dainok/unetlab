var DEMO = false;
var TIMEOUT = 3000

// GET /api/v1/auth
function getAuth(username, password) {
	var deferred = $.Deferred();
	if (DEMO) {
		if (username == 'admin' && password == 'admin') {
			deferred.resolve($.parseJSON('{"data": {"active_labs": {"7a6b5032-1430-4c58-8914-345e592d60fe": {"author": "Demo Author","id":"7a6b5032-1430-4c58-8914-345e592d60fe","name": "Demo Lab","repository": "local","version": 1}},"email":"admin@example.com","labels": -1,"name": "Default Administrator","roles": ["admin"],"username": "admin"},"message": "User authenticated","status": "success"}'))
		} else {
			deferred.reject({
				status: 'unauthorized',
				code: '401',
				message: 'The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.'
			});
		}
	} else {
		$.ajax({
			contentType: "application/json",
			dataType: 'json',
			timeout: TIMEOUT,
			type: 'GET',
			url: '/api/v1/auth',
            headers: {'Authorization': 'Basic ' + btoa(username + ':' + password)}
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
