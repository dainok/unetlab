// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/functions.js
 *
 * Functions
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */



// Basename: given /a/b/c return c
function basename(path) {
    return path.replace(/\\/g, '/').replace(/.*\//, '');
}

// Dirname: given /a/b/c return /a/b
function dirname(path) {
    var dir = path.replace(/\\/g, '/').replace(/\/[^\/]*$/, '');
    if (dir == '') {
        return '/';
    } else {
        return dir;
    }
}

// Alert management
function addMessage(severity, message, notFromLabviewport) {
    // Severity can be success (green), info (blue), warning (yellow) and danger (red)
    // Param 'notFromLabviewport' is used to filter notification

    var timeout = 10000;        // by default close messages after 10 seconds
    if (severity == 'danger') timeout = 5000;
    if (severity == 'alert') timeout = 10000;
    if (severity == 'warning') timeout = 10000;

    // Add notifications to #alert_container only when labview is open
    if ($("#lab-viewport").length) {
        if (!$('#alert_container').length) {
            // Add the frame container if not exists
            $('body').append('<div id="alert_container"><b><i class="fa fa-bell-o"></i> Notifications</b><div class="inner"></div></div>');
        }
        var msgalert = $('<div class="alert alert-' + severity.toLowerCase() + ' fade in">').append($('<button type="button" class="close" data-dismiss="alert">').append("&times;")).append(message);

        // Add the alert div to top (prepend()) or to bottom (append())
        $('#alert_container .inner').prepend(msgalert);

    }

    if ($("#lab-viewport").length || (!$("#lab-viewport").length && notFromLabviewport)) {
        if (!$('#notification_container').length) {
            $('body').append('<div id="notification_container"></div>');
        }

        //if (severity == "danger" )
        if (severity != "") {
            var notification_alert = $('<div class="alert alert-' + severity.toLowerCase() + ' fade in">').append($('<button type="button" class="close" data-dismiss="alert">').append("&times;")).append(message);

            $('#notification_container').prepend(notification_alert);
            if (timeout) {
                window.setTimeout(function () {
                    notification_alert.alert("close");
                }, timeout);
            }
        }
    }
}

// Add Modal
function addModal(title, body, footer, prop) {
    var html = '<div aria-hidden="false" style="display: block;z-index: 10000;" class="modal ' + ' ' + prop + ' fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">' + body + '</div><div class="modal-footer">' + footer + '</div></div></div></div>';
    $('body').append(html);
    $('body > .modal').modal('show');
}

// Add Modal
function addModalError(message) {
    var html = '<div aria-hidden="false" style="display: block;" class="modal fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button><h4 class="modal-title">' + MESSAGES[15] + '</h4></div><div class="modal-body">' + message + '</div><div class="modal-footer"></div></div></div></div>';
    $('body').append(html);
    $('body > .modal').modal('show');
}

// Add Modal
function addModalWide(title, body, footer, property) {
    var prop = property || "";
    console.log("### title is", title);
    var addittionalHeaderBtns = "";
    if (title.toUpperCase() == "STARTUP-CONFIGS" || title.toUpperCase() == "CONFIGURED NODES" || 
        title.toUpperCase() == "CONFIGURED TEXT OBJECTS" || 
        title.toUpperCase() == "CONFIGURED NETWORKS" || title.toUpperCase() == "CONFIGURED NODES" ||
        title.toUpperCase() == "STATUS" || title.toUpperCase() == "PICTURES") {
        addittionalHeaderBtns = '<i title="Make transparent" class="glyphicon glyphicon-certificate pull-right action-changeopacity"></i>'
    }
    var html = '<div aria-hidden="false" style="display: block;" class="modal modal-wide ' + prop + ' fade in" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"></i><button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' + addittionalHeaderBtns + '<h4 class="modal-title">' + title + '</h4></div><div class="modal-body">' + body + '</div><div class="modal-footer">' + footer + '</div></div></div></div>';
    $('body').append(html);
    $('body > .modal').modal('show');
}

// Export node(s) config
function cfg_export(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/export';
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT * 10,  // Takes a lot of time
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: config exported.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// // Export node(s) config recursive
function recursive_cfg_export(nodes, i) {
    i = i - 1
    addMessage('info', nodes[Object.keys(nodes)[i]]['name'] + ': ' + MESSAGES[138])
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    if (typeof nodes[Object.keys(nodes)[i]]['path'] === 'undefined') {
        var url = '/api/labs' + lab_filename + '/nodes/' + Object.keys(nodes)[i] + '/export';
    } else {
        var url = '/api/labs' + lab_filename + '/nodes/' + nodes[Object.keys(nodes)[i]]['path'] + '/export';
    }
    logger(1, 'DEBUG: ' + url);
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT * 10 * i,  // Takes a lot of time
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: config exported.');
                addMessage('success', nodes[Object.keys(nodes)[i]]['name'] + ': ' + MESSAGES[79])
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                addMessage('danger', nodes[Object.keys(nodes)[i]]['name'] + ': ' + data['message']);
            }
            if (i > 0) {
                recursive_cfg_export(nodes, i);
            } else {
                addMessage('info', 'Export All: done');
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            addMessage('danger', nodes[Object.keys(nodes)[i]]['name'] + ': ' + message);
            if (i > 0) {
                recursive_cfg_export(nodes, i);
            } else {
                addMessage('info', 'Export All: done');
            }
        }
    });
    return deferred.promise();
}

