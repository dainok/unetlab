// Close Form
$('body').on('hidden.bs.modal', '#form_frame > .modal', function(e) {
    $('#form_frame').empty();
});

// Add picture MAP
$('body').on('click', '#lab_picture', function(e) {
    var offset = $(this).offset();
    var y = (e.pageY - offset.top).toFixed(0);
    var x = (e.pageX - offset.left).toFixed(0);
    $('form :input[name="picture[map]"]').append("&lt;area shape='circle' coords='" + x + "," + y + ",30' href='telnet://{{IP}}:{{NODE1}}'&gt;\n");
});

// Start all nodes
$('.node_start_all').click(function() {
    lab_file = getParameter('filename');
    startLabNodes(lab_file, 'all');
});

// Stop all nodes
$('.node_stop_all').click(function() {
    lab_file = getParameter('filename');
    stopLabNodes(lab_file, 'all');
});

// Wipe all nodes
$('.node_wipe_all').click(function() {
    lab_file = getParameter('filename');
    wipeLabNodes(lab_file, 'all');
});

// Wipe all nodes
$('.node_export_all').click(function() {
    lab_file = getParameter('filename');
    exportLabNodes(lab_file, 'all');
});

// Add a network
$('.node_add').click(function() {
    lab_file = getParameter('filename');
    displayNodeForm(lab_file, null);
});

// Display network form
$('.network_add').click(function() {
    lab_file = getParameter('filename');
    displayNetworkForm(lab_file, null);
});

// Display picture form
$('.picture_add').click(function() {
    lab_file = getParameter('filename');
    displayPictureForm(lab_file, null);
});

// Display lab_add form
$('.lab_add').click(function() {
    path = getParameter('path');
    displayLabAddForm(path);
});

// Display folder_add form
$('.folder_add').click(function() {
    path = getParameter('path');
    displayFolderAddForm(path);
});

