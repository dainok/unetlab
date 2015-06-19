// Base64 encode/decode
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

// Get GET parameter
function getParameter(s) {
    s = s.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + s + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// Alert management
function raiseMessage(severity, message) {
    // Severity can be success (green), info (blue), warning (yellow) and danger (red)
    $('<div class="alert alert-' + severity.toLowerCase() + '">' + message + '</div>').prependTo('#msg_frame').fadeTo(10000, 500).slideUp(500, function() {
        $(this).alert('close');
    });
}

// Alert management
function raisePermanentMessage(severity, message) {
    // Severity can be success (green), info (blue), warning (yellow) and danger (red)
    $('<div class="alert alert-' + severity.toLowerCase() + '">' + message + '</div>').prependTo('#msg_frame').fadeTo(2000, 500);
}

// Translate MAP
function  translateMap(picture_map) {
    var map = picture_map;
    map = map.replace(/{{IP}}/g, location.hostname);
    map = map.replace(/{{NODE[0-9]+}}/g, function(e) { return parseInt(e.substr(6, e.length - 8)) + 32768});
    return map;
}

// Display system status()
function displaySystemStatus() {
    var deferred = $.Deferred();

    // Get system status data
    var url = '/api/status';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                cpu_percent = data['data']['cpu'];
                disk_percent = data['data']['disk'];
                mem_percent = data['data']['mem'];
                cached_percent = data['data']['cached'];
                swap_percent = data['data']['swap'];
                qemu_count = data['data']['qemu'];
                dynamips_count = data['data']['dynamips'];
                iol_count = data['data']['iol'];

                if (disk_percent >= 0) {
                    $('#status-disk').removeClass('progress-bar-striped');
                    if (disk_percent >= 75 && disk_percent < 90) {
                        // Warning, turn bar into yellow
                        $('#status-disk').addClass('progress-bar-warning');
                    }
                    if (disk_percent >= 90) {
                        // Critical, turn bar into red
                        $('#status-disk').addClass('progress-bar-danger');
                    }
                    // Expanding progress bar and setting text
                    $('#status-disk').text(disk_percent + '%');
                    $('#status-disk').width(disk_percent + '%');
                }
                if (cpu_percent >= 0) {
                    $('#status-cpu').removeClass('progress-bar-striped');
                    if (cpu_percent >= 75 && cpu_percent < 90) {
                        // Warning, turn bar into yellow
                        $('#status-cpu').addClass('progress-bar-warning');
                    }
                    if (cpu_percent >= 90) {
                        // Critical, turn bar into red
                        $('#status-cpu').addClass('progress-bar-danger');
                    }
                    // Expanding progress bar and setting text
                    $('#status-cpu').text(cpu_percent + '%');
                    $('#status-cpu').width(cpu_percent + '%');
                }
                if (mem_percent >= 0 && cached_percent >= 0) {
                    $('#status-mem').removeClass('progress-bar-striped');
                    $('#status-mem_used').removeClass('progress-bar-striped');
                    $('#status-mem_cached').removeClass('progress-bar-striped');
                    $('#status-mem_cached').addClass('progress-bar-success');
                    if (mem_percent >= 75 && mem_percent < 90) {
                        // Warning, turn bar into yellow
                        $('#status-mem_used').addClass('progress-bar-warning');
                    }
                    if (mem_percent >= 90) {
                        // Critical, turn bar into red
                        $('#status-mem_used').addClass('progress-bar-danger');
                    }
                    // Expanding progress bar and setting text
                    $('#status-mem').text('');
                    $('#status-mem').width('0%');
                    $('#status-mem_used').text('Used ' + mem_percent + '%');
                    $('#status-mem_used').width(mem_percent + '%');
                    $('#status-mem_cached').text('Cached ' + cached_percent + '%');
                    $('#status-mem_cached').width(cached_percent + '%');
                }
                if (swap_percent >= 0) {
                    $('#status-swap').removeClass('progress-bar-striped');
                    if (swap_percent >= 1 && swap_percent < 5) {
                        // Warning, turn bar into yellow
                        $('#status-swap').addClass('progress-bar-warning');
                    }
                    if (swap_percent >= 5) {
                        // Critical, turn bar into red
                        $('#status-swap').addClass('progress-bar-danger');
                    }
                    // Expanding progress bar and setting text
                    $('#status-swap').text(swap_percent + '%');
                    $('#status-swap').width(swap_percent + '%');
                }
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get disk usage.');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display folder_add form
function displayFolderAddForm(path) {
    var deferred = $.Deferred();
    var action = 'folder_add';
    var title = 'Add a new folder';
    var form = '';
    form += '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body"><form id="form-' + action + '" method="post" class="form-horizontal form-folder" action="#">';
    form += '<div class="form-group"><label class="col-md-3 control-label">Path</label><div class="col-md-5"><input type="text" class="form-control autofocus" name="folder[path]" value="' + path + '" disabled/></div></div>';
    form += '<div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input type="text" class="form-control autofocus" name="folder[name]" value=""/></div></div>';
    form += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">Add</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div><input type="hidden" name="action" value="' + action + '"/></form></div></div></div></div>';
    
    // Add the form to the HTML page
    $('#form_frame').html(form);

    // Autofocus on modal dialog
    $('.modal').on('shown.bs.modal', function () {
        $(this).find('.autofocus').focus();
    });

    // Show the form
    $('#modal-' + action).modal('show');
    $('.selectpicker').selectpicker();
    validateFolder();

    deferred.resolve();
    return deferred.promise();
}

// Display lab_add form
function displayLabAddForm(path) {
    var deferred = $.Deferred();
    var action = 'lab_add';
    var title = 'Add a new lab';
    var form = '';
    form += '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body"><form id="form-' + action + '" method="post" class="form-horizontal form-lab" action="#">';
    form += '<div class="form-group"><label class="col-md-3 control-label">Path</label><div class="col-md-5"><input type="text" class="form-control autofocus" name="lab[path]" value="' + path + '" disabled/></div></div>';
    // Name (autofocus)
    form += '<div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input type="text" class="form-control autofocus" name="lab[name]" value=""/></div></div>';
    // Version
    form += '<div class="form-group"><label class="col-md-3 control-label">Version</label><div class="col-md-5"><input type="text" class="form-control" name="lab[version]" value=""/></div></div>';
    // Author
    form += '<div class="form-group"><label class="col-md-3 control-label">Author</label><div class="col-md-5"><input type="text" class="form-control" name="lab[author]" value=""/></div></div>';
    // Description
    form += '<div class="form-group"><label class="col-md-3 control-label">Description</label><div class="col-md-5"><input type="text" class="form-control" name="lab[description]" value=""/></div></div>';
    form += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">Add</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div><input type="hidden" name="action" value="' + action + '"/></form></div></div></div></div>';

    // Add the form to the HTML page
    $('#form_frame').html(form);

    // Autofocus on modal dialog
    $('.modal').on('shown.bs.modal', function () {
        $(this).find('.autofocus').focus();
    });

    // Show the form
    $('#modal-' + action).modal('show');
    $('.selectpicker').selectpicker();
    validateLabInfo();

    deferred.resolve();
    return deferred.promise();
}

// Display folder content
function displayFolder(path) {
    var deferred = $.Deferred();

    // Get folder content
    var url = '/api/folders' + path;
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            var content = '';
            if (data['status'] == 'success') {
                // Fetching ok
                content += '<h1>Index of ' + path + '</h1>';
                content += '<div class="row">';
                content += '<div class="col-md-12">';

                // Listing folders
                content += '<table class="table table-hover">';
                content += '<thead><tr><th>Folders</th></tr></thead>';
                content += '<tbody>';
                $.each(data['data']['folders'], function(object_id, object) {
                    content += '<tr class="folder_menu" data-name="' + object['name'] + '" data-path="' + object['path'] + '"><td><a href="/lab_list.php?path=' + object['path'] + '"><span class="glyphicon glyphicon-folder-close"></span> ' + object['name'] + '</a></td></tr>';
                });
                content += '</tbody>';
                content += '</table>';

                // Listing labs
                content += '<table class="table table-hover">';
                content += '<thead><tr><th>Labs</th></tr></thead>';
                content += '<tbody>';
                $.each(data['data']['labs'], function(object_id, object) {
                    content += '<tr class="lab_menu" data-file="' + object['file'] + '" data-path="' + object['path'] + '"><td><a href="/lab_open.php?filename=' + object['path'] + '"><span class="glyphicon glyphicon-file"></span> ' + object['file'] + '</a></td></tr>';
                });
                content += '</tbody>';
                content += '</table>';
                content += '</div>';
                content += '</div>';

                deferred.resolve();
            } else {
                // Fetching failed
                content += '<h1>Cannot get folder "' + path + '"</h1>';
                raiseMessage('DANGER', 'Cannot get folder "' + path + '".');
                deferred.reject();
            }
            $('#folder_content').html(content);
        },
        error: function(data) {
            var content = '<h1>Cannot call API ("' + url + '")</h1>';
            $('#folder_content').html(content);
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Delete Folder
function deleteFolder(lab_file, folder) {
    var deferred = $.Deferred();
    var data = [];

    // Delete folder
    var url = '/api/folders' + folder;
    $.ajax({
        timeout: TIMEOUT,
        type: 'DELETE',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                $('*[data-path="' + folder + '"]').fadeOut(300, function() {
                    $(this).remove();
                });
                deferred.resolve(data);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot delete folder "' + folder + '".');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Open lab_edit page
function editLab(lab_file, lab) {
    window.location.href = '/lab_edit.php?filename=' + lab;
}

// Delete lab
function deleteLab(lab_file, lab) {
    var deferred = $.Deferred();
    var data = [];

    // Delete folder
    var url = '/api/labs' + lab;
    $.ajax({
        timeout: TIMEOUT,
        type: 'DELETE',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                $('*[data-path="' + lab + '"]').fadeOut(300, function() {
                    $(this).remove();
                });
                deferred.resolve(data);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot delete lab "' + lab + '".');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display lab info
function displayLabInfo(lab_file) {
    var deferred = $.Deferred();

    // Get main info
    var url = '/api/labs' + lab_file;
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            var info = '';
            if (data['status'] == 'success') {
                // Fetching ok
                if ($(location).attr('pathname') == '/lab_edit.php') {
                    // Form for edit lab
                    $('title').text(data['data']['name'] + ' - edit');
                    info += '<h1>' + data['data']['name'] + '</h1>';
                    info += '<form id="form-lab_edit" class="form-horizontal form-lab">';
                    info += '<div class="form-group"><label class="col-lg-3 control-label">Name</label><div class="col-lg-5"><input type="text" name="lab[name]" value="' + data['data']['name'] + '"/></div></div>';
                    info += '<div class="form-group"><label class="col-lg-3 control-label">Filename</label><div class="col-lg-5"><input type="text" name="lab[filename]" value="' + lab_file + '"/></div></div>';
                    info += '<div class="form-group"><label class="col-lg-3 control-label">Version</label><div class="col-lg-5"><input type="text" name="lab[version]" value="' + data['data']['version'] + '" required /></div></div>';
                    info += '<div class="form-group"><label class="col-lg-3 control-label">Author</label><div class="col-lg-5"><input type="text" name="lab[author]" value="' + data['data']['author'] + '"/></div></div>';
                    info += '<div class="form-group"><label class="col-lg-3 control-label">Description</label><div class="col-lg-5"><textarea type="text" name="lab[description]">' + data['data']['description'] + '</textarea></div></div>';
                    info += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">Save</button> <button type="reset" class="btn btn-danger">Cancel</button></div></div>';
                    info += '</form>';
                    $('#lab_info').html(info);

                    // Disable lab_name and lab_file
                    $('form :input[name="lab[name]"]').prop('disabled', true);
                    $('form :input[name="lab[filename]"]').prop('disabled', true);

                    // Validate values and set autofocus
                    $('.selectpicker').selectpicker();
                    validateLabInfo();
                } else {
                    // Normal info for open lab
                    $('title').text(data['data']['name']);
                    info += '<h1>' + data['data']['name'] + '</h1>';
                    info += '<small>' + data['data']['name'] + ' - Version ' + data['data']['version'] + '</small>';
                    info += '<p>' + data['data']['description'] + '</p>';
                    $('#lab_info').html(info);
                }
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get lab info "' + lab_file + '".');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display lab networks
function displayLabNetworks(lab_file) {
    var deferred = $.Deferred();

    // Get Networks
    var url = '/api/labs' + lab_file + '/networks';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            var objects = '';
            var topology = '';
            if (data['status'] == 'success') {
                // Fetching ok

                // Objects (header)
                objects += '<table class="table table-hover table-object">';
                objects += '<thead><tr><th>ID</th><th>Icon</th><th>Name</th><th>Type</th></tr></thead>';
                objects += '<tbody>';

                // For each network
                $.each(data['data'], function(network_id, network) {
                    // Setting network icon
                    if (network['type'].substr(0, 4) == 'pnet') {
                        var icon = '/images/cloud.png';
                    } else {
                        var icon = '/images/lan.png';
                    }

                    // Adding to topology
                    topology += '<div id="network' + network['id'] + '" class="unused network_menu network_frame network' + network['id'] + '" style="top: ' + network['top'] + '; left: ' + network['left'] + ';" data-id="' + network['id'] + '" data-name="' + network['name'] + '">'
                    topology += '<img border="0" src="' + icon + '" />';
                    topology += '<div class="network_name">' + network['name'] + '</div>';
                    topology += '</div>';

                    // Adding to objects tab
                    objects += '<tr class="network_menu network' + network['id'] + '" data-id="' + network['id'] + '" data-name="' + network['name'] + '">';
                    objects += '<td>' + network['id'] + '</td>';
                    objects += '<td><img border="0" src="' + icon + '" /></td>';
                    objects += '<td>' + network['name'] + '</td><td>' + network['type'] + '</td>';
                    objects += '</tr>';
                });

                // Objects (footer)
                objects += '</tbody>';
                objects += '</table>';

                $('#lab_networks').html(objects);
                $('#lab_topology').append(topology);
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get lab networks ("' + lab_file + '").');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display lab nodes
function displayLabNodes(lab_file) {
    var deferred = $.Deferred();

    // Get Nodes
    var url = '/api/labs' + lab_file + '/nodes';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            var objects = '';
            var topology = '';
            if (data['status'] == 'success') {
                // Fetching ok

                // Objects (header)
                objects += '<table class="table table-hover table-object">';
                objects += '<thead><tr><th>ID</th><th>Icon</th><th>Status</th><th>Name</th><th>Type</th><th>CPU</th><th>Idle PC</th><th>NVRAM</th><th>RAM</th><th>Ethernet</th><th>Serial</th></tr></thead>';
                objects += '<tbody>';

                // For each node
                $.each(data['data'], function(node_id, node) {
                    // Adding to topology
                    topology += '<div id="node' + node['id'] + '" class="node_menu node_frame node' + node['id'] + '" style="top: ' + node['top'] + '; left: ' + node['left'] + ';" data-id="' + node['id'] + '" data-name="' + node['name'] + '">'
                    topology += '<a href="' + node['url'] + '"><img border="0" src="/images/icons/' + node['icon'] + '" /></a>';
                    topology += '<div class="node_name"><i class="node' + node['id'] + '_status"></i> ' + node['name'] + '</div>';
                    topology += '</div>';

                    // Adding to objects tab
                    objects += '<tr class="node_menu node' + node['id'] + '" data-id="' + node['id'] + '" data-name="' + node['name'] + '">';
                    objects += '<td>' + node['id'] + '</td>';
                    objects += '<td><img border="0" src="/images/icons/' + node['icon'] + '" /></td>';
                    objects += '<td><i class="node' + node['id'] + '_status"></i></td>';
                    objects += '<td>' + node['name'] + '</td>';
                    objects += '<td>' + node['type'] + '</td>';
                    objects += '<td>'; if (typeof node['cpu'] != 'undefined') objects += node['cpu']; objects += '</td>';
                    objects += '<td>'; if (typeof node['idlepc'] != 'undefined') objects += node['idlepc']; objects += '</td>';
                    objects += '<td>'; if (typeof node['nvram'] != 'undefined') objects += node['nvram']; objects += '</td>';
                    objects += '<td>' + node['ram'] + '</td>';
                    objects += '<td>'; if (typeof node['ethernet'] != 'undefined') objects += node['ethernet']; objects += '</td>';
                    objects += '<td>'; if (typeof node['serial'] != 'undefined') objects += node['serial']; objects += '</td>';
                    objects += '</tr>';
                });

                // Objects (footer)
                objects += '</tbody>';
                objects += '</table>';

                $('#lab_nodes').html(objects);
                $('#lab_topology').append(topology);
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get lab nodes ("' + lab_file + '").');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display lab pictures
function displayLabPictures(lab_file) {
    var deferred = $.Deferred();

    // Get Networks
    var url = '/api/labs' + lab_file + '/pictures';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            var objects = '';
            if (data['status'] == 'success') {
                // Fetching ok
                objects += '<ul class="thumbnails">';

                // For each picture
                $.each(data['data'], function(picture_id, picture) {
                    // Adding to picture tab
                    objects += '<li><div class="picture_menu picture_frame picture' + picture['id'] + '" data-id="' + picture['id'] + '" data-name="' + picture['name'] + '" data-path="' + url + '/' + picture['id'] + '/data">';
                    if ($(location).attr('pathname') == '/lab_edit.php') {
                        // Form for edit lab
                        objects += '<img border="0" src="' + url + '/' + picture['id'] + '/data?height=40"/>';
                    } else {
                        // Normal for open lab
                        objects += '<a href="#"><img border="0" src="' + url + '/' + picture['id'] + '/data?height=40"/></a>';
                    }
                    objects += '<div class="caption">' + picture['name'] + '</div>';
                    objects += '</div></li>';
                });

                objects += '</ul>';

                $('#lab_pictures').html(objects);
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get lab networks ("' + lab_file + '").');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display lab status
function displayLabStatus() {
    var deferred = $.Deferred();

    // Get Nodes
    var url = '/api/labs' + lab_file + '/nodes';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                // For each node
                $.each(data['data'], function(node_id, node) {
                    if (node['status'] == 0) {
                        // Stopped
                        $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-stop');
                    } else if (node['status'] == 1) {
                        // Started
                        $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-play');
                    } else if (node['status'] == 2) {
                        // Building
                        $('.node' + node['id'] + '_status').attr('class', 'node' + node['id'] + '_status glyphicon glyphicon-flash');
                    }
                });
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get lab status ("' + lab_file + '").');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

function displayLabTopology(lab_file) {
    var deferred = $.Deferred();

    jsPlumb.ready(function() {
        // Defaults
        jsPlumb.importDefaults({
            Anchor: 'Continuous',
            Connector: ['Straight'],
            Endpoint: 'Blank',
            PaintStyle: {lineWidth: 2, strokeStyle: '#58585a'},
            cssClass: 'link',
        });

        // Create jsPlumb topology
        var lab_topology = jsPlumb.getInstance();

        // Nodes are draggable on lab_edit page only
        if ($(location).attr('pathname') == '/lab_edit.php') {
            // Nodes and netoworks are draggable within a grid
            lab_topology.draggable($('.node_frame, .network_frame'), { grid: [20, 20] });
        }

        // Get topology
        var url = '/api/labs' + lab_file + '/topology';
        $.ajax({
            timeout: TIMEOUT,
            type: 'GET',
            url: encodeURI(url),
            dataType: 'json',
            success: function(data) {
                if (data['status'] == 'success') {
                    // Fetching ok
                    $.each(data['data'], function(id, link) {
                        var type = link['type'];
                        var source = link['source'];
                        var source_label = link['source_label'];
                        var destination = link['destination'];
                        var destination_label = link['destination_label'];

                        if (type == 'ethernet') {
                            jsPlumb.connect({
                                source: source,       // Must attach to the IMG's parent or not printed correctly
                                target: destination,  // Must attach to the IMG's parent or not printed correctly
                                cssClass: source + " " + destination,
                                overlays: [
                                    [ "Label", { label: source_label, location: 0.15, cssClass: 'node_interface ' + source + ' ' + destination } ],
                                    [ "Label", { label: destination_label, location: 0.85, cssClass: 'node_interface ' + source + ' ' + destination } ],
                                ]
                            });
                        } else {
                            jsPlumb.connect({
                                source: source,       // Must attach to the IMG's parent or not printed correctly
                                target: destination,  // Must attach to the IMG's parent or not printed correctly
                                cssClass: source + " " + destination,
                                paintStyle : { lineWidth : 2, strokeStyle : "#ffcc00" },
                                overlays: [
                                    [ "Label", { label: source_label, location: 0.15, cssClass: 'node_interface ' + source + ' ' + destination } ],
                                    [ "Label", { label: destination_label, location: 0.85, cssClass: 'node_interface ' + source + ' ' + destination } ],
                                ]
                            });
                        }

                        // If destination is a network, remove the 'unused' class
                        if (destination.substr(0, 7) == 'network') {
                            $('.' + destination).removeClass('unused');
                        }
                    });

                    // Hide unused elements
                    $('.unused').hide();

                    // Move elements under the topology node
                    $('._jsPlumb_connector, ._jsPlumb_overlay, ._jsPlumb_endpoint_anchor_').detach().appendTo('#lab_topology');

                    // Now remove the progess bar
                    $('#lab_topology').children('.progress').remove();


                    deferred.resolve();
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', 'Cannot get lab topology ("' + lab_file + '").');
                    deferred.reject();
                }
            },
            error: function() {
                raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
                deferred.reject();
            }
        });
    });
    return deferred.promise();
}

// Stop node(s)
function stopLabNodes(lab_file, node_id) {
    var deferred = $.Deferred();

    // Get action URL
    if (node_id == 'all') {
        var url = '/api/labs' + lab_file + '/nodes/stop';
    } else {
        var url = '/api/labs' + lab_file + '/nodes/' + node_id + '/stop';
    }
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Node(s) stopped.');
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot stop node(s).');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Start node(s)
function startLabNodes(lab_file, node_id) {
    var deferred = $.Deferred();

    // Get action URL
    if (node_id == 'all') {
        var url = '/api/labs' + lab_file + '/nodes/start';
    } else {
        var url = '/api/labs' + lab_file + '/nodes/' + node_id + '/start';
    }
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Node(s) started, please wait.');
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot start node(s).');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Wipe node(s)
function wipeLabNodes(lab_file, node_id) {
    var deferred = $.Deferred();

    // Get action URL
    if (node_id == 'all') {
        var url = '/api/labs' + lab_file + '/nodes/wipe';
    } else {
        var url = '/api/labs' + lab_file + '/nodes/' + node_id + '/wipe';
    }
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                raiseMessage('SUCCESS', 'Node(s) wiped.');
                deferred.resolve();
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot wipe node(s).');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Get network
function getNetwork(lab_file, network_id) {
    var deferred = $.Deferred();
    var data = [];

    // Get network
    if (network_id == null) {
        deferred.resolve();
    } else {
        var url = '/api/labs' + lab_file + '/networks/' + network_id;
        $.ajax({
            timeout: TIMEOUT,
            type: 'GET',
            url: encodeURI(url),
            dataType: 'json',
            success: function(data) {
                if (data['status'] == 'success') {
                    // Fetching ok
                    data['name'] = data['data']['name'];
                    data['type'] = data['data']['type'];
                    deferred.resolve(data);
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', 'Cannot get network (network_id = ' + network_id + ').');
                    deferred.reject();
                }
            },
            error: function(data) {
                raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
                deferred.reject();
            }
        });
    }
    return deferred.promise();
}

// Get picture
function getPicture(lab_file, picture_id) {
    var deferred = $.Deferred();
    var data = [];

    // Get picture
    if (picture_id == null) {
        deferred.resolve();
    } else {
        var url = '/api/labs' + lab_file + '/pictures/' + picture_id;
        $.ajax({
            timeout: TIMEOUT,
            type: 'GET',
            url: encodeURI(url),
            dataType: 'json',
            success: function(data) {
                if (data['status'] == 'success') {
                    // Fetching ok
                    picture = data['data'];
                    deferred.resolve(picture);
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', 'Cannot get picture (picture_id = ' + picture_id + ').');
                    deferred.reject();
                }
            },
            error: function(data) {
                raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
                deferred.reject();
            }
        });
    }
    return deferred.promise();
}

// Display network form
function displayNetworkForm(lab_file, network_id) {
    var deferred = $.Deferred();
    var network_name = 'Net';
    var network_type = 'bridge';

    // List network types
    var url = '/api/list/networks';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                if (network_id == null) {
                    var title = 'Add new network(s)';
                    var action = 'network_add';
                    var button = 'Add';
                } else {
                    var title = 'Edit network';
                    var action = 'network_edit';
                    var button = 'Save';
                }

                // Builind the form (after loading network)
                $.when(getNetwork(lab_file, network_id)).done(function(network) {

                    if (network != null) {
                         network_name = network['data']['name'];
                         network_type = network['data']['type'];
                    }

                    var form = '';
                    // Header
                    form += '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body"><form id="form-' + action + '" class="form-horizontal form-network">';
                    // Count (only network_add)
                    if (network_id == null) {
                        form += '<div class="form-group"><label class="col-md-3 control-label">Number of networks to add</label><div class="col-md-5"><input type="text" class="form-control autofocus" name="network[count]" value="1"/></div></div>';
                    } else {
                        form += '<input type="hidden" name="network[id]" value="' + network_id + '"/>';
                    }
                    // Name
                    form += '<div class="form-group"><label class="col-md-3 control-label">Name/prefix</label><div class="col-md-5"><input type="text" class="form-control" name="network[name]" value="' + network_name + '"/></div></div>';
                    // Type
                    form += '<div class="form-group"><label class="col-md-3 control-label">Type</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="network[type]" data-live-search="true">';
                    $.each(data['data'], function(id, type) {
                        var type_selected = '';
                        if (type == network_type) {
                            // 'bridge' is the default option
                            type_selected = ' selected';
                        }
                        form += '<option' + type_selected + ' value="' + type + '">' + type + '</option>';
                    });
                    form += '</select></div></div>';
                    // Footer
                    form += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">' + button + '</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div></form></div></div></div></div>';

                    // Add the form to the HTML page
                    $('#form_frame').html(form);

                    // Show the form
                    $('#modal-' + action).modal('show');
                    $('.selectpicker').selectpicker();
                    validateLabNetwork();

                    deferred.resolve();
                }).fail(function() {
                    deferred.reject();
                });
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot list network types.');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display picture form
function displayPictureForm(lab_file, picture_id) {
    var deferred = $.Deferred();
    var form = '';

    if (picture_id == null) {
        // Adding a new picture
        var title = 'Add new picture';
        var action = 'picture_add';
        var button = 'Add';
        // Header
        form += '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body"><form id="form-' + action + '" class="form-horizontal form-picture">';
        // Name
        form += '<div class="form-group"><label class="col-md-3 control-label">Name</label><div class="col-md-5"><input type="text" class="form-control" name="picture[name]" value=""/></div></div>';
        // File (add only)
        form += '<div class="form-group"><label class="col-md-3 control-label">Picture</label><div class="col-md-5"><input type="file" name="picture[file]" value=""/></div></div>';
        // Footer
        form += '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">' + button + '</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div></form></div></div></div></div>';
        // Add the form to the HTML page
        $('#form_frame').html(form);

        // Show the form
        $('#modal-' + action).modal('show');
        $('.selectpicker').selectpicker();
        validateLabPicture();
        deferred.resolve();
    } else {
        // Can be lab_edit or lab_open

        $.when(getPicture(lab_file, picture_id)).done(function(picture) {
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

// Delete network
function deleteLabNetwork(lab_file, network_id) {
    var deferred = $.Deferred();
    var data = [];

    // Delete network
    var url = '/api/labs' + lab_file + '/networks/' + network_id;
    $.ajax({
        timeout: TIMEOUT,
        type: 'DELETE',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                $('.network' + network_id).fadeOut(300, function() {
                    $(this).remove();
                });
                deferred.resolve(data);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot delete network (network_id = ' + network_id + ').');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Delete picture
function deletePicture(lab_file, picture_id) {
    var deferred = $.Deferred();
    var data = [];

    // Delete network
    var url = '/api/labs' + lab_file + '/pictures/' + picture_id;
    $.ajax({
        timeout: TIMEOUT,
        type: 'DELETE',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                $('.picture' + picture_id).fadeOut(300, function() {
                    $(this).remove();
                });
                deferred.resolve(data);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot delete picture (picture_id = ' + picture_id + ').');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display template form
function displayTemplateForm() {
    var deferred = $.Deferred();
    var form = '';

    // Getting node templates
    var url = '/api/list/templates/';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                form += '<form id="form-node_template"><select class="selectpicker show-tick form-control" name="node[template]" data-live-search="true"><option value="" selected></option>';
                $.each(data['data'], function(template_id, template) {
                    form += '<option value="' + template_id + '">' + template + '</option>';
                });
                form += '</select></form>';
                deferred.resolve(form);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot list node templates.');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Display node form
function displayNodeForm(lab_file, node_id) {
    var deferred = $.Deferred();

    if (node_id == null) {
        // Adding a new node
        var title = 'Add new node(s)';
        var action = 'node_add';
        var button = 'Add';
    } else {
        // Editing an existing node
        var title = 'Edit node';
        var action = 'node_edit';
        var button = 'Save';
    }

    var form_header = '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body">';
    var form_footer = '</div></div></div></div>';

    if (node_id == null) {
        // Adding a new node (template form)
        $.when(displayTemplateForm()).done(function(form_template) {
            // Add the form to the HTML page
            $('#form_frame').html(form_header + form_template + '<form id="form-' + action + '" class="form-horizontal form-node"></form>' + form_footer);

            // Show the form
            $('#modal-' + action).modal('show');
            $('.selectpicker').selectpicker();
        }).fail(function() {
            deferred.reject();
        });
    } else {
        // Edit an existing node
        // Getting the node
        var url = '/api/labs' + lab_file + '/nodes/' + node_id;
        $.ajax({
            timeout: TIMEOUT,
            type: 'GET',
            url: encodeURI(url),
            dataType: 'json',
            success: function(data) {
                if (data['status'] == 'success') {
                    // Fetching ok
                    $.when(displayNodeFormFromTemplate(data['data']['template'], true)).done(function(form_template) {
                        // Attach the form to the page
                        $('#form_frame').html(form_header + '<form id="form-' + action + '" class="form-horizontal form-node">' + form_template + '</form>' + form_footer);

                        // Need to delete the "count" field
                        $('form :input[name="node[count]"]').parents('.form-group').remove();

                        // Need to add the "node[id]" field
                        $('#form-node_edit').append('<input type="hidden" value="' + node_id + '" name="node[id]"/>');

                        // Fill values
                        $.each(data['data'], function(field_name, field_value) {
                            $('form :input[name="node[' + field_name + ']"]').val(field_value);
                        });

                        // Show the form
                        $('#modal-' + action).modal('show');
                        $('.selectpicker').selectpicker();

                        deferred.promise();
                    }).fail(function() {
                        deferred.reject();
                    });
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', 'Cannot get node.');
                    deferred.reject();
                }
            },
            error: function(data) {
                raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
                deferred.reject();
            }
        });
    }

    return deferred.promise();
}

// Display node form from template
function displayNodeFormFromTemplate(node_template, edit_mode) {
    var deferred = $.Deferred();
    var button = 'Add';
    if (edit_mode == true) {
        button = 'Save';
    }

    // Getting template
    var url = '/api/list/templates/' + node_template;
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                var node_type = data['data']['type'];

                // Builind the HTML
                var html_header = '';
                var html_footer = '<div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">' + button + '</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div><input type="hidden" name="node[type]" value="' + node_type + '"><input type="hidden" name="node[template]" value="' + node_template + '">';

                // Count
                var html_content = '<div class="form-group"><label class="col-md-3 control-label">Number of nodes to add</label><div class="col-md-5"><input type="text" class="form-control autofocus" name="node[count]" value="1"/></div></div>';

                // Adding options from XML
                $.each(data['data']['options'], function(option_id, option) {
                    var option_name = 'node[' + option_id + ']';
                    var option_text = option['name'];
                    var option_type = option['type'];
                    var option_value = option['value'];

                    if (option_type == 'input') {
                        // Simple input item
                        html_content = html_content + '<div class="form-group"><label class="col-md-3 control-label">' + option_text + '</label><div class="col-md-5"><input type="text" class="form-control" name="' + option_name + '" value="' + option_value + '"/></div></div>';
                    } else if (option_type == 'hidden') {
                        // Hidden item
                        html_content = html_content + '<input type="hidden" name="' + option_name + '" value="' + option_value + '"/>';
                    } else if (option_type == 'list') {
                        // List item
                        html_content = html_content + '<div class="form-group"><label class="col-md-3 control-label">' + option_text + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="' + option_name + '" data-live-search="true">';
                        $.each(option['list'], function(item_id, item) {
                            var item_name = item_id;
                            var item_text = item;
                            if (item_name == option_value) {
                                var item_selected = ' selected';
                            } else {
                                var item_selected = '';
                            }
                            html_content = html_content + '<option' + item_selected + ' value="' + item_name + '">' + item_text + '</option>';
                        });
                        html_content = html_content + '</select></div></div>';
                    }
                });

                deferred.resolve(html_header + html_content + html_footer);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get node template.');
                deferred.reject();
            }
        },
        error: function() {
            // Fetching failed
            raiseMessage('DANGER', 'Cannot get node template.');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Delete node
function deleteLabNode(lab_file, node_id) {
    var deferred = $.Deferred();
    var data = [];

    // Delete network
    var url = '/api/labs' + lab_file + '/nodes/' + node_id;
    $.ajax({
        timeout: TIMEOUT,
        type: 'DELETE',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                $('.node' + node_id).fadeOut(300, function() {
                    $(this).remove();
                });
                deferred.resolve(data);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot delete node (node_id = ' + noed_id + ').');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });
    return deferred.promise();
}

// Get lab links
function getLabLinks(lab_file) {
    var deferred = $.Deferred();

    // Getting the data
    var url = '/api/labs' + lab_file + '/links';
    $.ajax({
        timeout: TIMEOUT,
        type: 'GET',
        url: encodeURI(url),
        dataType: 'json',
        success: function(data) {
            if (data['status'] == 'success') {
                // Fetching ok
                deferred.resolve(data['data']);
            } else {
                // Fetching failed
                raiseMessage('DANGER', 'Cannot get lab links.');
                deferred.reject();
            }
        },
        error: function(data) {
            raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
            deferred.reject();
        }
    });

    return deferred.promise();
}

// Display node interface form
function displayNodeInterfacesForm(lab_file, node_id) {
    var deferred = $.Deferred();

    var title = 'Connect node';
    var action = 'node_connect';
    var button = 'Save';

    var form_header = '<div class="modal fade" id="modal-' + action + '" tabindex="-1" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title">' + title + '</h4></div><div class="modal-body"><form id="form-' + action + '" class="form-horizontal form-network">';
    var form_footer = '<input type="hidden" name="node_id" value="' + node_id + '"/><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">' + button + '</button> <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div></form></div></div></div></div>';
    var form_body = '';

    // Get lab links
    $.when(getLabLinks(lab_file)).done(function(links) {
        // Getting the node
        var url = '/api/labs' + lab_file + '/nodes/' + node_id + '/interfaces';
        $.ajax({
            timeout: TIMEOUT,
            type: 'GET',
            url: encodeURI(url),
            dataType: 'json',
            success: function(data) {
                if (data['status'] == 'success') {
                    // Fetching ok

                    // For each interface type
                    $.each(data['data'], function(type_id, type) {
                        if (type_id == 'ethernet') {
                            $.each(type, function(interfc_id, interfc) {
                                form_body += '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="interfc[' + interfc_id + ']" data-live-search="true">';
                                form_body += '<option value="">Disconnected</option>';
                                $.each(links['ethernet'], function(network_id, network_name) {
                                    var selected = '';
                                    if (interfc['network_id'] == network_id) {
                                        selected = ' selected';
                                    }
                                    form_body += '<option' + selected + ' value="' + network_id + '">' + network_name + '</option>';
                                });
                                form_body += '</select></div></div>';
                            });
                        } else if (type_id == 'serial') {
                            $.each(type, function(interfc_id, interfc) {
                                form_body += '<div class="form-group"><label class="col-md-3 control-label">' + interfc['name'] + '</label><div class="col-md-5"><select class="selectpicker show-tick form-control" name="interfc[' + interfc_id + ']" data-live-search="true">';
                                form_body += '<option value="">Disconnected</option>';
                                $.each(links['serial'], function(remote_id, link) {
                                    if (node_id != remote_id) {
                                        // Print only other nodes, not current
                                        $.each(link, function(remote_if, remote_name) {
                                            var selected = '';
                                            if (interfc['remote_id'] + ':' + interfc['remote_if'] == remote_id + ':' + remote_if) {
                                                selected = ' selected';
                                            }
                                            form_body += '<option' + selected + ' value="' + remote_id + ':' + remote_if + '">' + remote_name + '</option>';
                                        });
                                    }
                                });
                                form_body += '</select></div></div>';
                            });
                        }
                    });

                    // Show the form
                    $('#modal-' + action).modal('show');
                    $('.selectpicker').selectpicker();

                    // Add the form to the HTML page
                    $('#form_frame').html(form_header + form_body + form_footer);

                    // Show the form
                    $('#modal-' + action).modal('show');
                    $('.selectpicker').selectpicker();

                    deferred.resolve();
                } else {
                    // Fetching failed
                    raiseMessage('DANGER', 'Cannot get node interfaces.');
                    deferred.reject();
                }
            },
            error: function(data) {
                raiseMessage('DANGER', 'Cannot call API ("' + url + '").');
                deferred.reject();
            }
        });
    }).fail(function() {
        deferred.reject();
    });

    return deferred.promise();
}