// Clone selected labs
function cloneLab(form_data) {
    var deferred = $.Deferred();
    var type = 'POST';
    var url = '/api/labs';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: created lab "' + form_data['name'] + '" from "' + form_data['source'] + '".');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Close lab
function closeLab() {
    var deferred = $.Deferred();
    $.when(getNodes()).done(function (values) {
        var running_nodes = false;
        $.each(values, function (node_id, node) {
            if (node['status'] > 1) {
                running_nodes = true;
            }
        });

        if (running_nodes == false) {
            var url = '/api/labs/close';
            var type = 'DELETE';
            $.ajax({
                timeout: TIMEOUT,
                type: type,
                url: encodeURI(url),
                dataType: 'json',
                success: function (data) {
                    if (data['status'] == 'success') {
                        logger(1, 'DEBUG: lab closed.');
                        LAB = null;
                        deferred.resolve();
                    } else {
                        // Application error
                        logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                        deferred.reject(data['message']);
                    }
                },
                error: function (data) {
                    // Server error
                    var message = getJsonMessage(data['responseText']);
                    logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
                    logger(1, 'DEBUG: ' + message);
                    deferred.reject(message);
                }
            });
        } else {
            deferred.reject(MESSAGES[131]);
        }
    }).fail(function (message) {
        // Lab maybe does not exist, closing
        var url = '/api/labs/close';
        var type = 'DELETE';
        $.ajax({
            timeout: TIMEOUT,
            type: type,
            url: encodeURI(url),
            dataType: 'json',
            success: function (data) {
                if (data['status'] == 'success') {
                    logger(1, 'DEBUG: lab closed.');
                    LAB = null;
                    deferred.resolve();
                } else {
                    // Application error
                    logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                    deferred.reject(data['message']);
                }
            },
            error: function (data) {
                // Server error
                var message = getJsonMessage(data['responseText']);
                logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
                logger(1, 'DEBUG: ' + message);
                deferred.reject(message);
            }
        });
    });
    return deferred.promise();
}

// Delete folder
function deleteFolder(path) {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var url = '/api/folders' + path;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: folder "' + path + '" deleted.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Delete lab
function deleteLab(path) {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var url = '/api/labs' + path;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: lab "' + path + '" deleted.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Delete network
function deleteNetwork(id) {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/networks/' + id;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: network deleted.');
                deferred.resolve(data);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Delete node
function deleteNode(id) {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/nodes/' + id;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node deleted.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Delete user
function deleteUser(path) {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var url = '/api/users/' + path;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: user "' + path + '" deleted.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Export selected folders and labs
function exportObjects(form_data) {
    var deferred = $.Deferred();
    var type = 'POST';
    var url = '/api/export';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: objects exported into "' + data['data'] + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// HTML Form to array
function form2Array(form_name) {
    var form_array = {};
    $('form :input[name^="' + form_name + '["]').each(function (id, object) {
        // INPUT name is in the form of "form_name[value]", get value only
        form_array[$(this).attr('name').substr(form_name.length + 1, $(this).attr('name').length - form_name.length - 2)] = $(this).val();
    });
    return form_array;
}

// HTML Form to array by row
function form2ArrayByRow(form_name, id) {
    var form_array = {};
    
    $('form :input[name^="' + form_name + '["][data-path="' + id +'"]').each(function (id, object) {
        // INPUT name is in the form of "form_name[value]", get value only
        form_array[$(this).attr('name').substr(form_name.length + 1, $(this).attr('name').length - form_name.length - 2)] = $(this).val();
    });
    return form_array;
}

// Get JSon message from HTTP response
function getJsonMessage(response) {
    var message = '';
    try {
        message = JSON.parse(response)['message'];
        code = JSON.parse(response)['code'];
        if (code == 412) {
            // if 412 should redirect (user timed out)
            window.setTimeout(function () {
                location.reload();
            }, 2000);
        }
    } catch (e) {
        if (response != '') {
            message = response;
        } else {
            message = 'Undefined message, check if the UNetLab VM is powered on. If it is, see <a href="/Logs" target="_blank">logs</a>.';
        }
    }
    return message;
}

// Get lab info
function getLabInfo(lab_filename) {
    var deferred = $.Deferred();
    var url = '/api/labs' + lab_filename;
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: lab "' + lab_filename + '" found.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get lab body
function getLabBody() {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/html';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: lab "' + lab_filename + '" body found.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get lab endpoints
function getLabLinks() {
    var lab_filename = $('#lab-viewport').attr('data-path');
    var deferred = $.Deferred();
    var url = '/api/labs' + lab_filename + '/links';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got available links(s) from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}


// Get lab networks
function getNetworks(network_id) {
    var lab_filename = $('#lab-viewport').attr('data-path');
    var deferred = $.Deferred();
    if (network_id != null) {
        var url = '/api/labs' + lab_filename + '/networks/' + network_id;
    } else {
        var url = '/api/labs' + lab_filename + '/networks';
    }
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got network(s) from lab "' + lab_filename + '".');

                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

//remove network with type=bridge with 1 node connected on refresh
function deleteSingleNetworks() {
    var deferred = $.Deferred();
    var networksArr=[];

     $.when(getNetworks())
        .then(function (networks) {
            var deleted = [];
            networksArr = networks;

            $.each(networksArr, function (key, value) {
                if (value.count == 1 && value.type == 'bridge'){
                    deleted.push(deleteNetwork(value.id))
                    delete networksArr[key];
                    $('.network' + value.id).remove();
                }
            });

              return $.when.apply(this, deleted)
        }).done(function(){

         deferred.resolve(networksArr);
     }).fail(function (message) {
         deferred.reject(message);
     });

    return deferred.promise();
}

// Get available network types
function getNetworkTypes() {
    var deferred = $.Deferred();
    var url = '/api/list/networks';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got network types.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get lab nodes
function getNodes(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    if (node_id != null) {
        var url = '/api/labs' + lab_filename + '/nodes/' + node_id;
    } else {
        var url = '/api/labs' + lab_filename + '/nodes';
    }
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got node(s) from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get node startup-config
function getNodeConfigs(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    if (node_id != null) {
        var url = '/api/labs' + lab_filename + '/configs/' + node_id;
    } else {
        var url = '/api/labs' + lab_filename + '/configs';
    }
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got sartup-config(s) from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get lab node interfaces
function getNodeInterfaces(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/interfaces';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got node(s) from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get lab pictures
function getPictures(picture_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    if (picture_id != null) {
        var url = '/api/labs' + lab_filename + '/pictures/' + picture_id;
    } else {
        var url = '/api/labs' + lab_filename + '/pictures';
    }
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got pictures(s) from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get lab topology
function getTopology() {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/topology';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got topology from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get roles
function getRoles() {
    var deferred = $.Deferred();
    var form_data = {};
    var url = '/api/list/roles';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got roles.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get system stats
function getSystemStats() {
    var deferred = $.Deferred();
    var url = '/api/status';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: system stats.');
                data['data']['cpu'] = data['data']['cpu'] / 100;
                data['data']['disk'] = data['data']['disk'] / 100;
                data['data']['mem'] = data['data']['mem'] / 100;
                data['data']['cached'] = data['data']['cached'] / 100;
                data['data']['swap'] = data['data']['swap'] / 100;
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get templates
function getTemplates(template) {
    var deferred = $.Deferred();
    var url = (template == null) ? '/api/list/templates/' : '/api/list/templates/' + template;
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got template(s).');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get user info
function getUserInfo() {
    var deferred = $.Deferred();
    var url = '/api/auth';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        beforeSend: function (jqXHR) {
            if (window.BASE_URL) {
                jqXHR.crossDomain = true;
            }
        },
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: user is authenticated.');
                EMAIL = data['data']['email'];
                FOLDER = (data['data']['folder'] == null) ? '/' : data['data']['folder'];
                LAB = data['data']['lab'];
                LANG = data['data']['lang'];
                NAME = data['data']['name'];
                ROLE = data['data']['role'];
                TENANT = data['data']['tenant'];
                USERNAME = data['data']['username'];
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get users
function getUsers(user) {
    var deferred = $.Deferred();
    if (user != null) {
        var url = '/api/users/' + user;
    } else {
        var url = '/api/users/';
    }
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got user(s).');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Logging
function logger(severity, message) {
    if (DEBUG >= severity) {
        console.log(message);
    }
}

// Logout user
function logoutUser() {
    var deferred = $.Deferred();
    var url = '/api/auth/logout';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: user is logged off.');
                if (UPDATEID != null) {
                    // Stop updating node_status
                    clearInterval(UPDATEID);
                }
                deferred.resolve();
            } else {
                // Authentication error
                logger(1, 'DEBUG: internal error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Authentication error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: Ajax error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Move folder inside a folder
function moveFolder(folder, path) {
    var deferred = $.Deferred();
    var type = 'PUT';
    var url = '/api/folders' + folder;
    var form_data = {};
    form_data['path'] = (path == '/') ? '/' + basename(folder) : path + '/' + basename(folder);
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: folder is moved.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Move lab inside a folder
function moveLab(lab, path) {
    var deferred = $.Deferred();
    var type = 'PUT';
    var url = '/api/labs' + lab + '/move';
    var form_data = {};
    form_data['path'] = path;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: lab is moved.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Delete picture
function deletePicture(lab_file, picture_id, cb) {
    var deferred = $.Deferred();
    var data = [];

    // Delete network
    var url = '/api/labs' + lab_file + '/pictures/' + picture_id;
    $.ajax({
        timeout: TIMEOUT,
        type: 'DELETE',
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                // Fetching ok
                $('.picture' + picture_id).fadeOut(300, function () {
                    $(this).remove();
                });
                deferred.resolve(data);
            } else {
                // Fetching failed
                addMessage('DANGER', data['status']);
                deferred.reject(data['status']);
            }
        },
        error: function (data) {
            addMessage('DANGER', getJsonMessage(data['responseText']));
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Post login
function postLogin(param) {
    if (UPDATEID != null) {
        // Stop updating node_status
        clearInterval(UPDATEID);
    }

    if (LAB == null && param == null) {
        logger(1, 'DEBUG: loading folder "' + FOLDER + '".');
        printPageLabList(FOLDER);
    } else {
        LAB = LAB || param;
        logger(1, 'DEBUG: loading lab "' + LAB + '".');


        printPageLabOpen(LAB);

        // Update node status
        UPDATEID = setInterval('printLabStatus("' + LAB + '")', STATUSINTERVAL);


    }


}

//set Network

function setNetwork(nodeName,left, top) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = {};

    form_data['count'] = 1;
    form_data['name'] = 'Net-'+nodeName;
    form_data['type'] = 'bridge';
    form_data['left'] = left;
    form_data['top'] = top;
    form_data['postfix'] = 0;

    var url = '/api/labs' + lab_filename + '/networks';
    var type = 'POST';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: new network created.');
                deferred.resolve(data);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
            addMessage(data['status'], data['message']);

        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Set network position
function setNetworkPosition(network_id, left, top) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = {};
    form_data['left'] = left;
    form_data['top'] = top;
    var url = '/api/labs' + lab_filename + '/networks/' + network_id;
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: network position updated.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
            addMessage(data['status'], data['message']);

        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Set node boot
function setNodeBoot(node_id, config) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = {};
    form_data['config'] = config;
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id;
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node bootflag updated.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}
// Set node position
function setNodePosition(node_id, left, top) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = {};
    form_data['left'] = left;
    form_data['top'] = top;
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id;
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node position updated.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}
// Update node data from node list
function setNodeData(id){
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = form2ArrayByRow('node', id);
    var promises = [];
    logger(1, 'DEBUG: posting form-node-edit form.');
    var url = '/api/labs' + lab_filename + '/nodes/' + id;
    var type = 'PUT';
    form_data['id'] = id;
    form_data['count'] = 1;
    form_data['postfix'] = 0;
    for (var i = 0; i < form_data['count']; i++) {
        form_data['left'] = parseInt(form_data['left']) + i * 10;
        form_data['top'] = parseInt(form_data['top']) + i * 10;
        var request = $.ajax({
            timeout: TIMEOUT,
            type: type,
            url: encodeURI(url),
            dataType: 'json',
            data: JSON.stringify(form_data),
            success: function (data) {
                if (data['status'] == 'success') {
                    logger(1, 'DEBUG: node "' + form_data['name'] + '" saved.');
                    // Close the modal
                    $("#node" + id + " .node_name").html('<i class="node' + id + '_status glyphicon glyphicon-stop"></i>' + form_data['name'])
                    $("#node" + id + " a img").attr("src", "/images/icons/" + form_data['icon'])
                    addMessage(data['status'], data['message']);
                } else {
                    // Application error
                    logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                    addModal('ERROR', '<p>' + data['message'] + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
                }
            },
            error: function (data) {
                // Server error
                var message = getJsonMessage(data['responseText']);
                logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
                logger(1, 'DEBUG: ' + message);
                addModal('ERROR', '<p>' + message + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
            }
        });
        promises.push(request);
    }

    $.when.apply(null, promises).done(function () {
        logger(1,"data is sent");
    });
    return false;
}

//set note interface
function setNodeInterface(node_id,network_id,interface_id){

    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = {};
    form_data[interface_id] = network_id;

    var url = '/api/labs' + lab_filename + '/nodes/' + node_id +'/interfaces';
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node interface updated.');
                deferred.resolve(data);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();

}

// Start node(s)
function start(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/start';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node(s) started.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Start nodes recursive
function recursive_start(nodes, i) {
    i = i - 1;
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    if (typeof nodes[Object.keys(nodes)[i]]['path'] === 'undefined') {
        var url = '/api/labs' + lab_filename + '/nodes/' + Object.keys(nodes)[i] + '/start';
    } else {
        var url = '/api/labs' + lab_filename + '/nodes/' + nodes[Object.keys(nodes)[i]]['path'] + '/start';
    }
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node(s) started.');
                addMessage('success', nodes[Object.keys(nodes)[i]]['name'] + ': ' + MESSAGES[76]);
                
                //set start status
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                addMessage('danger', nodes[Object.keys(nodes)[i]]['name'] + ': ' + MESSAGES[76] + 'failed');
            }
            if (i > 0) {
                recursive_start(nodes, i);
            } else {
                addMessage('info', 'Start All: done');
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            addMessage('danger', message);
            if (i > 0) {
                recursive_start(nodes, i);
            } else {
                addMessage('info', 'Start All: done');
            }

        }
    });
    return deferred.promise();
}


// Stop node(s)
function stop(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/stop';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node(s) stopped.');
                deferred.resolve(data['data']);

            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Stop all nodes
function stopAll() {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var url = '/api/status';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: stopped all nodes.');
                deferred.resolve();

            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Update
function update(path) {
    var deferred = $.Deferred();
    var type = 'GET';
    var url = '/api/update';
    $.ajax({
        timeout: TIMEOUT * 10,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: system updated.');
                deferred.resolve(data['message']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        /*
         error: function(data) {
         // Server error
         var message = getJsonMessage(data['responseText']);
         logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
         logger(1, 'DEBUG: ' + message);
         deferred.reject(message);
         }
         */
    });
    return deferred.promise();
}

// Wipe node(s)
function wipe(node_id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/wipe';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node(s) wiped.');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

/***************************************************************************
 * Print forms and pages
 **************************************************************************/
// Context menu
function printContextMenu(title, body, pageX, pageY, addToBody) {
    var menu = '<div id="context-menu" class="collapse clearfix dropdown">';
    menu += '<ul class="dropdown-menu" role="menu"><li role="presentation" class="dropdown-header">' + title + '</li>' + body + '</ul></div>';

    if(addToBody){
        $('body').append(menu);
    } else {
        $('#lab-viewport').append(menu);
    }

    // Set initial status
    $('.menu-interface, .menu-edit').slideToggle();
    $('.menu-interface, .menu-edit').hide();

    // Calculating position
    if (pageX + $('#context-menu').width() > $(window).width()) {
        // Dropright
        var left = pageX - $('#context-menu').width();
    } else {
        // Dropleft
        var left = pageX;
    }
    if ($('#context-menu').height() > $(window).height()) {
        // Page is too short, drop down by default
        var top = 0;
        var max_height = $(window).height();
    } else if ($(window).height() - pageY >= $('#context-menu').height()) {
        // Dropdown if enough space
        var top = pageY;
        var max_height = $('#context-menu').height();
    } else {
        // Dropup
        var top = $(window).height() - $('#context-menu').height();
        var max_height = $('#context-menu').height();
    }

    // Setting position via CSS
    $('#context-menu').css({
        left: left - 30 + 'px',
        maxHeight: max_height,
        top: top + 'px'
    });
    $('#context-menu > ul').css({
        maxHeight: max_height - 5
    });
}

// Folder form
function printFormFolder(action, values) {
    var name = (values['name'] != null) ? values['name'] : '';
    var path = (values['path'] != null) ? values['path'] : '';
    var original = (path == '/') ? '/' + name : path + '/' + name;
    var submit = (action == 'add') ? MESSAGES[17] : MESSAGES[21];
    var title = (action == 'add') ? MESSAGES[4] : MESSAGES[10];
    if (original == '/' && action == 'rename') {
        addModalError(MESSAGES[51]);
    } else {
        var html = '<form id="form-folder-' + action + '" class="form-horizontal form-folder-' + action + '"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="folder[path]" value="' + path + '" disabled type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control autofocus" name="folder[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><input class="form-control" name="folder[original]" value="' + original + '" type="hidden"/><button type="submit" class="btn btn-aqua">' + submit + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
        logger(1, 'DEBUG: popping up the folder-' + action + ' form.');
        addModal(title, html, '');
        validateFolder();
    }
}

// Import external labs
function printFormImport(path) {
    var html = '<form id="form-import" class="form-horizontal form-import"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[20] + '</label><div class="col-md-5"><input class="form-control" name="import[path]" value="' + path + '" disabled type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[2] + '</label><div class="col-md-5"><input class="form-control" name="import[local]" value="" disabled="" placeholder="' + MESSAGES[25] + '" "type="text"/></div></div><div class="form-group"><div class="col-md-7 col-md-offset-3"><span class="btn btn-default btn-file btn-aqua">' + MESSAGES[23] + ' <input class="form-control" name="import[file]" value="" type="file"></span> <button type="submit" class="btn btn-aqua">' + MESSAGES[24] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
    logger(1, 'DEBUG: popping up the import form.');
    addModal(MESSAGES[9], html, '');
    validateImport();
}

// Add a new lab
function printFormLab(action, values) {
    if (action == 'add') {
        var path = values['path'];
    } else {
        var path = (values['path'] == '/') ? '/' + values['name'] + '.unl' : values['path'] + '/' + values['name'] + '.unl';
    }
    var name = (values['name'] != null) ? values['name'] : '';
    var version = (values['version'] != null) ? values['version'] : '';
    var scripttimeout = (values['scripttimeout'] != null) ? values['scripttimeout'] : '300';
    var author = (values['author'] != null) ? values['author'] : '';
    var description = (values['description'] != null) ? values['description'] : '';
    var body = (values['body'] != null) ? values['body'] : '';
    var title = (action == 'add') ? MESSAGES[5] : MESSAGES[87];
    var html = '<form id="form-lab-' + action + '" class="form-horizontal form-lab-' + action + '">' +
        '<div class="form-group">' +
        '<label class="col-md-3 control-label">' + MESSAGES[20] + '</label>' +
        '<div class="col-md-5">' +
        '<input class="form-control" name="lab[path]" value="' + path + '" disabled="" type="text"/>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="col-md-3 control-label">' + MESSAGES[19] + '</label>' +
        '<div class="col-md-5"><input class="form-control autofocus" name="lab[name]" value="' + name + '" type="text"/>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="col-md-3 control-label">' + MESSAGES[26] + '</label>' +
        '<div class="col-md-5"><input class="form-control" name="lab[version]" value="' + version + '" type="text"/>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="col-md-3 control-label">Author</label>' +
        '<div class="col-md-5">' +
        '<input class="form-control" name="lab[author]" value="' + author + '" type="text"/>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="col-md-3 control-label">' + MESSAGES[27] + '</label>' +
        '<div class="col-md-5">' +
        '<textarea class="form-control" name="lab[description]">' + description + '</textarea>' +
        '</div>' +
        '</div>' +
        '<div class="form-group"> ' +
        '<label class="col-md-3 control-label">' + MESSAGES[88] + '</label>' +
        '<div class="col-md-5">' +
        '<textarea class="form-control" name="lab[body]">' + body + '</textarea>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="col-md-3 control-label">' + MESSAGES[158] + '</label>' +
        '<div class="col-md-5"><input class="form-control" name="lab[scripttimeout]" value="' + scripttimeout + '" type="text"/>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<div class="col-md-5 col-md-offset-3">' +
        '<button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button>' +
        '<button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button>' +
        '</div>' +
        '</div>' +
        '</form>';
    logger(1, 'DEBUG: popping up the lab-add form.');
    addModalWide(title, html, '');
    validateLabInfo();
}

// Network Form
function printFormNetwork(action, values) {
    var id = (values == null || values['id'] == null) ? '' : values['id'];
    var left = (values == null || values['left'] == null) ? '' : values['left'];
    var name = (values == null || values['name'] == null) ? 'Net' : values['name'];
    var top = (values == null || values['top'] == null) ? '' : values['top'];
    var type = (values == null || values['type'] == null) ? '' : values['type'];
    var title = (action == 'add') ? MESSAGES[89] : MESSAGES[90];

    $.when(getNetworkTypes()).done(function (network_types) {
        // Read privileges and set specific actions/elements
        var html = '<form id="form-network-' + action + '" class="form-horizontal">';
        if (action == 'add') {
            // If action == add -> print the nework count input
            html += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[114] + '</label><div class="col-md-5"><input class="form-control" name="network[count]" value="1" type="text"/></div></div>';
        } else {
            // If action == edit -> print the network ID
            html += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[92] + '</label><div class="col-md-5"><input class="form-control" disabled name="network[id]" value="' + id + '" type="text"/></div></div>';
        }
        html += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[103] + '</label><div class="col-md-5"><input class="form-control autofocus" name="network[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[95] + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="network[type]" data-live-search="true" data-style="selectpicker-button">';
        $.each(network_types, function (key, value) {
            // Print all network types
            var type_selected = (key == type) ? 'selected ' : '';
            html += '<option ' + type_selected + 'value="' + key + '">' + value + '</option>';
        });
        html += '</select></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[93] + '</label><div class="col-md-5"><input class="form-control" name="network[left]" value="' + left + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[94] + '</label><div class="col-md-5"><input class="form-control" name="network[top]" value="' + top + '" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form></form>';

        // Show the form
        addModal(title, html, '', 'second-win');
        $('.selectpicker').selectpicker();
        $('.autofocus').focus();
    });
}

// Node form
function printFormNode(action, values) {
    var id = (values == null || values['id'] == null) ? null : values['id'];
    var left = (values == null || values['left'] == null) ? null : values['left'];
    var top = (values == null || values['top'] == null) ? null : values['top'];
    var template = (values == null || values['template'] == null) ? null : values['template'];

    var title = (action == 'add') ? MESSAGES[85] : MESSAGES[86];
    var template_disabled = (values == null || values['template'] == null) ? '' : 'disabled ';

    $.when(getTemplates(null)).done(function (templates) {
        var html = '';
        html += '<form id="form-node-' + action + '" class="form-horizontal"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[84] + '</label><div class="col-md-5"><select id="form-node-template" class="selectpicker form-control" name="node[template]" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[102] + '</option>';
        $.each(templates, function (key, value) {
            // Adding all templates
            html += '<option value="' + key + '">' + value + '</option>';
        });
        html += '</select></div></div><div id="form-node-data"></div><div id="form-node-buttons"></div></form>';

        // Show the form
        addModal(title, html, '', 'second-win');
        $('.selectpicker').selectpicker();

        $('#form-node-template').change(function (e2) {
            id = (id == '') ? null : id;    // Ugly fix for change template after selection
            template = $(this).find("option:selected").val();
            if (template != '') {
                // Getting template only if a valid option is selected (to avoid requests during typewriting)
                $.when(getTemplates(template), getNodes(id)).done(function (template_values, node_values) {
                    // TODO: this event is called twice
                    id = (id == null) ? '' : id;
                    var html_data = '<input name="node[type]" value="' + template_values['type'] + '" type="hidden"/>';
                    if (action == 'add') {
                        // If action == add -> print the nework count input
                        html_data += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[113] + '</label><div class="col-md-5"><input class="form-control" name="node[count]" value="1" type="text"/></div></div>';
                    } else {
                        // If action == edit -> print the network ID
                        html_data += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[92] + '</label><div class="col-md-5"><input class="form-control" disabled name="node[id]" value="' + id + '" type="text"/></div></div>';
                    }
                    $.each(template_values['options'], function (key, value) {
                        // Print all options from template
                        var value_set = (node_values != null && node_values[key] != null) ? node_values[key] : value['value'];
                        if (value['type'] == 'list') {
                            // Option is a list
                            html_data += '<div class="form-group"><label class="col-md-3 control-label">' + value['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="node[' + key + ']" data-style="selectpicker-button">';
                            $.each(value['list'], function (list_key, list_value) {
                                var selected = (list_key == value_set) ? 'selected ' : '';
                                html_data += '<option ' + selected + 'value="' + list_key + '">' + list_value + '</option>';
                            });
                            html_data += '</select></div>';
                            html_data += '</div>';
                        } else {
                            // Option is standard
                            html_data += '<div class="form-group"><label class="col-md-3 control-label">' + value['name'] + '</label><div class="col-md-5"><input class="form-control' + ((key == 'name') ? ' autofocus' : '') + '" name="node[' + key + ']" value="' + value_set + '" type="text"/></div></div>';
                        }
                    });
                    html_data += '<div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[93] + '</label><div class="col-md-5"><input class="form-control" name="node[left]" value="' + left + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[94] + '</label><div class="col-md-5"><input class="form-control" name="node[top]" value="' + top + '" type="text"/></div></div>';

                    // Show the buttons
                    $('#form-node-buttons').html('<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div>');

                    // Show the form
                    $('#form-node-data').html(html_data);
                    $('.selectpicker').selectpicker();
                    $('.autofocus').focus();
                    validateNode();
                }).fail(function (message1, message2) {
                    // Cannot get data
                    if (message1 != null) {
                        addModalError(message1);
                    } else {
                        addModalError(message2)
                    }
                    ;
                });
            }
        });

        if (action == 'edit') {
            // If editing a node, disable the select and trigger
            $('#form-node-template').prop('disabled', 'disabled');
            $('#form-node-template').val(template).change();
        }

    }).fail(function (message) {
        // Cannot get data
        addModalError(message);
    });
}

// Node config
function printFormNodeConfigs(values, cb) {
    var title = values['name'] + ': ' + MESSAGES[123];
    if (ROLE == 'admin' || ROLE == 'editor') {
        var html = '<form id="form-node-config" class="form-horizontal"><input name="config[id]" value="' + values['id'] + '" type="hidden"/><div class="form-group"><div class="col-md-12"><textarea class="form-control autofocus" id="nodeconfig" name="config[data]" rows="15"></textarea></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
    } else {
        var html = '<div class="col-md-12"><pre>' + values['data'] + '</pre></div>';
    }
    $('#config-data').html(html);
    $('#nodeconfig').val(values['data']);
    cb && cb();
}

// Custom Shape form
function printFormCustomShape(values) {
    var shapeTypes = ['square', 'circle'],
        borderTypes = ['solid', 'dashed'],
        left = (values == null || values['left'] == null) ? null : values['left'],
        top = (values == null || values['top'] == null) ? null : values['top'];

  var html = '<form id="main-modal" class="container col-md-12 col-lg-12 custom-shape-form">' +
        '<div class="row">' +
        '<div class="col-md-8 col-md-offset-1 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Type</label>' +
        '<div class="col-md-5">' +
        '<select class="form-control shape-type-select">' +
        '</select>' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-8 col-md-offset-1 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Name</label>' +
        '<div class="col-md-5">' +
        '<input type="text" class="form-control shape_name" placeholder="Name">' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-8 col-md-offset-1 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Border-type</label>' +
        '<div class="col-md-5">' +
        '<select class="form-control border-type-select" >' +
        '</select>' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-8 col-md-offset-1 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Border-width</label>' +
        '<div class="col-md-5">' +
        '<input type="number" min="0" value="5" class="form-control shape_border_width">' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-8 col-md-offset-1 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Border-color</label>' +
        '<div class="col-md-5">' +
        '<input type="color" class="form-control shape_border_color">' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-8 col-md-offset-1 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Background-color</label>' +
        '<div class="col-md-5">' +
        '<input type="color" class="form-control shape_background_color">' +
        '</div>' +
        '</div> <br>' +
        '<button type="submit" class="btn btn-aqua col-md-offset-1">' + MESSAGES[47] + '</button>' +
        '<button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button>' +
        '</div>' +
        '<input  type="text" class="hide left-coordinate" value="' + left + '">' +
        '<input  type="text" class="hide top-coordinate" value="' + top + '">' +
        '</form>';

    addModal("ADD CUSTOM SHAPE", html, '');

    $('.custom-shape-form .shape_background_color').val('#ffffff');

    for (var i = 0; i < shapeTypes.length; i++) {
        $('.shape-type-select').append($('<option></option>').val(shapeTypes[i]).html(shapeTypes[i]));
    }

    for (var j = 0; j < borderTypes.length; j++) {
        $('.border-type-select').append($('<option></option>').val(borderTypes[j]).html(borderTypes[j]));
    }

};

// Text form
function printFormText(values) {
    var left = (values == null || values['left'] == null) ? null : values['left']
        , top = (values == null || values['top'] == null) ? null : values['top']
        , fontStyles = ['normal', 'bold', 'italic']
        ;

  var html = '<form id="main-modal" class="container col-md-12 col-lg-12 add-text-form">' +
        '<div class="row">' +
        '<div class="col-md-12 col-md-offset-0 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Text</label>' +
        '<div class="col-md-9">' +
        '<textarea class="form-control main-text autofocus" >' +
        '</textarea>' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-12 col-md-offset-0 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Font Size</label>' +
        '<div class="col-md-9">' +
        '<input type="number" min="0" class="form-control text_font_size" value="12">' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-12 col-md-offset-0 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Font Style</label>' +
        '<div class="col-md-9">' +
        '<select class="form-control text-font-style-select" >' +
        '</select>' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-12 col-md-offset-0 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Font Color</label>' +
        '<div class="col-md-9">' +
        '<input type="color" class="form-control text_font_color">' +
        '</div>' +
        '</div> <br>' +
        '<div class="col-md-12 col-md-offset-0 form-group">' +
        '<label class="col-md-3 control-label form-group-addon">Background Color</label>' +
        '<div class="col-md-9">' +
        '<input type="color" class="form-control text_background_color">' +
        '</div>' +
        '</div> <br>' +
         '<button type="submit" class="btn btn-aqua col-md-offset-1">' + MESSAGES[47] + '</button>' +
        '<button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button>' +
        '</div>' +
        '<input  type="text" class="hide left-coordinate" value="' + left + '">' +
        '<input  type="text" class="hide top-coordinate" value="' + top + '">' +
        '</form>';

    addModal("ADD TEXT", html, '');
    $('.autofocus').focus();
    $('.add-text-form .text_background_color').val('#ffffff');

    for (var i = 0; i < fontStyles.length; i++) {
        $('.text-font-style-select').append($('<option></option>').val(fontStyles[i]).html(fontStyles[i]));
    }
};

// Map picture
function printNodesMap(values, cb) {
    var title = values['name'] + ': ' + MESSAGES[123];
    var html = '<div class="col-md-12">' + values.body + '</div><div class="text-right">' + values.footer + '</div>';
    $('#config-data').html(html);
    cb && cb();
}

//save lab handler
function saveLab(form) {
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = form2Array('config');
    var url = '/api/labs' + lab_filename + '/configs/' + form_data['id'];
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: config saved.');
                // Close the modal
                $('body').children('.modal').attr('skipRedraw', true);
                if (form) {
                    $('body').children('.modal').modal('hide');
                    addMessage(data['status'], data['message']);
                }
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                addModal('ERROR', '<p>' + data['message'] + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            addModal('ERROR', '<p>' + message + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
        }
    });
    return false;  // Stop to avoid POST
}

// Node interfaces
function printFormNodeInterfaces(values) {
    $.when(getLabLinks()).done(function (links) {
        var html = '<form id="form-node-connect" class="form-horizontal">';
        html += '<input name="node_id" value="' + values['node_id'] + '" type="hidden"/>';
        if (values['sort'] == 'iol') {
            // IOL nodes need to reorder interfaces
            // i = x/y with x = i % 16 and y = (i - x) / 16
            var iol_interfc = {};
            $.each(values['ethernet'], function (interfc_id, interfc) {
                var x = interfc_id % 16;
                var y = (interfc_id - x) / 16;
                iol_interfc[4 * x + y] = '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
                $.each(links['ethernet'], function (link_id, link) {
                    var link_selected = (interfc['network_id'] == link_id) ? 'selected ' : '';
                    iol_interfc[4 * x + y] += '<option ' + link_selected + 'value="' + link_id + '">' + link + '</option>';
                });
                iol_interfc[4 * x + y] += '</select></div></div>';
            });
            $.each(iol_interfc, function (key, value) {
                html += value;
            });
        } else {
            $.each(values['ethernet'], function (interfc_id, interfc) {
                html += '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
                $.each(links['ethernet'], function (link_id, link) {
                    var link_selected = (interfc['network_id'] == link_id) ? 'selected ' : '';
                    html += '<option ' + link_selected + 'value="' + link_id + '">' + link + '</option>';
                });
                html += '</select></div></div>';
            });
        }
        if (values['sort'] == 'iol') {
            // IOL nodes need to reorder interfaces
            // i = x/y with x = i % 16 and y = (i - x) / 16
            var iol_interfc = {};
            $.each(values['serial'], function (interfc_id, interfc) {
                var x = interfc_id % 16;
                var y = (interfc_id - x) / 16;
                iol_interfc[4 * x + y] = '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
                $.each(links['serial'], function (node_id, serial_link) {
                    if (values['node_id'] != node_id) {
                        $.each(serial_link, function (link_id, link) {
                            var link_selected = (interfc['remote_id'] + ':' + interfc['remote_if'] == node_id + ':' + link_id) ? 'selected ' : '';
                            iol_interfc[4 * x + y] += '<option ' + link_selected + 'value="' + node_id + ':' + link_id + '">' + link + '</option>';
                        });
                    }
                });
                iol_interfc[4 * x + y] += '</select></div></div>';
            });
            $.each(iol_interfc, function (key, value) {
                html += value;
            });
        } else {
            $.each(values['serial'], function (interfc_id, interfc) {
                html += '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker form-control" name="interfc[' + interfc_id + ']" data-live-search="true" data-style="selectpicker-button"><option value="">' + MESSAGES[117] + '</option>';
                $.each(links['serial'], function (node_id, serial_link) {
                    if (values['node_id'] != node_id) {
                        $.each(serial_link, function (link_id, link) {
                            var link_selected = '';
                            html += '<option ' + link_selected + 'value="' + link_id + '">' + link + '</option>';
                        });
                    }
                });
                html += '</select></div></div>';
            });
        }

        html += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';

        addModal(values['node_name'] + ': ' + MESSAGES[116], html, '', 'second-win');
        $('.selectpicker').selectpicker();
    }).fail(function (message) {
        // Cannot get data
        addModalError(message);
    });
}

// Display picture in form
function printPictureInForm(id) {
    var picture_id = id;
    var picture_url = '/api/labs' + $('#lab-viewport').attr('data-path') + '/pictures/' + picture_id + '/data';

    $.when(getPictures(picture_id)).done(function (picture) {
        var picture_map = picture['map'];
        picture_map = picture_map.replace(/{{IP}}/g, location.hostname);
        picture_map = picture_map.replace(/{{(NODE\$?){1}([0-9]+){1}}}/g, function (matchedString, group1, group2, startingPosition, originString) {
            return parseInt(group2) + 32768 + 128 * TENANT;
        });
        // Read privileges and set specific actions/elements
        var body = '<div id="lab_picture">' +
            '<img usemap="#picture_map" ' +
            'src="' + picture_url + '" ' +
            'alt="' + picture['name'] + '" ' +
            'title="' + picture['name'] + '" ' +
            'width="' + picture['width'] + '" ' +
            'height="' + picture['height'] + '"/>' +
            '<map name="picture_map">' + picture_map + '</map>' +
            '</div>';
        if (ROLE == 'admin' || ROLE == 'editor') {
            var footer = '<button type="button" class="btn btn-aqua action-pictureedit" data-path="' + picture_id + '">Edit</button>';
        } else {
            var footer = '';
        }
        printNodesMap({name: picture['name'], body: body, footer: footer}, function () {
            setTimeout(function () {
                $('map').imageMapResize();
            }, 500);
        });
    }).fail(function (message) {
        addModalError(message);
    });
}

// Display picture form
function displayPictureForm(picture_id) {
    var deferred = $.Deferred();
    var form = '';
    var lab_file = LAB;
    if (picture_id == null) {
        // Adding a new picture
        var title = 'Add new picture';
        var action = 'picture-add';
        var button = 'Add';
        // Header
        form += '<form id="form-' + action + '" class="form-horizontal form-picture">';
        // Name
        form += '<div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input type="text" class="form-control-static" name="picture[name]" value=""/></div></div>';
        // File (add only)
        form += '<div class="form-group"><label class="col-md-3 control-label">Picture</label><div class="col-md-5"><input type="file" name="picture[file]" value=""/></div></div>';
        // Footer
        form += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">' + button + '</button><button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div></form>';
        // Add the form to the HTML page
        // $('#form_frame').html(form);

        addModal("Add picture", form, '<div></div>');

        // Show the form
        // $('#modal-' + action).modal('show');
        $('.selectpicker').selectpicker();
        validateLabPicture();
        deferred.resolve();
    } else {
        // Can be lab_edit or lab_open

        $.when(getPicture(lab_file, picture_id)).done(function (picture) {
            if (picture != null) {
                if ($(location).attr('pathname') == '/lab_edit.php') {
                    var title = 'Edit picture';
                    var action = 'picture_edit';
                    var button = 'Save';

                    picture_name = picture['name'];
                    if (typeof picture['map'] != 'undefined') {
                        picture_map = picture['map'];
                    } else {
                        picture_map = '';
                    }
                    // Header
                    form += '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog" style="width: 100%;"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body"><form id="form-' + action + '" class="form-horizontal form-picture">';
                    // Name
                    form += '<div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input type="text" class="form-control" name="picture[name]" value="' + picture_name + '"/></div></div>';
                    // Picure
                    form += '<img id="lab_picture" src="/api/labs' + lab_file + '/pictures/' + picture_id + '/data">'
                    // MAP
                    form += '<div class="form-group"><label class="col-md-3 control-label">Map</label><div class="col-md-5"><textarea type="textarea" name="picture[map]">' + picture_map + '</textarea></div></div>';
                    // Footer
                    form += '<input type="hidden" name="picture[id]" value="' + picture_id + '"/>';
                    form += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">' + button + '</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div></form></div></div></div></div>';
                    // Add the form to the HTML page
                    $('#form_frame').html(form);

                    // Show the form
                    $('#modal-' + action).modal('show');
                    $('.selectpicker').selectpicker();
                    validateLabPicture();
                    deferred.resolve();
                } else {
                    var action = 'picture_open';
                    var title = picture['name'];
                    if (typeof picture['map'] != 'undefined') {
                        picture_map = picture['map'];
                    } else {
                        picture_map = '';
                    }
                    // Header
                    form += '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog" style="width: 100%;"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">';
                    // Picure
                    form += '<img id="lab_picture" src="/api/labs' + lab_file + '/pictures/' + picture_id + '/data" usemap="#picture_map">';
                    // Map
                    form += '<map name="picture_map">' + translateMap(picture_map) + '</map>';
                    // Footer
                    form += '</div></div></div></div>';
                    // Add the form to the HTML page
                    $('#form_frame').html(form);

                    // Show the form
                    $('#modal-' + action).modal('show');
                    deferred.resolve();
                }
            } else {
                // Cannot get picture
                raiseMessage('DANGER', 'Cannot get picture (picture_id = ' + picture_id + ').');
                deferred.reject();
            }
        });
    }

    return deferred.promise();
}

// Add a new picture
function printFormPicture(action, values) {
    var map = (values['map'] != null) ? values['map'] : ''
        , name = (values['name'] != null) ? values['name'] : ''
        , width = (values['width'] != null) ? values['width'] : ''
        , height = (values['height'] != null) ? values['height'] : ''
        , title = (action == 'add') ? MESSAGES[135] : MESSAGES[137]
        , html = '';

    if (action == 'add') {
        html += '<form id="form-picture-' + action + '" class="form-horizontal form-lab-' + action + '"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control" autofocus name="picture[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[137] + '</label><div class="col-md-5"><textarea class="form-control" name="picture[map]">' + map + '</textarea></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
    } else {
        html += '<form id="form-picture-' + action + '" class="form-horizontal form-lab-' + action + '" data-path=' + values['id'] + '><div class="follower-wrapper"><img src="/api/labs' + $('#lab-viewport').attr('data-path') + '/pictures/' + values['id'] + '/data" alt="' + values['name'] + '" width="' + values['width'] + '" height="' + values['height'] + '"/><div id="follower"></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control" autofocus name="picture[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[137] + '</label><div class="col-md-5"><textarea class="form-control" name="picture[map]">' + map + '</textarea></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + MESSAGES[47] + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
    }
    logger(1, 'DEBUG: popping up the picture form.');
    addModalWide(title, html, '', 'second-win modal-ultra-wide');
    validateLabInfo();
}

// User form
function printFormUser(action, values) {
    $.when(getRoles()).done(function (roles) {
        // Got data
        var username = (values['username'] != null) ? values['username'] : '';
        var name = (values['name'] != null) ? values['name'] : '';
        var email = (values['email'] != null) ? values['email'] : '';
        var role = (values['role'] != null) ? values['role'] : '';
        var expiration = (values['expiration'] != null && values['expiration'] != -1) ? $.datepicker.formatDate('yy-mm-dd', new Date(values['expiration'] * 1000)) : '';
        var pod = (values['pod'] != null && values['pod'] != -1) ? values['pod'] : '';
        var pexpiration = (values['pexpiration'] != null && values['pexpiration'] != -1) ? $.datepicker.formatDate('yy-mm-dd', new Date(values['pexpiration'] * 1000)) : '';
        var submit = (action == 'add') ? MESSAGES[17] : MESSAGES[47];
        var title = (action == 'add') ? MESSAGES[34] : MESSAGES[48] + ' ' + username;
        var user_disabled = (action == 'add') ? '' : 'disabled ';
        var html = '<form id="form-user-' + action + '" class="form-horizontal form-user-' + action + '"><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[44] + '</label><div class="col-md-5"><input class="form-control autofocus" ' + user_disabled + 'name="user[username]" value="' + username + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[19] + '</label><div class="col-md-5"><input class="form-control" name="user[name]" value="' + name + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[28] + '</label><div class="col-md-5"><input class="form-control" name="user[email]" value="' + email + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[45] + '</label><div class="col-md-5"><input class="form-control" name="user[password]" value="" type="password"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[29] + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="user[role]" data-live-search="true" data-style="selectpicker-button">';
        $.each(roles, function (key, value) {
            var role_selected = (role == key) ? 'selected ' : '';
            html += '<option ' + role_selected + 'value="' + key + '">' + value + '</option>';
        });
        html += '</select></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[30] + '</label><div class="col-md-5"><input class="form-control expiration" name="user[expiration]" value="' + expiration + '" type="text"/></div></div><h4>' + MESSAGES[46] + '</h4><div class="form-group"><label class="col-md-3 control-label">POD</label><div class="col-md-5"><input class="form-control pod" name="user[pod]" value="' + pod + '" type="text"/></div></div><div class="form-group"><label class="col-md-3 control-label">' + MESSAGES[30] + '</label><div class="col-md-5"><input class="form-control expiration pod" name="user[pexpiration]" value="' + pexpiration + '" type="text"/></div></div><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-aqua">' + submit + '</button> <button type="button" class="btn btn-grey" data-dismiss="modal">' + MESSAGES[18] + '</button></div></div></form>';
        addModal(title, html, '');
        if (ROLE == "user") {
            $("#form-user-edit input,#form-user-edit select").prop("disabled", true)
            $("#form-user-edit button").remove();
        }
        if (ROLE == "editor") {
            $("#form-user-edit select").prop("disabled", true)
            $("#form-user-edit .pod,#form-user-edit .expiration").prop("disabled", true)
        }
        $('.selectpicker').selectpicker();
        $('.expiration').datepicker({dateFormat: 'yy-mm-dd'});
        //$(".expiration").on("blur", function(e) { $(this).datepicker("hide"); });

        //datepicker forced to close on click
        $('.modal-dialog').on('click', function (e) {
            if (!$(e.target).hasClass('expiration'))
                $('.expiration').datepicker('hide');
        });

        $('.modal').on('hidden.bs.modal', function () {
            $('.expiration').datepicker('hide');
        })

        validateUser();
    }).fail(function (message) {
        // Cannot get data
        addModalError(message);
    });
}

// Print lab preview section
function printLabPreview(lab_filename) {
    $.when(getLabInfo(lab_filename)).done(function (lab) {
        var html = '<h1>' + lab['name'] + ' v' + lab['version'] + '</h1>';
        if (lab['author'] != null) {
            html += '<h2>by ' + lab['author'] + '</h2>';
        }
        html += '<p><code>' + lab['id'] + '</code></p>';
        if (lab['description'] != null) {
            html += '<p>' + lab['description'] + '</p>';
        }
        html += '<button class="action-labopen btn btn-aqua" type="button" data-path="' + lab_filename + '">' + MESSAGES[22] + '</button> ';
        if (ROLE != "user")
            html += '<button class="action-labedit-inline btn btn-aqua" type="button" data-path="' + lab_filename + '">Edit</button>';
        $('#list-title-info span').html(lab['filename'].replace(/\\/g, '/').replace(/.*\//, ''));
        $('#list-info').html(html);
    }).fail(function (message) {
        addModalError(message);
    });
}

// Print lab topology
function printLabTopology() {
    var lab_filename = $('#lab-viewport').attr('data-path')
        , $labViewport = $('#lab-viewport')
        , loadingLabHtml = '' +
            '<div id="loading-lab" class="loading-lab">' +
            '<div class="container">' +
            '<img src="/themes/default/images/wait.gif"/><br />' +
            '<h3>Loading Lab</h3>' +
            '<div class="progress">' +
            '<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>' +
            '</div>' +
            '</div>' +
            '</div>'
        , labNodesResolver = $.Deferred()
        , labTextObjectsResolver = $.Deferred()
        , progressbarValue = 0
        , progressbarMax = 100
        ;

    if ($labViewport.data("refreshing")) {
        return;
    }
    $labViewport.empty();
    $labViewport.data('refreshing', true);
    $labViewport.after(loadingLabHtml);
    $("#lab-sidebar *").hide();


     $.when(
        getNetworks(null),
        getNodes(null),
        getTopology(),
        getTextObjects()
    ).done(function (networks, nodes, topology, textObjects) {


        var networkImgs = []
            , nodesImgs = []
            , textObjectsCount = Object.keys(textObjects).length
            ;

        progressbarMax = Object.keys(networks).length + Object.keys(nodes).length + Object.keys(textObjects).length;
        $(".progress-bar").attr("aria-valuemax", progressbarMax);

        $.each(networks, function (key, value) {
            var icon;
            var unusedClass='';

            if (value['type'] == 'bridge') {
                icon = 'lan.png';
                unusedClass = ' unused ';
            } else if (value['type'] == 'ovs') {
                icon = 'lan.png';

            } else {
                icon = 'cloud.png';
            }


            $labViewport.append(
                '<div id="network' + value['id'] + '" ' +
                'class="context-menu network network' + value['id'] + ' network_frame '+unusedClass+' " ' +
                'style="top: ' + value['top'] + 'px; left: ' + value['left'] + 'px" ' +
                'data-path="' + value['id'] + '" ' +
                'data-name="' + value['name'] + '">' +
                '<div class="network_name">' + value['name'] + '</div>' +
                '</div>');

            networkImgs.push($.Deferred(function (defer) {
                var img = new Image();

                img.onload = resolve;
                img.onerror = resolve;
                img.onabort = resolve;

                img.src = "/images/" + icon;

                $(img).prependTo("#network" + value['id']);

                function resolve(image) {
                    img.onload = null;
                    img.onerror = null;
                    img.onabort = null;
                    defer.resolve(image);
                }
            }));

            $(".progress-bar").css("width", ++progressbarValue / progressbarMax * 100 + "%");



        });
        $.each(nodes, function (key, value) {
            $labViewport.append(
                '<div id="node' + value['id'] + '" ' +
                'class="context-menu node node' + value['id'] + ' node_frame" ' +
                'style="top: ' + value['top'] + 'px; left: ' + value['left'] + 'px;" ' +
                'data-path="' + value['id'] + '" ' +
                'data-status="' + value['status'] + '" ' +
                'data-name="' + value['name'] + '">' +
                '<a href="' + value['url'] + '">' +
                '</a>' +
                '<div class="node_name"><i class="node' + value['id'] + '_status"></i> ' + value['name'] + '</div>' +
                '</div>');

            nodesImgs.push($.Deferred(function (defer) {
                var img = new Image();

                img.onload = resolve;
                img.onerror = resolve;
                img.onabort = resolve;

                img.src = "/images/icons/" + value['icon'];

                $(img).appendTo("#node" + value['id'] + " a");

                function resolve(image) {
                    img.onload = null;
                    img.onerror = null;
                    img.onabort = null;
                    defer.resolve(image);
                }
            }));

            $(".progress-bar").css("width", ++progressbarValue / progressbarMax * 100 + "%");
        });

        //add shapes from server to viewport
        $.each(textObjects, function (key, value) {
            getTextObject(value['id']).done(function (textObject) {
                $(".progress-bar").css("width", ++progressbarValue / progressbarMax * 100 + "%");
                if (--textObjectsCount === 0) {
                    labTextObjectsResolver.resolve();
                }

                var $newTextObject = $(textObject['data']);

                if ($newTextObject.attr("id").indexOf("customShape") !== -1) {
                    $newTextObject.attr("id", "customShape" + textObject.id);
                    $newTextObject.attr("data-path", textObject.id);
                    $labViewport.prepend($newTextObject);

                    $newTextObject
                        .draggable({
                            stop: textObjectDragStop
                        })
                        .resizable().resizable("destroy")
                        .resizable({
                            autoHide: true,
                            resize: function (event, ui) {
                                textObjectResize(event, ui, {"shape_border_width": 5});
                            },
                            stop: textObjectDragStop
                        });
                }
                else if ($newTextObject.attr("id").indexOf("customText") !== -1) {
                    $newTextObject.attr("id", "customText" + textObject.id);
                    $newTextObject.attr("data-path", textObject.id);
                    $labViewport.prepend($newTextObject);

                    $newTextObject
                        .draggable({
                            stop: textObjectDragStop
                        })
                        .resizable().resizable('destroy')
                        .resizable({
                            autoHide: true,
                            resize: function (event, ui) {
                                textObjectResize(event, ui, {"shape_border_width": 5});
                            },
                            stop: textObjectDragStop
                        });
                }
                else {
                    return void 0;
                }
            }).fail(function () {
                logger(1, 'DEBUG: Failed to load Text Object' + value['name'] + '!');
            });
        });
        if (Object.keys(textObjects).length === 0) {
            labTextObjectsResolver.resolve();
        }

        $.when.apply($, networkImgs.concat(nodesImgs)).done(function () {
            // Drawing topology
            jsPlumb.ready(function () {
                // Defaults
                jsPlumb.importDefaults({
                    Anchor: 'Continuous',
                    Connector: ['Straight'],
                    Endpoint: 'Blank',
                    PaintStyle: {lineWidth: 2, strokeStyle: '#58585a'},
                    cssClass: 'link'
                });

                // Create jsPlumb topology
                var lab_topology = jsPlumb.getInstance();
                lab_topology.setContainer($("#lab-viewport"));
                lab_topology.importDefaults({
                    Anchor: 'Continuous',
                    Connector: ['Straight'],
                    Endpoint: 'Blank',
                    PaintStyle: {lineWidth: 2, strokeStyle: '#58585a'},
                    cssClass: 'link'
                });

                // Read privileges and set specific actions/elements
                if (ROLE == 'admin' || ROLE == 'editor') {
                    // Nodes and networks are draggable within a grid
                    lab_topology.draggable($('.node_frame, .network_frame'), {grid: [10, 10]});
                }

                $.each(topology, function (id, link) {
                    var type = link['type'],
                        source = link['source'],
                        source_label = link['source_label'],
                        destination = link['destination'],
                        destination_label = link['destination_label'],
                        src_label = ["Label"],
                        dst_label = ["Label"];

                    if (type == 'ethernet') {
                        if (source_label != '') {
                            src_label.push({
                                label: source_label,
                                location: 0.15,
                                cssClass: 'node_interface ' + source + ' ' + destination
                            });
                        } else {
                            src_label.push(Object());
                        }
                        if (destination_label != '') {
                            dst_label.push({
                                label: destination_label,
                                location: 0.85,
                                cssClass: 'node_interface ' + source + ' ' + destination
                            });
                        } else {
                            dst_label.push(Object());
                        }

                     
                        lab_topology.connect({
                            source: source,       // Must attach to the IMG's parent or not printed correctly
                            target: destination,  // Must attach to the IMG's parent or not printed correctly
                            cssClass: source + ' ' + destination + ' frame_ethernet',
                            overlays: [src_label, dst_label]
                        });
                    } else {
                        src_label.push({
                            label: source_label,
                            location: 0.15,
                            cssClass: 'node_interface ' + source + ' ' + destination
                        });
                        dst_label.push({
                            label: destination_label,
                            location: 0.85,
                            cssClass: 'node_interface ' + source + ' ' + destination
                        });

                        lab_topology.connect({
                            source: source,       // Must attach to the IMG's parent or not printed correctly
                            target: destination,  // Must attach to the IMG's parent or not printed correctly
                            cssClass: source + " " + destination + ' frame_serial',
                            paintStyle: {lineWidth: 2, strokeStyle: "#ffcc00"},
                            overlays: [src_label, dst_label]
                        });
                    }

                    // If destination is a network, remove the 'unused' class
                    if (destination.substr(0, 7) == 'network') {
                        $('.' + destination).removeClass('unused');
                    }


                });

                // Remove unused elements
                $('.unused').remove();

                printLabStatus();

                // Move elements under the topology node
                $('._jsPlumb_connector, ._jsPlumb_overlay, ._jsPlumb_endpoint_anchor_').detach().appendTo('#lab-viewport');
                $labViewport.data('refreshing', false);
                labNodesResolver.resolve();
            });
        }).fail(function () {
            logger(1, "DEBUG: not all images of networks or nodes loaded");
            $('#lab-viewport').data('refreshing', false);
            labNodesResolver.reject();
            labTextObjectsResolver.reject();
        });
    }).fail(function (message1, message2, message3) {
        if (message1 != null) {
            addModalError(message1);
        } else if (message2 != null) {
            addModalError(message2)
        } else {
            addModalError(message3)
        }
        $('#lab-viewport').data('refreshing', false);
        labNodesResolver.reject();
        labTextObjectsResolver.reject();
    });


    $.when(labNodesResolver, labTextObjectsResolver).done(function () {

        return $.when(deleteSingleNetworks()).done(function(){
            $("#loading-lab").remove();
            $("#lab-sidebar *").show();


            var active = localStorage.getItem('action-nodelink');

           $('.action-nodelink').toggleClass('active',(active=='true'));

        })

    }).fail(function (message1, message2) {
        if (message1 != null) {
            addModalError(message1);
        } else if (message2 != null) {
            addModalError(message2)
        }
        $("#loading-lab").remove();
        $("#lab-sidebar ul").show();
        $("#lab-sidebar ul li:lt(11)").hide();
    });



}

// Display lab status
function printLabStatus() {
    logger(1, 'DEBUG: updating node status');
    $.when(getNodes(null)).done(function (nodes) {
        $.each(nodes, function (node_id, node) {
            if (node['status'] == 0) {
                // Stopped
                $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-stop');

            } else if (node['status'] == 1) {
                // Stopped and locked
                $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-warning-sign');
            } else if (node['status'] == 2) {
                // Running
                $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-play');
            } else if (node['status'] == 3) {
                // Running and locked
                $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-time');
            } else {
                // Undefined
                $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-question-sign');
            }

            //add status attr
            $('.node' + node['id']).attr('data-status',node['status']);

        });
    }).fail(function (message) {
        addMessage('danger', message);
    });
}

// Display all networks in a table
function printListNetworks(networks) {
    logger(1, 'DEBUG: printing network list');
    var body = '<div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[92] + '</th><th>' + MESSAGES[19] + '</th><th>' + MESSAGES[95] + '</th><th>' + MESSAGES[97] + '</th><th>' + MESSAGES[99] + '</th></tr></thead><tbody>';
    $.each(networks, function (key, value) {
        body += '<tr class="network' + value['id'] + '"><td>' + value['id'] + '</td><td>' + value['name'] + '</td><td>' + value['type'] + '</td><td>' + value['count'] + '</td><td><a class="action-networkedit" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="javascript:void(0)" title="' + MESSAGES[71] + '"><i class="glyphicon glyphicon-edit"></i></a><a class="action-networkdelete" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="javascript:void(0)" title="' + MESSAGES[65] + '"><i class="glyphicon glyphicon-trash"></i></a></td></tr>';
    });
    body += '</tbody></table></div>';

    body = $(body);
    if (ROLE == "user") {
        body.find(".action-networkedit,.action-networkdelete").remove();
    }

    addModalWide(MESSAGES[96], body.html(), '');
}

// check template's options that field's exists
function checkTemplateValue(template_options, field){
    if(template_options[field]){
        return template_options[field].value.toString();
    } else if(!template_options[field] && parseInt(template_options[field]) === 0) {
        return template_options[field].value.toString();
    } else {
        return "";
    }
}

function createNodeListRow(template, id){
    var html_data = "";
    var defer = $.Deferred();

    $.when(getTemplates(template), getNodes(id)).done(function (template_values, node_values) {
        var value_set = "";
        var readonlyAttr = "";
        var value_name      = node_values['name'];
        var value_cpu       = node_values['cpu'] || "n/a";
        var value_idlepc    = node_values['idlepc'] || "n/a";
        var value_nvram     = node_values['nvram'] || "n/a";
        var value_ram       = node_values['ram'] || "n/a";
        var value_ethernet  = node_values['ethernet'] || "n/a";
        var value_console   = checkTemplateValue(template_values,'console') || node_values['console'] || ""
        var value_serial    = "";
        if(node_values['serial']){
            value_serial = node_values['serial'];
        } else if(!node_values['serial'] && parseInt(node_values['serial']) === 0){
            value_serial = node_values['serial'].toString();
        } else{
            value_serial = "n/a";
        }
        
        // TODO: this event is called twice
        id = (id == null) ? '' : id;
        var html_data = '<tr><input name="node[type]" data-path="' + id + '" value="' + template_values['type'] + '" type="hidden"/>';
        html_data += '<input name="node[left]" data-path="' + id + '" value="' + node_values['left'] + '" type="hidden"/>';
        html_data += '<input name="node[top]" data-path="' + id + '" value="' + node_values['top'] + '" type="hidden"/>';

        // node id
        html_data += '<td><input class="hide-border" style="width: 20px;" value="' + id + '" readonly/></td>';
        
        //node name
        html_data += '<td><input class="configured-nodes-input" data-path="' + id + '" name="node[name]" value="' + value_name + '" type="text" /></td>';
        
        //node template
        html_data += '<td><input class="hide-border" data-path="' + id + '" name="node[template]" value="' + template + '" readonly/></td>';

        //node boot image
        if(template == "vpcs"){
            html_data += '<td><input class="configured-nodes-input short-input readonly" data-path="' + id + '" name="node[cpu]" value="n/a" type="text" readonly /></td>';
        } else {
            html_data += '<td><select class="configured-nods-select form-control" data-path="' + id + '" name="node[image]">'
            value_set = (node_values != null && template_values['options']['image'] && template_values['options']['image']['list']) ? node_values['image'] : "";
            var options_arr = template_values['options']['image'] && template_values['options']['image']['list'] ? template_values['options']['image']['list'] : [];
            $.each(options_arr, function (list_key, list_value) {
                var selected = (list_key == value_set) ? 'selected ' : '';
                html_data += '<option ' + selected + 'value="' + list_key + '">' + list_value + '</option>';
            });
            html_data += '</select></td>';
        }

        //node cpu
        readonlyAttr = (value_cpu && value_cpu != "n/a") ? "" : "readonly";
        html_data += '<td><input class="configured-nodes-input short-input ' + readonlyAttr + '" data-path="' + id + '" name="node[cpu]" value="' + value_cpu + '" type="text" ' + readonlyAttr + ' /></td>';

        //node idle
        readonlyAttr = (value_idlepc && value_idlepc != "n/a") ? "" : "readonly";
        html_data += '<td><input class="configured-nodes-input ' + readonlyAttr + '" data-path="' + id + '" name="node[idlepc]" value="' + value_idlepc + '" type="text" ' + readonlyAttr + ' /></td>';

        //node nvram
        readonlyAttr = (value_nvram && value_nvram != "n/a") ? "" : "readonly";
        html_data += '<td><input class="configured-nodes-input short-input ' + readonlyAttr + '" data-path="' + id + '" name="node[nvram]" value="' + value_nvram + '" type="text" ' + readonlyAttr + ' /></td>';

        //node ram
        readonlyAttr = (value_ram && value_ram != "n/a") ? "" : "readonly";
        html_data += '<td><input class="configured-nodes-input short-input ' + readonlyAttr + '" data-path="' + id + '" name="node[ram]" value="' + value_ram + '" type="text" ' + readonlyAttr + ' /></td>';

        //node ethernet
        if(template == "vpcs"){
            readonlyAttr = "readonly";
        } else {
            readonlyAttr = (value_ethernet && value_ethernet != "n/a") ? "" : "readonly";
        }
        html_data += '<td><input class="configured-nodes-input short-input ' + readonlyAttr + '" data-path="' + id + '" name="node[ethernet]" value="' + value_ethernet + '" type="text" ' + readonlyAttr + ' /></td>';

        //node serial
        readonlyAttr = (value_serial && value_serial != "n/a") ? "" : "readonly";
        html_data += '<td><input class="configured-nodes-input short-input ' + readonlyAttr + '" data-path="' + id + '" name="node[serial]" value="' + value_serial + '" type="text" '  + readonlyAttr + '/></td>';

        //node console
        if(template == "iol"){
            html_data += '<td><input class="hide-border"  data-path="' + id + '" value="telnet" readonly/></td>';
        } else if(template_values['options']['console']){
            html_data += '<td><select class="configured-nods-select form-control" name="node[console]" data-path="' + id + '" >'
            value_set = (node_values != null && node_values['console'] != null) ? node_values['console'] : value['value'];
            $.each(template_values['options']['console']['list'], function (list_key, list_value) {
                var selected = (list_key == value_set) ? 'selected ' : '';
                html_data += '<option ' + selected + 'value="' + list_key + '">' + list_value + '</option>';
            });
            html_data += '</select></td>';
        } else {
            html_data += '<td><input class="hide-border" name="node[console]" value="' + value_console + '" type="text" readonly/></td>';
        }

        //node icons
        html_data += '<td><select class="configured-nods-select form-control" data-path="' + id + '" name="node[icon]" >'
        value_set = (node_values != null && node_values['icon'] != null) ? node_values['icon'] : value['value'];
        $.each(template_values['options']['icon']['list'], function (list_key, list_value) {
            var selected = (list_key == value_set) ? 'selected ' : '';
            html_data += '<option ' + selected + 'value="' + list_key + '">' + list_value + '</option>';
        });
        html_data += '</select></td>';

        //node startup-configs
        html_data += '<td><select class="configured-nods-select form-control" data-path="' + id + '" name="node[config]">'
        value_set = (node_values != null && node_values['config'] != null) ? node_values['config'] : value['value'];
        $.each(template_values['options']['config']['list'], function (list_key, list_value) {
            var selected = (list_key == value_set) ? 'selected ' : '';
            html_data += '<option ' + selected + 'value="' + list_key + '">' + list_value + '</option>';
        });
        html_data += '</select></td>';

        //node actions
        html_data += '<td><div class="action-controls">'+
                         '<a class="action-nodestart" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[66] + '"><i class="glyphicon glyphicon-play"></i></a>'+
                         '<a class="action-nodestop" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[67] + '"><i class="glyphicon glyphicon-stop"></i></a>'+
                         '<a class="action-nodewipe" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[68] + '"><i class="glyphicon glyphicon-erase"></i></a>'
        if (ROLE == 'admin' || ROLE == 'editor') {
            html_data += '<a class="action-nodeexport" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[69] + '"><i class="glyphicon glyphicon-save"></i></a> '+
                         '<a class="action-nodeinterfaces" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[72] + '"><i class="glyphicon glyphicon-transfer"></i></a>'+
                         '<a class="action-nodeedit" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[71] + '"><i class="glyphicon glyphicon-edit"></i></a>'+
                         '<a class="action-nodedelete" data-path="' + id + '" data-name="' + checkTemplateValue(template_values['options'],'name') + '" href="javascript:void(0)" title="' + MESSAGES[65] + '"><i class="glyphicon glyphicon-trash"></i></a>';
        } 
        html_data += '</div></td></tr>';
        defer.resolve({"html": html_data, "id": id});
    }).fail(function (message1, message2) {
        // Cannot get data
        if (message1 != null) {
            addModalError(message1);
        } else {
            addModalError(message2)
        }
        // return html_data;
        defer.resolve({"html": html_data, "id": id});
    });

    return defer;
}

// Display all nodes in a table
function printListNodes(nodes) {
    logger(1, 'DEBUG: printing node list');
    var body = '<div class="table-responsive"><form id="form-node-edit-table" ><table class="configured-nodes table"><thead><tr><th>' + MESSAGES[92] + '</th><th>' + MESSAGES[19] + '</th><th>' + MESSAGES[111] + '</th><th>' + MESSAGES[163] + '</th><th>' + MESSAGES[105] + '</th><th>' + MESSAGES[106] + '</th><th>' + MESSAGES[107] + '</th><th>' + MESSAGES[108] + '</th><th>' + MESSAGES[109] + '</th><th>' + MESSAGES[110] + '</th><th>' + MESSAGES[112] + '</th><th>' + MESSAGES[164] + '</th><th>' + MESSAGES[123] + '</th><th>' + MESSAGES[99] + '</th></tr></thead><tbody>';
    var html_rows = [];
    var promises = [];

    var composePromise = function (key, value) {
        var defer = $.Deferred();
        var cpu = (value['cpu'] != null) ? value['cpu'] : '';
        var ethernet = (value['ethernet'] != null) ? value['ethernet'] : '';
        var idlepc = (value['idlepc'] != null) ? value['idlepc'] : '';
        var image = (value['image'] != null) ? value['image'] : '';
        var nvram = (value['nvram'] != null) ? value['nvram'] : '';
        var serial = (value['serial'] != null) ? value['serial'] : '';

        $.when(createNodeListRow(value['template'], value['id'])).done(function (data) {
            html_rows.push(data);
            
            defer.resolve();
        });
        return defer;
    };

    $.each(nodes, function (key, value) {
        promises.push(composePromise(key, value));
    })

    $.when.apply($, promises).done(function () {
        var html_data = html_rows.sort(function(a, b){
            return (a.id < b.id) ? -1 : (a.id > b.id) ? 1 : 0
        })
        $.each(html_data, function(key, value){
            body += value.html;
        });
        body += '</tbody></table></form></div>';
        $("#nodelist-loader").remove();
        addModalWide(MESSAGES[118], body, '');
        $('.selectpicker').selectpicker();
    })
}

// Display all text objects in a table
function printListTextobjects(textobjects) {
    logger(1, 'DEBUG: printing text objects list');
    var text
        , body = '<div class="table-responsive">' +
            '<table class="table">' +
            '<thead>' +
            '<tr>' +
            '<th>' + MESSAGES[92] + '</th>' +
            '<th>' + MESSAGES[19] + '</th>' +
            '<th>' + MESSAGES[95] + '</th>' +
            '<th style="width:69%">' + MESSAGES[146] + '</th>' +
            '<th style="width:9%">' + MESSAGES[99] + '</th>' +
            '</tr>' +
            '</thead>' +
            '<tbody>'
        ;

    $.each(textobjects, function (key, value) {
        if (value['type'] == 'text') {
            text = $('#customText' + value['id'] + ' p').html();
        } else {
            text = ''
        }

        body +=
            '<tr class="textObject' + value['id'] + '">' +
            '<td>' + value['id'] + '</td>' +
            '<td>' + value['name'] + '</td>' +
            '<td>' + value['type'] + '</td>' +
            '<td>' + text + '</td>' +
            '<td>';
        if (ROLE != "user") {
             body += '<a class="action-textobjectdelete" data-path="' + value['id'] + '" data-name="' + value['name'] + '" href="javascript:void(0)" title="' + MESSAGES[65] + '">' +
                '<i class="glyphicon glyphicon-trash" style="margin-left:20px;"></i>' +
                '</a>'
        }
        body += '</td>' +
            '</tr>';
    });
    body += '</tbody></table></div>';
    addModalWide(MESSAGES[150], body, '');
}

// Print Authentication Page
function printPageAuthentication() {
    var html = new EJS({url: '/themes/default/ejs/login.ejs'}).render()
    $('#body').html(html);
    $("#form-login input:eq(0)").focus();
    bodyAddClass('login');
}

// Print lab list page
function printPageLabList(folder) {
    var html = '';
    var url = '/api/folders' + folder;
    var type = 'GET';
    FOLDER = folder;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            // Clear the message container
            $("#notification_container").empty()
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: folder "' + folder + '" found.');

                html = new EJS({url: '/themes/default/ejs/layout.ejs'}).render({
                    "MESSAGES": MESSAGES,
                    "folder": folder,
                    "username": USERNAME,
                    "role": ROLE
                })
                $("#alert_container").remove();

                // Adding to the page
                $('#body').html(html);

                // Adding all folders
                $.each(data['data']['folders'], function (id, object) {
                    $('#list-folders > ul').append('<li><a class="folder action-folderopen" data-path="' + object['path'] + '" href="javascript:void(0)" title="Double click to open, single click to select.">' + object['name'] + '</a></li>');
                });

                // Adding all labs
                $.each(data['data']['labs'], function (id, object) {
                    $('#list-labs > ul').append('<li><a class="lab action-labpreview" data-path="' + object['path'] + '" href="javascript:void(0)" title="Double click to open, single click to select.">' + object['file'] + '</a></li>');
                });



                // Read privileges and set specific actions/elements
                if (ROLE == 'admin' || ROLE == 'editor') {
                    // Adding actions
                    $('#actions-menu').empty();
                    $('#actions-menu').append('<li><a class="action-folderadd" href="javascript:void(0)"><i class="glyphicon glyphicon-folder-close"></i> ' + MESSAGES[4] + '</a></li>');
                    $('#actions-menu').append('<li><a class="action-labadd" href="javascript:void(0)"><i class="glyphicon glyphicon-file"></i> ' + MESSAGES[5] + '</a></li>');
                    $('#actions-menu').append('<li><a class="action-selectedclone" href="javascript:void(0)"><i class="glyphicon glyphicon-copy"></i> ' + MESSAGES[6] + '</a></li>');
                    $('#actions-menu').append('<li><a class="action-selectedexport" href="javascript:void(0)"><i class="glyphicon glyphicon-export"></i> ' + MESSAGES[8] + '</a></li>');
                    $('#actions-menu').append('<li><a class="action-import" href="javascript:void(0)"><i class="glyphicon glyphicon-import"></i> ' + MESSAGES[9] + '</a></li>');
                    $('#actions-menu').append('<li><a class="action-folderrename" href="javascript:void(0)"><i class="glyphicon glyphicon-pencil"></i> ' + MESSAGES[10] + '</a></li>');
                    $('#actions-menu').append('<li><a class="action-selecteddelete" href="javascript:void(0)"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[7] + '</a></li>');

                    // Make labs draggable (to move inside folders)
                    $('.lab').draggable({
                        appendTo: '#body',
                        helper: 'clone',
                        revert: 'invalid',
                        scroll: false,
                        snap: '.folder',
                        stack: '.folder'
                    });

                    // Make folders draggable (to move inside folders)
                    $('.folder').draggable({
                        appendTo: '#body',
                        helper: 'clone',
                        revert: 'invalid',
                        scroll: false,
                        snap: '.folder',
                        stack: '.folder'
                    });

                    // Make folders draggable (to receive labs and folders)
                    $('.folder').droppable({
                        drop: function (e, o) {
                            var object = o['draggable'].attr('data-path');
                            var path = $(this).attr('data-path');
                            logger(1, 'DEBUG: moving "' + object + '" to "' + path + '".');
                            if (o['draggable'].hasClass('lab')) {
                                $.when(moveLab(object, path)).done(function (data) {
                                    logger(1, 'DEBUG: "' + object + '" moved to "' + path + '".');
                                    o['draggable'].fadeOut(300, function () {
                                        o['draggable'].remove();
                                    })
                                }).fail(function (data) {
                                    logger(1, 'DEBUG: failed to move "' + object + '" into "' + path + '".');
                                    addModal('ERROR', '<p>' + data + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
                                });
                            } else if (o['draggable'].hasClass('folder')) {
                                $.when(moveFolder(object, path)).done(function (data) {
                                    logger(1, 'DEBUG: "' + object + '" moved to "' + path + '".');
                                    o['draggable'].fadeOut(300, function () {
                                        o['draggable'].remove();
                                    })
                                }).fail(function (data) {
                                    logger(1, 'DEBUG: failed to move "' + object + '" into "' + path + '".');
                                    addModal('ERROR', '<p>' + data + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
                                });
                            } else {
                                // Should not be here
                                logger(1, 'DEBUG: cannot move unknown object.');
                            }

                        }
                    });
                } else {
                    $('#actions-menu').empty();
                    $('#actions-menu').append('<li><a href="javascript:void()">&lt;' + MESSAGES[3] + '&gt;</a></li>');
                }
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                addModal('ERROR', '<p>' + data['message'] + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
            }

            bodyAddClass('folders');
            // Extend height to the bottom if shorter
            autoheight();
            
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            addModal('ERROR', '<p>' + message + '</p>', '<button type="button" class="btn btn-aqua" data-dismiss="modal">Close</button>');
        }
    });
}

// Print lab open page
function printPageLabOpen(lab) {
    var html = '<div id="lab-sidebar"><ul></ul></div><div id="lab-viewport" data-path="' + lab + '"></div>';

    $('#body').html(html);

    // Print topology
    printLabTopology();

    // Read privileges and set specific actions/elements
    if (ROLE == 'admin' || ROLE == 'editor') {
        $('#lab-sidebar ul').append('<li><a class="action-labobjectadd" href="javascript:void(0)" title="' + MESSAGES[56] + '"><i class="glyphicon glyphicon-plus"></i></a></li>');
        $('#lab-sidebar ul').append('<li><a class="action-nodelink" href="javascript:void(0)" title="' + MESSAGES[115] + '"><i class="glyphicon glyphicon-link"></i></a></li>');
    }

    $('#lab-sidebar ul').append('<li><a class="action-nodesget" href="javascript:void(0)" title="' + MESSAGES[62] + '"><i class="glyphicon glyphicon-hdd"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-networksget" href="javascript:void(0)" title="' + MESSAGES[61] + '"><i class="glyphicon glyphicon-transfer"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-configsget" href="javascript:void(0)" title="' + MESSAGES[58] + '"><i class="glyphicon glyphicon-align-left"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-picturesget" href="javascript:void(0)" title="' + MESSAGES[59] + '"><i class="glyphicon glyphicon-picture"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-textobjectsget" href="javascript:void(0)" title="' + MESSAGES[150] + '"><i class="glyphicon glyphicon-text-background"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-moreactions" href="javascript:void(0)" title="' + MESSAGES[125] + '"><i class="glyphicon glyphicon-th"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-labtopologyrefresh" href="javascript:void(0)" title="' + MESSAGES[57] + '"><i class="glyphicon glyphicon-refresh"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-freeselect" href="javascript:void(0)" title="' + MESSAGES[151] + '"><i class="glyphicon glyphicon-check"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-status" href="javascript:void(0)" title="' + MESSAGES[13] + '"><i class="glyphicon glyphicon-info-sign"></i></a></li>');
    $('#lab-sidebar ul').append('<li><a class="action-labbodyget" href="javascript:void(0)" title="' + MESSAGES[64] + '"><i class="glyphicon glyphicon-list-alt"></i></a></li>');
    $('#lab-sidebar ul').append('<div id="action-labclose"><li><a class="action-labclose" href="javascript:void(0)" title="' + MESSAGES[60] + '"><i class="glyphicon glyphicon-off"></i></a></li></div>');
    $('#lab-sidebar ul').append('<li><a class="action-logout" href="javascript:void(0)" title="' + MESSAGES[14] + '"><i class="glyphicon glyphicon-log-out"></i></a></li>');
    $('#lab-sidebar ul a').each(function () {
        var t = $(this).attr("title");
        $(this).append(t);


    })
}

// Print user management section
function printUserManagement() {
    $.when(getUsers(null)).done(function (data) {
        var html = '<div class="row"><div id="users" class="col-md-12 col-lg-12"><div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[44] + '</th><th>' + MESSAGES[19] + '</th><th>' + MESSAGES[28] + '</th><th>' + MESSAGES[29] + '</th><th>' + MESSAGES[30] + '</th><th>' + MESSAGES[31] + '</th><th>' + MESSAGES[32] + '</th></tr></thead><tbody></tbody></table></div></div></div>';
        html += '<div class="row"><div id="pods" class="col-md-12 col-lg-12"><div class="table-responsive"><table class="table"><thead><tr><th>' + MESSAGES[44] + '</th><th>' + MESSAGES[32] + '</th><th>' + MESSAGES[33] + '</th><th>' + MESSAGES[63] + '</th></tr></thead><tbody></tbody></table></div></div></div>';

        var html_title = '' +
            '<div class="row row-eq-height"><div id="list-title-folders" class="col-md-12 col-lg-12">' +
            '<span title="Users">Users</span>' +
            '</div>' +
            '</div>';
        $('#main-title').html(html_title);
        $('#main-title').show();
        $('#main').html(html);

        // Read privileges and set specific actions/elements
        if (ROLE == 'admin') {
            // Adding actions
            $('#actions-menu').empty();
            $('#actions-menu').append('<li><a class="action-useradd" href="javascript:void(0)"><i class="glyphicon glyphicon-plus"></i> ' + MESSAGES[34] + '</a></li>');
            $('#actions-menu').append('<li><a class="action-selecteddelete" href="javascript:void(0)"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[35] + '</a></li>');
        } else {
            $('#actions-menu').empty();
            $('#actions-menu').append('<li><a href="javascript:void()">&lt;' + MESSAGES[3] + '&gt;</a></li>');
        }

        // Adding all users
        $.each(data, function (id, object) {
            var username = object['username'];
            var name = object['name'];
            var email = object['email'];
            var role = object['role'];
            if (object['lab'] == null) {
                var lab = 'none';
            } else {
                var lab = object['lab'];
            }
            if (object['pod'] == -1) {
                var pod = 'none';
            } else {
                var pod = object['pod'];
            }
            if (object['expiration'] <= 0) {
                var expiration = MESSAGES[54];
            } else {
                var d = new Date(object['expiration'] * 1000);
                expiration = d.toLocaleDateString();
            }
            if (object['session'] <= 0) {
                var session = MESSAGES[53];
            } else {
                var d = new Date(object['session'] * 1000);
                session = d.toLocaleDateString() + ' ' + d.toLocaleTimeString() + ' from ' + object['ip'];
            }
            if (object['pexpiration'] <= 0) {
                var pexpiration = MESSAGES[54];
            } else {
                var d = new Date(object['pexpiration'] * 1000);
                pexpiration = d.toLocaleDateString();
            }
            $('#users tbody').append('<tr class="action-useredit user" data-path="' + username + '"><td class="username">' + username + '</td><td class="class="name">' + name + '</td><td class="email">' + email + '</td><td class="role">' + role + '</td><td class="expiration">' + expiration + '</td><td class="session">' + session + '</td><td class="pod">' + pod + '</td></tr>');
            if (object['pod'] >= 0) {
                $('#pods tbody').append('<tr class="action-useredit user" data-path="' + username + '"><td class="username">' + username + '</td><td class="pod">' + pod + '</td><td class="pexpiration">' + pexpiration + '</td><td class="">' + lab + '</td></tr>');
            }

            bodyAddClass('users');
        });
    }).fail(function (message) {
        addModalError(message);
    });
}

// Print system status in modal
function drawStatusInModal(data) {
    var $statusModalBody = $("#statusModal");

    if (!$statusModalBody.length) {
        return void 0;
    }

    // Read privileges and set specific actions/elements
    $('#actions-menu', $statusModalBody).empty();
    $('#actions-menu', $statusModalBody).append('<li><a class="action-sysstatus" href="javascript:void(0)"><i class="glyphicon glyphicon-refresh"></i> ' + MESSAGES[40] + '</a></li>');
    $('#actions-menu', $statusModalBody).append('<li><a class="action-stopall" href="javascript:void(0)"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[50] + '</a></li>');
    //$('#actions-menu', $statusModalBody).append('<li><a class="action-update" href="javascript:void(0)"><i class="glyphicon glyphicon-repeat"></i> ' + MESSAGES[132] + '</a></li>');

    // Adding all stats

    // Text
    $('#stats-text ul', $statusModalBody).empty();
    $('#stats-text ul', $statusModalBody).append('<li>' + MESSAGES[39] + ': <code>' + data['version'] + '</code></li>');
    $('#stats-text ul', $statusModalBody).append('<li>' + MESSAGES[49] + ': <code>' + data['qemu_version'] + '</code></li>');
    $('#stats-text ul', $statusModalBody).append('<li>' + MESSAGES[29] + ': <code>' + ROLE + '</code></li>');
    $('#stats-text ul', $statusModalBody).append('<li>' + MESSAGES[32] + ': <code>' + ((TENANT == -1) ? 'none' : TENANT) + '</code></li>');

    // use graphs
    $('#stats-graph ul', $statusModalBody).empty();

    // CPU usage
    $('#stats-graph ul', $statusModalBody).append('<li><div class="circle circle-cpu col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[36] + '</span></div></li>');
    $('.circle-cpu').circleProgress({
        arcCoef: 0.7,
        value: data['cpu'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['cpu']) {
            $(this).find('strong').html(parseInt(100 * data['cpu']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // Memory usage
    $('#stats-graph ul', $statusModalBody).append('<li><div class="circle circle-memory col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[37] + '</span></div></li>');
    $('.circle-memory').circleProgress({
        arcCoef: 0.7,
        value: data['mem'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['mem']) {
            $(this).find('strong').html(parseInt(100 * data['mem']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // Swap usage
    $('#stats-graph ul', $statusModalBody).append('<li><div class="circle circle-swap col-md-3 col-lg-3"><strong></strong><br/><span>Swap usage</span></div></li>');
    $('.circle-swap').circleProgress({
        arcCoef: 0.7,
        value: data['swap'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['swap']) {
            $(this).find('strong').html(parseInt(100 * data['swap']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // Disk usage
    $('#stats-graph ul', $statusModalBody).append('<li><div class="circle circle-disk col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[38] + '</span></div></li>');
    $('.circle-disk').circleProgress({
        arcCoef: 0.7,
        value: data['disk'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['disk']) {
            $(this).find('strong').html(parseInt(100 * data['disk']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // IOL running nodes
    $('#stats-graph ul', $statusModalBody).append('<li><div class="count count-iol col-md-4 col-lg-4"></div>');
    $('.count-iol', $statusModalBody).html('<strong>' + data['iol'] + '</strong><br/><span>' + MESSAGES[41] + '</span></li>');

    // Dynamips running nodes
    $('#stats-graph ul', $statusModalBody).append('<li><div class="count count-dynamips col-md-4 col-lg-4"></div></li>');
    $('.count-dynamips', $statusModalBody).html('<strong>' + data['dynamips'] + '</strong><br/><span>' + MESSAGES[42] + '</span>');

    // QEMU running nodes
    $('#stats-graph ul', $statusModalBody).append('<li><div class="count count-qemu col-md-4 col-lg-4"></div></li>');
    $('.count-qemu', $statusModalBody).html('<strong>' + data['qemu'] + '</strong><br/><span>' + MESSAGES[43] + '</span>');

    // Docker running nodes
    $('#stats-graph ul', $statusModalBody).append('<li><div class="count count-docker col-md-4 col-lg-6"></div></li>');
    $('.count-docker', $statusModalBody).html('<strong>' + data['docker'] + '</strong><br/><span>' + MESSAGES[161] + '</span>');

    // VPCS running nodes
    $('#stats-graph ul', $statusModalBody).append('<li><div class="count count-vpcs col-md-4 col-lg-6"></div></li>');
    $('.count-vpcs', $statusModalBody).html('<strong>' + data['vpcs'] + '</strong><br/><span>' + MESSAGES[162] + '</span>');
}

// Update system status in modal
function updateStatusInModal(intervalId, data) {
    if (!intervalId) {
        return null;
    }

    if (!$("#statusModal").length) {
        return clearInterval(intervalId);
    }

    drawStatusInModal(data);
}

// Update system status
function updateStatus(intervalId, data) {
    if (!intervalId) {
        return null;
    }

    if (!$("#systemStats").length) {
        return clearInterval(intervalId);
    }

    printSystemStats(data);
}

// Print system status
function printSystemStats(data) {
    var $statusBody = $("#systemStats");

    if (!$statusBody.length) {
        return void 0;
    }
    // Read privileges and set specific actions/elements
    $('#actions-menu').empty();
    $('#actions-menu').append('<li><a class="action-sysstatus" href="javascript:void(0)"><i class="glyphicon glyphicon-refresh"></i> ' + MESSAGES[40] + '</a></li>');
    $('#actions-menu').append('<li><a class="action-stopall" href="javascript:void(0)"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[50] + '</a></li>');
    //$('#actions-menu').append('<li><a class="action-update" href="javascript:void(0)"><i class="glyphicon glyphicon-repeat"></i> ' + MESSAGES[132] + '</a></li>');

    // Adding all stats

    // Text
    $('#stats-text ul').empty();
    $('#stats-text ul').append('<li>' + MESSAGES[39] + ': <code>' + data['version'] + '</code></li>');
    $('#stats-text ul').append('<li>' + MESSAGES[49] + ': <code>' + data['qemu_version'] + '</code></li>');
    $('#stats-text ul').append('<li>' + MESSAGES[29] + ': <code>' + ROLE + '</code></li>');
    $('#stats-text ul').append('<li>' + MESSAGES[32] + ': <code>' + ((TENANT == -1) ? 'none' : TENANT) + '</code></li>');

    $('#stats-graph ul').empty();

    // CPU usage
    $('#stats-graph ul').append('<li><div class="circle circle-cpu col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[36] + '</span></div></li>');
    $('.circle-cpu').circleProgress({
        arcCoef: 0.7,
        value: data['cpu'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['cpu']) {
            $(this).find('strong').html(parseInt(100 * data['cpu']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // Memory usage
    $('#stats-graph ul').append('<li><div class="circle circle-memory col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[37] + '</span></div></li>');
    $('.circle-memory').circleProgress({
        arcCoef: 0.7,
        value: data['mem'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['mem']) {
            $(this).find('strong').html(parseInt(100 * data['mem']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // Swap usage
    $('#stats-graph ul').append('<li><div class="circle circle-swap col-md-3 col-lg-3"><strong></strong><br/><span>Swap usage</span></div></li>');
    $('.circle-swap').circleProgress({
        arcCoef: 0.7,
        value: data['swap'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['swap']) {
            $(this).find('strong').html(parseInt(100 * data['swap']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // Disk usage
    $('#stats-graph ul').append('<li><div class="circle circle-disk col-md-3 col-lg-3"><strong></strong><br/><span>' + MESSAGES[38] + '</span></div></li>');
    $('.circle-disk').circleProgress({
        arcCoef: 0.7,
        value: data['disk'],
        thickness: 10,
        startAngle: -Math.PI / 2,
        fill: {gradient: ['#46a6b6']}
    }).on('circle-animation-progress', function (event, progress) {
        if (progress > data['disk']) {
            $(this).find('strong').html(parseInt(100 * data['disk']) + '%');
        } else {
            $(this).find('strong').html(parseInt(100 * progress) + '%');
        }
    });

    // IOL running nodes
    $('#stats-graph ul').append('<li><div class="count count-iol col-md-4 col-lg-4"></div>');
    $('.count-iol').html('<strong>' + data['iol'] + '</strong><br/><span>' + MESSAGES[41] + '</span></li>');

    // Dynamips running nodes
    $('#stats-graph ul').append('<li><div class="count count-dynamips col-md-4 col-lg-4"></div></li>');
    $('.count-dynamips').html('<strong>' + data['dynamips'] + '</strong><br/><span>' + MESSAGES[42] + '</span>');

    // QEMU running nodes
    $('#stats-graph ul').append('<li><div class="count count-qemu col-md-4 col-lg-4"></div></li>');
    $('.count-qemu').html('<strong>' + data['qemu'] + '</strong><br/><span>' + MESSAGES[43] + '</span>');

    // Docker running nodes
    $('#stats-graph ul').append('<li><div class="count count-docker col-md-4 col-lg-6"></div></li>');
    $('.count-docker').html('<strong>' + data['docker'] + '</strong><br/><span>' + MESSAGES[161] + '</span>');

    // VPCS running nodes
    $('#stats-graph ul').append('<li><div class="count count-vpcs col-md-4 col-lg-6"></div></li>');
    $('.count-vpcs').html('<strong>' + data['vpcs'] + '</strong><br/><span>' + MESSAGES[162] + '</span>');

}

/*******************************************************************************
 * Custom Shape Functions
 * *****************************************************************************/
// Get All Text Objects
function getTextObjects() {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/textobjects';
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got shape(s) from lab "' + lab_filename + '".');
                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Get Text Object By Id
function getTextObject(id) {
    var deferred = $.Deferred();
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/textobjects/' + id;
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: got shape ' + id + 'from lab "' + lab_filename + '".');

                try {
                    data['data'].data = new TextDecoderLite('utf-8').decode(toByteArray(data['data'].data));
                }
                catch (e) {
                    console.warn("Compatibility issue", e);
                }

                deferred.resolve(data['data']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Create New Text Object
function createTextObject(newData) {
    var deferred = $.Deferred()
        , lab_filename = $('#lab-viewport').attr('data-path')
        , url = '/api/labs' + lab_filename + '/textobjects'
        , type = 'POST';

    if (newData.data) {
        newData.data = fromByteArray(new TextEncoderLite('utf-8').encode(newData.data));
    }

    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        data: JSON.stringify(newData),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: create shape ' + 'for lab "' + lab_filename + '".');
                deferred.resolve(data['result']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });

    return deferred.promise();
}

// Update Text Object
function editTextObject(id, newData) {
    var lab_filename = $('#lab-viewport').attr('data-path');
    var deferred = $.Deferred();
    var type = 'PUT';
    var url = '/api/labs' + lab_filename + '/textobjects/' + id;

    if (newData.data) {
        newData.data = fromByteArray(new TextEncoderLite('utf-8').encode(newData.data));
    }

    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(newData), // newData is object with differences between old and new data
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: custom shape text object updated.');
                deferred.resolve(data['message']);
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Delete Text Object By Id
function deleteTextObject(id) {
    var deferred = $.Deferred();
    var type = 'DELETE';
    var lab_filename = $('#lab-viewport').attr('data-path');
    var url = '/api/labs' + lab_filename + '/textobjects/' + id;
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: shape/text deleted.');
                deferred.resolve();
            } else {
                // Application error
                logger(1, 'DEBUG: application error (' + data['status'] + ') on ' + type + ' ' + url + ' (' + data['message'] + ').');
                deferred.reject(data['message']);
            }
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

// Text Object Drag Stop / Resize Stop
function textObjectDragStop(event, ui) {
    var id
        , objectData
        , shape_border_width
        ;
    if (event.target.id.indexOf("customShape") != -1) {
        id = event.target.id.slice("customShape".length);
        shape_border_width = $("#customShape" + id + " svg").children().attr('stroke-width');
    }
    else if (event.target.id.indexOf("customText") != -1) {
        id = event.target.id.slice("customText".length);
        shape_border_width = 5;
    }

    objectData = event.target.outerHTML;

    editTextObject(id, {
        data: objectData
    });
}

// Text Object Resize Event
function textObjectResize(event, ui, shape_options) {
    var newWidth = ui.size.width
        , newHeight = ui.size.height
        ;

    $("svg", ui.element).attr({
        width: newWidth,
        height: newHeight
    });
    $("svg > rect", ui.element).attr({
        width: newWidth,
        height: newHeight
    });
    $("svg > ellipse", ui.element).attr({
        rx: newWidth / 2 - shape_options['shape_border_width'] / 2,
        ry: newHeight / 2 - shape_options['shape_border_width'] / 2,
        cx: newWidth / 2,
        cy: newHeight / 2
    });
    var n = $("br", ui.element).size();
    if (n) {
        $("p", ui.element).css({
            "font-size": newHeight / (n * 1.5 + 1)
        });
    } else {
        $("p", ui.element).css({
            "font-size": newHeight / 2
        });
    }
    if ($("p", ui.element).length && $(ui.element).width() > newWidth) {
        ui.size.width = $(ui.element).width();
    }
}

// Edit Form: Custom Shape
function printFormEditCustomShape(id) {
    $('.edit-custom-shape-form').remove();
    $('.edit-custom-text-form').remove();
    $('.customShape').each(function (index) {
        $(this).removeClass('in-editing');
    });
    getTextObject(id).done(function(res){
        var borderTypes = ['solid', 'dashed']
        , firstShapeValues = {}
        , shape
        , transparent = false
        , colorDigits
        , bgColor
        , html =
        '<form id="main-modal-edit" class="container col-md-12 col-lg-12 edit-custom-shape-form" data-path="' + id + '">' +
            '<div class="row col-md-9 top-part">' +
            '<label class="edit-custom-shape-label">Edit: ' + id + '</label><br>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Z-Index</label>' +
            '<input type="number" class="form-control shape-z_index-input"  min="-100" max="100" step="1" data-path="' + id + '">' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Border-width</label>' +
            '<input type="number" class="form-control shape_border_width" min="0" data-path="' + id + '">' +
            '</div>' +
            '<div class="form-group">' +
            '<label class=" control-label form-group-addon">Border-type</label>' +
            '<select class="form-control border-type-select" data-path="' + id + '">' +
            '</select>' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Border-color</label>' +
            '<input type="color" class="form-control shape_border_color" data-path="' + id + '">' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Background-color</label> ' +
            '<input type="color" class="form-control shape_background_color" data-path="' + id + '">' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Transparent</label> ' +
            '<button type="button" class="btn btn-default shape_background_transparent" data-path="' + id + '"></button>' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Rotate</label>' +
            '<input type="number" class="form-control shape-rotation-input" data-path="' + id + '" min="-360" max="360" step="1">' +
            '</div>' +
            '<div class="form-group">' +
            '<label class="control-label form-group-addon">Name</label>' +
            '<input type="text" class="form-control shape-name-input" data-path="' + id + '" >' +
            '</div>' +
            '</div>' +
            '<div class="row col-md-3 btn-part">' +
            '<button type="button" class="btn btn-aqua edit-custom-shape-form-save" data-path="' + id + '">' + MESSAGES[47] + '</button>' +
            '<button type="button" class="btn btn-grey cancelForm" data-path="' + id + '">' + MESSAGES[18] + '</button>' +
            '</div>' +
            '<input type="hidden" class="firstShapeValues-z_index">' +
            '<input type="hidden" class="firstShapeValues-border-color">' +
            '<input type="hidden" class="firstShapeValues-background-color">' +
            '<input type="hidden" class="firstShapeValues-border-type">' +
            '<input type="hidden" class="firstShapeValues-border-width">' +
            '<input type="hidden" class="firstShapeValues-rotation">' +
            '</form>';

        $('#lab-viewport').append(html);

        for (var i = 0; i < borderTypes.length; i++) {
            $('.edit-custom-shape-form .border-type-select').append($('<option></option>').val(borderTypes[i]).html(borderTypes[i]));
        }

        if ($("#customShape" + id + " svg").children().attr('stroke-dasharray')) {
            $('.edit-custom-shape-form .border-type-select').val(borderTypes[1]);
            firstShapeValues['border-types'] = borderTypes[1];
        } else {
            $('.edit-custom-shape-form .border-type-select').val(borderTypes[0]);
            firstShapeValues['border-types'] = borderTypes[0];
        }

        bgColor = $("#customShape" + id + " svg").children().attr('fill');
        colorDigits = /(.*?)rgba{0,1}\((\d+), (\d+), (\d+)\)/.exec(bgColor);
        if (colorDigits === null) {
            var ifHex = bgColor.indexOf('#');
            if (ifHex < 0) {
                transparent = true;
            }
        }

        if (transparent) {
            $('.edit-custom-shape-form .shape_background_transparent').addClass('active  btn-success').text('On');
        } else {
            $('.edit-custom-shape-form .shape_background_transparent').removeClass('active  btn-success').text('Off');
        }

        firstShapeValues['shape-name'] = res.name;
        firstShapeValues['shape-z-index'] = $('#customShape' + id).css('z-index');
        firstShapeValues['shape-background-color'] = rgb2hex($("#customShape" + id + " svg").children().attr('fill'));
        firstShapeValues['shape-border-color'] = rgb2hex($("#customShape" + id + " svg ").children().attr('stroke'));
        firstShapeValues['shape-border-width'] = $("#customShape" + id + " svg").children().attr('stroke-width');
        firstShapeValues['shape-rotation'] = getElementsAngle("#customShape" + id);
        // $("#customShape" + id ).attr('name');

        // fill inputs
        $('.edit-custom-shape-form .shape-z_index-input').val(firstShapeValues['shape-z-index'] - 1000);
        $('.edit-custom-shape-form .shape_background_color').val(firstShapeValues['shape-background-color']);
        $('.edit-custom-shape-form .shape_border_color').val(firstShapeValues['shape-border-color']);
        $('.edit-custom-shape-form .shape_border_width').val(firstShapeValues['shape-border-width']);
        $('.edit-custom-shape-form .shape-rotation-input').val(firstShapeValues['shape-rotation']);
        $('.edit-custom-shape-form .shape-name-input').val(firstShapeValues['shape-name']);

        // fill backup
        $('.edit-custom-shape-form .firstShapeValues-z_index').val(firstShapeValues['shape-z-index']);
        $('.edit-custom-shape-form .firstShapeValues-border-color').val(firstShapeValues['shape-border-color']);
        $('.edit-custom-shape-form .firstShapeValues-background-color').val(firstShapeValues['shape-background-color']);
        $('.edit-custom-shape-form .firstShapeValues-border-type').val(firstShapeValues['border-types']);
        $('.edit-custom-shape-form .firstShapeValues-border-width').val(firstShapeValues['shape-border-width']);
        $('.edit-custom-shape-form .firstShapeValues-rotation').val(firstShapeValues['shape-rotation']);

        if ($("#customShape" + id + " svg").children().attr('cx')) {
            $('.edit-custom-shape-form .shape_border_width').val(firstShapeValues['shape-border-width'] * 2);
            $('.edit-custom-shape-form .firstShapeValues-border-width').val(firstShapeValues['shape-border-width'] * 2);
        }
        $("#customShape" + id).addClass('in-editing');
    });
    
}

// Edit Form: Text
function printFormEditText(id) {
    $('.edit-custom-shape-form').remove();
    $('.edit-custom-text-form').remove();
    $('.customShape').each(function (index) {
        $(this).removeClass('in-editing');
    });

    var firstTextValues = {}
        , transparent = false
        , colorDigits
        , bgColor
        , html =
  '<form id="main-modal-edit" class="container col-md-12 col-lg-12 edit-custom-text-form"  data-path="' + id + '">' +
        '<div class="row col-md-9  top-part">' +
        '<label class="edit-custom-text-label">Edit: ' + id + '</label><br>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Z-Index</label>' +
        '<input type="number" class="form-control text-z_index-input" min="-100" max="100" step="1" data-path="' + id + '">' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Text-align</label>' +
        '<div class="btn-group">' +
        '<button type="button" class="btn btn-default btn-align-left" data-path="' + id + '"><i class="glyphicon glyphicon-align-left"></i></button>' +
        '<button type="button" class="btn btn-default btn-align-center" data-path="' + id + '"><i class="glyphicon glyphicon-align-center"></i></button>' +
        '<button type="button" class="btn btn-default btn-align-right" data-path="' + id + '"><i class="glyphicon glyphicon-align-right"></i></button>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Text-type</label>' +
        '<div class="btn-group">' +
        '<button type="button" class="btn btn-default btn-text-bold" data-path="' + id + '"><i class="glyphicon glyphicon-bold"></i></button>' +
        '<button type="button" class="btn btn-default btn-text-italic" data-path="' + id + '"><i class="glyphicon glyphicon-italic"></i></button>' +
        '</div>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Text-color</label>' +
        '<input type="color" class="form-control text_color"  data-path="' + id + '">' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Background-color</label> ' +
        '<input type="color" class="form-control text_background_color"  data-path="' + id + '">' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Transparent</label> ' +
        '<button type="button" class="btn btn-default text_background_transparent" data-path="' + id + '"></button>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Rotate</label>' +
        '<input type="number" class="form-control text-rotation-input"  data-path="' + id + '" min="-360" max="360" step="1">' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label form-group-addon">Name</label>' +
        '<input type="text" class="form-control shape-name-input" data-path="' + id + '">' +
        '</div>' +
        '</div>' +
        '<div class="row col-md-3 btn-part">' +
        '<button type="button" class="btn btn-aqua edit-custom-text-form-save" data-path="' + id + '">' + MESSAGES[47] + '</button>' +
        '<button type="button" class="btn btn-grey cancelForm" data-path="' + id + '">' + MESSAGES[18] + '</button>' +
        '</div>' +
        '<input type="text" class="hide firstTextValues-z_index">' +
        '<input type="text" class="hide firstTextValues-color">' +
        '<input type="text" class="hide firstTextValues-background-color">' +
        '<input type="text" class="hide firstTextValues-italic">' +
        '<input type="text" class="hide firstTextValues-bold">' +
        '<input type="text" class="hide firstTextValues-align">' +
        '<input type="text" class="hide firstTextValues-rotation">' +
        '</form>';

    $('#lab-viewport').append(html);

    bgColor = $("#customText" + id + " p").css('background-color');
    colorDigits = /(.*?)rgba{0,1}\((\d+), (\d+), (\d+)\)/.exec(bgColor);
    if (colorDigits === null) {
        var ifHex = bgColor.indexOf('#');
        if (ifHex < 0) {
            transparent = true;
        }
    }

    if (transparent) {
        $('.edit-custom-text-form .text_background_transparent').addClass('active  btn-success').text('On');
    } else {
        $('.edit-custom-text-form .text_background_transparent').removeClass('active  btn-success').text('Off');
    }

    firstTextValues['text-z-index'] = parseInt($('#customText' + id).css('z-index'));
    firstTextValues['text-color'] = rgb2hex($("#customText" + id + " p").css('color'));
    firstTextValues['text-background-color'] = rgb2hex($("#customText" + id + " p").css('background-color'));
    firstTextValues['text-rotation'] = getElementsAngle("#customText" + id);


    $('.edit-custom-text-form .text-z_index-input').val(parseInt(firstTextValues['text-z-index']) - 1000);
    $('.edit-custom-text-form .text_color').val(firstTextValues['text-color']);
    $('.edit-custom-text-form .text_background_color').val(firstTextValues['text-background-color']);
    $('.edit-custom-text-form .text-rotation-input').val(firstTextValues['text-rotation']);

    if ($("#customText" + id + " p").css('font-style') == 'italic') {
        $('.edit-custom-text-form .btn-text-italic').addClass('active');
        firstTextValues['text-type-italic'] = 'italic'
    }
    if ($("#customText" + id + " p").css('font-weight') == 'bold') {
        $('.edit-custom-text-form .btn-text-bold').addClass('active');
        firstTextValues['text-type-bold'] = 'bold';
    }
    if ($("#customText" + id + " p").attr('align') == 'left') {
        $('.edit-custom-text-form .btn-align-left').addClass('active');
        firstTextValues['text-align'] = 'left';
    } else if ($("#customText" + id + " p").attr('align') == 'center') {
        $('.edit-custom-text-form .btn-align-center').addClass('active');
        firstTextValues['text-align'] = 'center';
    } else if ($("#customText" + id + " p").attr('align') == 'right') {
        $('.edit-custom-text-form .btn-align-right').addClass('active');
        firstTextValues['text-align'] = 'right';
    }

    $('.edit-custom-text-form .firstTextValues-z_index').val(parseInt(firstTextValues['text-z-index']));
    $('.edit-custom-text-form .firstTextValues-color').val(firstTextValues['text-color']);
    $('.edit-custom-text-form .firstTextValues-background-color').val($("#customText" + id + " p").css('background-color'));
    $('.edit-custom-text-form .firstTextValues-italic').val(firstTextValues['text-type-italic']);
    $('.edit-custom-text-form .firstTextValues-bold').val(firstTextValues['text-type-bold']);
    $('.edit-custom-text-form .firstTextValues-align').val(firstTextValues['text-align']);
    $('.edit-custom-text-form .firstTextValues-rotation').val(firstTextValues['text-rotation']);

    $("#customText" + id).addClass('in-editing');
}

// Change from RGB to Hex color
function rgb2hex(color) {
    if (color.substr(0, 1) === '#') {
        return color;
    }
    var digits = /(.*?)rgba{0,1}\((\d+), (\d+), (\d+)\)/.exec(color);

    if (digits == null) {
        digits = /(.*?)rgba\((\d+), (\d+), (\d+), (\d+)\)/.exec(color);
    }

    var red = parseInt(digits[2]);
    var green = parseInt(digits[3]);
    var blue = parseInt(digits[4]);

    var rgb = blue | (green << 8) | (red << 16);
    return digits[1] + '#' + ("000000" + rgb.toString(16)).slice(-6);
}

// Change from Hex to RGB color
function hex2rgb(hex, opacity) {
    hex = hex.replace('#', '');
    var r = parseInt(hex.substring(0, 2), 16);
    var g = parseInt(hex.substring(2, 4), 16);
    var b = parseInt(hex.substring(4, 6), 16);

    return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + opacity + ')';
}

function getElementsAngle(selector) {
    var el = document.querySelector(selector)
        , st = window.getComputedStyle(el, null)
        , tr = st.getPropertyValue("-webkit-transform") ||
        st.getPropertyValue("-moz-transform") ||
        st.getPropertyValue("-ms-transform") ||
        st.getPropertyValue("-o-transform") ||
        st.getPropertyValue("transform") ||
        "FAIL";

    if (tr === "FAIL" || tr === "none") {
        return 0;
    }

    // With rotate(30deg)...
    // matrix(0.866025, 0.5, -0.5, 0.866025, 0px, 0px)
    // rotation matrix - http://en.wikipedia.org/wiki/Rotation_matrix

    var values = tr.split('(')[1].split(')')[0].split(',')
        , a = values[0]
        , b = values[1]
        , c = values[2]
        , d = values[3]
        , scale = Math.sqrt(a * a + b * b)
    // arc sin, convert from radians to degrees, round
        , sin = b / scale
        , angle = Math.round(Math.atan2(b, a) * (180 / Math.PI))
        ;

    return angle;
}

function getLogs(file, per_page, search) {
    var deferred = $.Deferred();
    var url = '/api/logs/' + file + "/" + per_page + "/" + search;
    var type = 'GET';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        success: function (data) {
            var html = new EJS({url: '/themes/default/ejs/logs.ejs'}).render({
                "logs": data,
                "per_page": per_page,
                "search": search,
                "file": file
            });
            $('#main').html(html);

            var html_title = '' +
                '<div class="row row-eq-height"><div id="list-title-folders" class="col-md-12 col-lg-12">' +
                '<span title="Logs">Logs</span>' +
                '</div>' +
                '</div>';
            $('#main-title').html(html_title);
            $('#main-title').show();

            bodyAddClass('logs');
        },
        error: function (data) {
            // Server error
            var message = getJsonMessage(data['responseText']);
            logger(1, 'DEBUG: server error (' + data['status'] + ') on ' + type + ' ' + url + '.');
            logger(1, 'DEBUG: ' + message);
            deferred.reject(message);
        }
    });
    return deferred.promise();
}

function search_log(file) {
    if (file)
        curr_log = file;
    per_page = $("#log_lines").val();
    search = $("#log_search").val();

    getLogs(curr_log, per_page, search);
}

var curr_log = "";
// Print user management section
function printLogs(file, per_page, search) {
    curr_log = file;
    $('#actions-menu').empty();
    $('#actions-menu').append('<li><a href="#" onclick="search_log(); return false"><i class="glyphicon glyphicon-refresh"></i> Refresh</a></li>');

    $.when(getLogs(file, per_page, search)).done(function (data) {

    }).fail(function (message) {
        addModalError(message);
    });
}

/**
 * add class to body
 */
function bodyAddClass(cl){
    $('body').attr('class',cl);
}

/**
 *
 */
function autoheight()
{
    if ($('#main').height() < window.innerHeight - $('#main').offset().top) {
        $('#main').height(function(index, height) {
            return window.innerHeight - $(this).offset().top;
        });
    }
}