// Add folder form
$('body').on('submit', '#form-folder_add', function(e) {
    var form_data = {};

    // Setting options
    $('form :input[name^="folder["]').each(function(id, object) {
        form_data[$(this).attr('name').substr(7, $(this).attr('name').length - 8)] = $(this).val();
    });

    // Get action URL
    var url = '/api/folders';
    $.ajax({
        timeout: TIMEOUT,
        type: 'POST',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                raiseMessage('SUCCESS', 'Folder added.');
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Reopen the page
    window.location.href = '/lab_list.php' + window.location.search;

    // Stop or form will follow the action link
    return false;
});

// Add lab form
$('body').on('submit', '#form-lab_add', function(e) {
    var form_data = {};

    // Setting options
    $('form :input[name^="lab["]').each(function(id, object) {
        form_data[$(this).attr('name').substr(4, $(this).attr('name').length - 5)] = $(this).val();
    });

    // Get action URL
    var url = '/api/labs';
    $.ajax({
        timeout: TIMEOUT,
        type: 'POST',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                raiseMessage('SUCCESS', 'Folder added.');

                // Go to lab_edit page
                if (form_data['path'] == '/') {
                    var lab_file = '/' + form_data['name'] + '.unl';
                } else {
                    var lab_file = form_data['path'] + '/' + form_data['name'] + '.unl';
                }
                window.location.href = '/lab_edit.php?filename=' + lab_file;
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Edit lab form
$('body').on('submit', '#form-lab_edit', function(e) {
    lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    $('form :input[name^="lab["]').each(function(id, object) {
        form_data[$(this).attr('name').substr(4, $(this).attr('name').length - 5)] = $(this).val();
    });

    // Get action URL
    var url = '/api/labs' + lab_file;
    $.ajax({
        timeout: TIMEOUT,
        type: 'PUT',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                raiseMessage('SUCCESS', 'Lab saved.');
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Stop or form will follow the action link
    return false;
});

// Add network(s) form
$('body').on('submit', '#form-network_add', function(e) {
    lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    $('form :input[name^="network["]').each(function(id, object) {
        form_data[$(this).attr('name').substr(8, $(this).attr('name').length - 9)] = $(this).val();
    });
    form_data['postfix'] = 0;
    if (form_data['count'] > 1) {
        form_data['postfix'] = 1;
    }

    // Get action URL
    var url = '/api/labs' + lab_file + '/networks';
    for (var i = 0; i < form_data['count']; i++) {
        $.ajax({
            timeout: TIMEOUT,
            type: 'POST',
            url: encodeURI(url),
            dataType: 'json',
            data: JSON.stringify(form_data),
            success: function(data) {
                if (data['status'] == 'success') {
                    raiseMessage('SUCCESS', 'Network "' + form_data['name'] + '" added.');
                    // Folder added -> reopen this page (not reload, or will be posted twice)
                    window.location.href = '/lab_edit.php' + window.location.search;
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', data['status']);
                }
            },
            error: function(data) {
                raiseMessage('DANGER', getJsonMessage(data['responseText']));
            }
        });
    }

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Edit network form
$('body').on('submit', '#form-network_edit', function(e) {
    lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    $('form :input[name^="network["]').each(function(id, object) {
        if ($(this).attr('name').match(/^network\[[a-z]+\]$/)) {
            // Standard options
            var field_name = $(this).attr('name').replace(/^network\[([a-z]+)\]$/, '$1');
            form_data[field_name] = $(this).val();
        }
    });

    // Get action URL
    var url = '/api/labs' + lab_file + '/networks/' + form_data['id'];
    $.ajax({
        timeout: TIMEOUT,
        type: 'PUT',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Network "' + form_data['name'] + '" saved.');
                // Network saved  -> reopen this page (not reload, or will be posted twice)
                window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Attach files
var attachments;
$('body').on('change', 'input[type=file]', function(e) {
    attachments = e.target.files;
});

// Add picture form
$('body').on('submit', '#form-picture_add', function(e) {
    lab_file = getParameter('filename');
    var form_data = new FormData();

    // Setting options
    $('form :input[name^="picture["]').each(function(id, object) {
        form_data.append($(this).attr('name').substr(8, $(this).attr('name').length - 9), $(this).val());
    });

    // Add attachments
    $.each(attachments, function(key, value) {
        form_data.append(key, value);
    });

    // Get action URL
    var url = '/api/labs' + lab_file + '/pictures';
    $.ajax({
        timeout: TIMEOUT,
        type: 'POST',
        url: encodeURI(url),
        contentType: false, // Set content type to false as jQuery will tell the server its a query string request
        processData: false, // Don't process the files
        dataType: 'json',
        data: form_data,
        success: function(data) {
            if (data['status'] == 'success') {
                raiseMessage('SUCCESS', 'Picture "' + form_data['name'] + '" added.');
                // Picture added -> reopen this page (not reload, or will be posted twice)
                window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Edit picture form
$('body').on('submit', '#form-picture_edit', function(e) {
    lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    $('form :input[name^="picture["]').each(function(id, object) {
        // Standard options
        var field_name = $(this).attr('name').replace(/^picture\[([a-z]+)\]$/, '$1');
        form_data[field_name] = $(this).val();
    });

    // Get action URL
    var url = '/api/labs' + lab_file + '/pictures/' + form_data['id'];
    $.ajax({
        timeout: TIMEOUT,
        type: 'PUT',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Picture "' + form_data['name'] + '" saved.');
                // Picture saved  -> reopen this page (not reload, or will be posted twice)
                window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Select node template
$('body').on('change', '#form-node_template', function(e) {
    var deferred = $.Deferred();
    var node_template = $(this).find("option:selected").val();

    if (node_template != '') {
        // Getting template only if a valid option is selected (to avoid requests during typewriting)
        $.when(displayNodeFormFromTemplate(node_template, false)).done(function(form_template) {
            // Add the form to the HTML page
            $('#form-node_add').html(form_template);

            // Validate values and set autofocus
            $('.selectpicker').selectpicker();
            validateLabNode();

            deferred.resolve();
        }).fail(function() {
            deferred.reject();
        });
    }
});

// Add node form
$('body').on('submit', '#form-node_add', function(e) {
    var lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    $('form :input[name^="node["]').each(function(id, object) {
        var field_name = $(this).attr('name').replace(/^node\[([a-z0-9]+)\]$/, '$1');
        form_data[field_name] = $(this).val();
    });
    form_data['postfix'] = 0;
    if (form_data['count'] > 1) {
        form_data['postfix'] = 1;
    }

    // Get action URL
    var url = '/api/labs' + lab_file + '/nodes';
    for (var i = 0; i < form_data['count']; i++) {
        $.ajax({
            timeout: TIMEOUT,
            type: 'POST',
            url: encodeURI(url),
            dataType: 'json',
            data: JSON.stringify(form_data),
            success: function(data) {
                if (data['status'] == 'success') {
                    // Fetching ok
                    raiseMessage('SUCCESS', 'Node "' + form_data['name'] + '" added.');
                    // Node saved  -> reopen this page (not reload, or will be posted twice)
                    window.location.href = '/lab_edit.php' + window.location.search;
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', data['status']);
                }
            },
            error: function(data) {
                raiseMessage('DANGER', getJsonMessage(data['responseText']));
            }
        });
    }

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Edit node form
$('body').on('submit', '#form-node_edit', function(e) {
    lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    $('form :input[name^="node["]').each(function(id, object) {
        var field_name = $(this).attr('name').replace(/^node\[([a-z0-9]+)\]$/, '$1');
        form_data[field_name] = $(this).val();
    });

    // Get action URL
    var url = '/api/labs' + lab_file + '/nodes/' + form_data['id'];
    $.ajax({
        timeout: TIMEOUT,
        type: 'PUT',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Node "' + form_data['name'] + '" saved.');
                // Network saved  -> reopen this page (not reload, or will be posted twice)
                window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Display picture
$('body').on('click', '.picture_frame', function(e) {
    lab_file = getParameter('filename');
    picture_id = $(this).attr('data-id');
    displayPictureForm(lab_file, picture_id);
});

// Save node position (on lab_edit page only)
if ($(location).attr('pathname') == '/lab_edit.php') {
    $('body').on('mouseup', '.node_frame, .network_frame', function(e) {
        if (e.which != 1) {
            // This is a right click
            return false;
        }

        // Read position
        var offset = $(this).offset();
        var form_data = {}
        form_data['left'] = (100 * (offset.left / $(window).width())).toFixed(0) + '%';
        form_data['top'] = (100 * (offset.top / $(window).height())).toFixed(0) + '%';

        if ($(this).hasClass('node_frame')) {
            form_data['id'] = $(this).attr('id').substr(4);

            // Get action URL
            var url = '/api/labs' + lab_file + '/nodes/' + form_data['id'];
            $.ajax({
                timeout: TIMEOUT,
                type: 'PUT',
                url: encodeURI(url),
                dataType: 'json',
                data: JSON.stringify(form_data),
                success: function(data) {
                    if (data['status'] == 'success') {
                        // Fetching ok
                        jsPlumb.repaintEverything();
                    } else {
                        // Fetching failed
                        raiseMessage('DANGER', data['status']);
                    }
                },
                error: function() {
                    raiseMessage('DANGER', getJsonMessage(data['responseText']));
                }
            });
        } else if ($(this).hasClass('network_frame')) {
            form_data['id'] = $(this).attr('id').substr(7);

            // Get action URL
            var url = '/api/labs' + lab_file + '/networks/' + form_data['id'];
            $.ajax({
                timeout: TIMEOUT,
                type: 'PUT',
                url: encodeURI(url),
                dataType: 'json',
                data: JSON.stringify(form_data),
                success: function(data) {
                    if (data['status'] == 'success') {
                        // Fetching ok
                        jsPlumb.repaintEverything();
                    } else {
                        // Fetching failed
                        raiseMessage('DANGER', data['status']);
                    }
                },
                error: function() {
                    raiseMessage('DANGER', getJsonMessage(data['responseText']));
                }
            });
        } else {
            // Should not be here
            raiseMessage('DANGER', 'Invalid object type.');
        }
    });
}

// Edit lab node interface links
$('body').on('submit', '#form-node_connect', function(e) {
    lab_file = getParameter('filename');
    var form_data = {};

    // Setting options
    var node_id = $('form :input[name="node_id"]').val();
    $('form :input[name^="interfc["]').each(function(id, object) {
        var field_name = $(this).attr('name').replace(/^interfc\[([0-9]+)\]$/, '$1');
        form_data[field_name] = $(this).val();
    });

    // Get action URL
    var url = '/api/labs' + lab_file + '/nodes/' + node_id + '/interfaces';
    $.ajax({
        timeout: TIMEOUT,
        type: 'PUT',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Node "' + form_data['name'] + '" saved.');
                // Network saved  -> reopen this page (not reload, or will be posted twice)
                window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                raiseMessage('DANGER', data['status']);
            }
        },
        error: function(data) {
            raiseMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Logout button
$(document).on('click', '#button-logout', function(e) {
    e.preventDefault();  // Prevent default behaviour
    var url = '/api/auth/logout';
    var type = 'GET'
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
				window.location = '/themes/default/auth.html';
            } else {
                // Authentication error
				window.location = '/themes/default/auth.html';
            }
        },
        error: function(data) {
            // Authentication error
			window.location = '/themes/default/auth.html';
        }
    });
    return false;
});

