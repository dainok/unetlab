// vim: syntax=javascript tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/themes/default/js/actions.js
 *
 * Actions for HTML elements
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

var KEY_CODES = {
    "tab": 9,
    "enter": 13,
    "shift": 16,
    "ctrl": 17,
    "alt": 18,
    "escape": 27
};

// Attach files
$('body').on('change', 'input[type=file]', function (e) {
    ATTACHMENTS = e.target.files;
});

// Add the selected filename to the proper input box
$('body').on('change', 'input[name="import[file]"]', function (e) {
    $('input[name="import[local]"]').val($(this).val());
});

// On escape remove mouse_frame
$(document).on('keydown', 'body', function (e) {
    var $labViewport = $("#lab-viewport")
        , isFreeSelectMode = $labViewport.hasClass("freeSelectMode")
        , isEditCustomShape = $labViewport.has(".edit-custom-shape-form").length > 0
        , isEditText = $labViewport.has(".edit-custom-text-form").length > 0
        ;

    if (KEY_CODES.escape == e.which) {
        $('.lab-viewport-click-catcher').unbind('click');
        $('#mouse_frame').remove();
        $('#lab-viewport').removeClass('lab-viewport-click-catcher').data("prevent-contextmenu", false);

        //remove active link node connection

        if (islinkActive())
            $('.action-nodelink').trigger('click');

        $('#context-menu').remove();

    }

    if (isFreeSelectMode && KEY_CODES.escape == e.which) {
        $(".action-freeselect").click();    // it will handle all the stuff
    }
    if (isEditCustomShape && KEY_CODES.escape == e.which) {
        $(".edit-custom-shape-form button.cancelForm").click(); // it will handle all the stuff
    }
    if (isEditText && KEY_CODES.escape == e.which) {
        $(".edit-custom-text-form button.cancelForm").click();  // it will handle all the stuff
    }
});

//Add picture MAP
$('body').on('click', '.follower-wrapper', function (e) {
    var data_x = $("#follower").data("data_x");
    var data_y = $("#follower").data("data_y");
    var y = parseInt((data_y).toFixed(0));
    var x = parseInt((data_x).toFixed(0));
    $('form textarea').val($('form textarea').val() + "<area shape='circle' alt='img' coords='" + x + "," + y + ",30' href='telnet://{{IP}}:{{NODE1}}'>\n");
});

// Accept privacy
$(document).on('click', '#privacy', function () {
    $.cookie('privacy', 'true', {
        expires: 90,
        path: '/'
    });
    if ($.cookie('privacy') == 'true') {
        window.location.reload();
    }
});

// Select folders, labs or users
$(document).on('click', 'a.folder, a.lab, tr.user', function (e) {
    logger(1, 'DEBUG: selected "' + $(this).attr('data-path') + '".');
    if ($(this).hasClass('selected')) {
        // Already selected -> unselect it
        $(this).removeClass('selected');
    } else {
        // Selected it
        $(this).addClass('selected');
    }
});

// Remove modal on close
$(document).on('hidden.bs.modal', '.modal', function (e) {
    $(this).remove();
    if ($('body').children('.modal.fade.in')) {
        $('body').children('.modal.fade.in').focus();
        $('body').children('.modal.fade.in').css("overflow-y", "auto");
    }
    if ($(this).prop('skipRedraw') && !$(this).attr('skipRedraw')) {
        printLabTopology();
    }
    $(this).attr('skipRedraw', false);
});

// Set autofocus on show modal
$(document).on('shown.bs.modal', '.modal', function () {
    $('.autofocus').focus();
});

// After node/network move
$(document).on('dragstop', '.node_frame, .network_frame', function (e) {
    var that = this,
        offset = $(this).offset(),
        left = Math.round(offset.left - 30 + $('#lab-viewport').scrollLeft()),  // 30 is the sidebar
        top = Math.round(offset.top + $('#lab-viewport').scrollTop()),
        id = $(this).attr('data-path');
    if (left >= 0 && top >= 0) {
        if ($(this).hasClass('node_frame')) {
            logger(1, 'DEBUG: setting node' + id + ' position.');
            $.when(setNodePosition(id, left, top)).done(function () {
                // Position saved -> redraw topology
                jsPlumb.repaint(that);
            }).fail(function (message) {
                // Error on save
                addModalError(message);
            });
        } else if ($(this).hasClass('network_frame')) {
            logger(1, 'DEBUG: setting network' + id + ' position.');
            $.when(setNetworkPosition(id, left, top)).done(function () {
                // Position saved -> redraw topology
                jsPlumb.repaint(that);
            }).fail(function (message) {
                // Error on save
                addModalError(message);
            });
        } else {
            logger(1, 'DEBUG: unknown object.');
        }
    } else {
        addMessage('warning', MESSAGES[124]);
    }
});

// Close all context menu
$(document).on('mousedown', '*', function (e) {
    if (!$(e.target).is('#context-menu, #context-menu *')) {
        // If click outside context menu, remove the menu
        e.stopPropagation();
        $('#context-menu').remove();

    }
});

// Open context menu block
$(document).on('click', '.menu-collapse, .menu-collapse i', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var item_class = $(this).attr('data-path');
    $('.context-collapsible').slideUp('slow');
    $('.' + item_class).slideToggle('slow');
});

$(document).on('contextmenu', '#lab-viewport', function (e) {
    // Prevent default context menu on viewport
    e.stopPropagation();
    e.preventDefault();

    logger(1, 'DEBUG: action = opencontextmenu');

    if ($(this).hasClass("freeSelectMode")) {
        // prevent 'contextmenu' on non Free Selected Elements

        return;
    }

    if ($(this).data("prevent-contextmenu")) {
        // prevent code execution

        return;
    }

    if (ROLE != "user") {
        var body = '';
        body += '<li><a class="action-nodeplace" href="javascript:void(0)"><i class="glyphicon glyphicon-hdd"></i> ' + MESSAGES[81] + '</a></li>';
        body += '<li><a class="action-networkplace" href="javascript:void(0)"><i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[82] + '</a></li>';
        body += '<li><a class="action-pictureadd" href="javascript:void(0)"><i class="glyphicon glyphicon-picture"></i> ' + MESSAGES[83] + '</a></li>';
        body += '<li><a class="action-customshapeadd" href="javascript:void(0)"><i class="glyphicon glyphicon-unchecked"></i> ' + MESSAGES[145] + '</a></li>';
        body += '<li><a class="action-textadd" href="javascript:void(0)"><i class="glyphicon glyphicon-font"></i> ' + MESSAGES[146] + '</a></li>';
        printContextMenu(MESSAGES[80], body, e.pageX, e.pageY);
    }
});

// Manage context menu
$(document).on('contextmenu', '.context-menu', function (e) {
    e.stopPropagation();
    e.preventDefault();  // Prevent default behaviour

    if ($("#lab-viewport").data("prevent-contextmenu")) {
        // prevent code execution

        return;
    }

    var isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode");

    if (isFreeSelectMode && !$(this).is(".node_frame.free-selected", ".node_frame.free-selected *")) {
        // prevent 'contextmenu' on non Free Selected Elements

        return;
    }

    if ($(this).hasClass('node_frame')) {
        logger(1, 'DEBUG: opening node context menu');

        var node_id = $(this).attr('data-path')
            , title = $(this).attr('data-name') + " (" + node_id + ")"
            , body = '<li>' +
                        '<a class="menu-collapse" data-path="menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[75] + '</a>' +
                '</li>' +
                '<li>' +
                        '<a class="action-nodestart context-collapsible menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-play"></i> ' + MESSAGES[66] +
                '</a>' +
                '</li>' +
                '<li>' +
                        '<a class="action-nodestop context-collapsible menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[67] +
                '</a>' +
                '</li>' +
                '<li>' +
                        '<a class="action-nodewipe context-collapsible menu-manage" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-erase"></i> ' + MESSAGES[68] +
                '</a>' +
                '</li>' +
                '<li role="separator" class="divider">' +
                '</li>' +
                '<li id="menu-node-interfaces">' +
                        '<a class="menu-collapse" data-path="menu-interface" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[70] +
                '</a>' +
                '</li>'
            ;


        // Read privileges and set specific actions/elements
        if (ROLE == 'admin' || ROLE == 'editor') {


            body += '<li role="separator" class="divider">' +
                '</li>' +
                '<li>' +
                      '<a class="menu-collapse" data-path="menu-edit" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[73] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="action-nodeexport context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-save"></i> ' + MESSAGES[69] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="action-nodeinterfaces context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[72] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="action-nodeedit context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[71] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="action-nodedelete context-collapsible menu-edit" data-path="' + node_id + '" data-name="' + title + '" href="javascript:void(0)">' +
                '<i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[65] +
                '</a>' +
                '</li>'
            ;
        }
        ;

        // Adding interfaces
        $.when(getNodeInterfaces(node_id)).done(function (values) {
            var interfaces = '';
            $.each(values['ethernet'], function (id, object) {
                interfaces += '<li><a class="action-nodecapture context-collapsible menu-interface" href="capture://' + window.location.hostname + '/vunl' + TENANT + '_' + node_id + '_' + id + '" style="display: none;"><i class="glyphicon glyphicon-search"></i> ' + object['name'] + '</a></li>';
            });

            $(interfaces).insertAfter('#menu-node-interfaces');

        }).fail(function (message) {
            // Error on getting node interfaces
            addModalError(message);
        });


        if (isFreeSelectMode) {
            body = '' +
                '<li>' +
                    '<a class="menu-collapse" data-path="menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-chevron-down"></i> ' + MESSAGES[75] + '</a>' +
                '</li>' +
                '<li>' +
                    '<a class="action-nodestart-group context-collapsible menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-play"></i> ' + MESSAGES[153] + '</a>' +
                '</li>' +
                '<li>' +
                    '<a class="action-nodestop-group context-collapsible menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[154] + '</a>' +
                '</li>' +
                '<li>' +
                    '<a class="action-nodewipe-group context-collapsible menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-erase"></i> ' + MESSAGES[155] + '</a>' +
                '</li>';
            if (ROLE == 'admin' || ROLE == 'editor') {
                body += '' +
                    '<li role="separator" class="divider"></li>' +
                    '<li>' +
                        '<a class="action-nodeexport-group context-collapsible menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-save"></i> ' + MESSAGES[129] + '</a>' +
                    '</li>' +
                    '<li>' +
                        '<a class="action-nodesbootsaved-group" href="javascript:void(0)"><i class="glyphicon glyphicon-floppy-saved"></i> ' + MESSAGES[139] + '</a>' +
                    '</li>' +
                    '<li>' +
                        '<a class="action-nodesbootscratch-group" href="javascript:void(0)"><i class="glyphicon glyphicon-floppy-save"></i> ' + MESSAGES[140] + '</a>' +
                    '</li>';
            }
            body += '' +
                '<li role="separator" class="divider"></li>' +
                '<li>' +
                    '<a class="action-nodesbootdelete-group" href="javascript:void(0)"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[159] + '</a>' +
                '</li>' +
                '<li>' +
                    '<a class="action-nodedelete-group context-collapsible menu-manage" href="javascript:void(0)"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[157] + '</a>' +
                '</li>' +
                '';

            title = 'Group of ' + window.freeSelectedNodes.map(function (node) {
                    return node.name;
                }).join(", ").slice(0, 16);
            title += title.length > 24 ? "..." : "";

        }

    } else if ($(this).hasClass('network_frame')) {
        if (ROLE == 'admin' || ROLE == 'editor') {


            logger(1, 'DEBUG: opening network context menu');
            var network_id = $(this).attr('data-path');
            var title = $(this).attr('data-name');
            var body = '<li><a class="context-collapsible  action-networkedit" data-path="' + network_id + '" data-name="' + title + '" href="javascript:void(0)"><i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[71] + '</a></li><li><a class="context-collapsible  action-networkdelete" data-path="' + network_id + '" data-name="' + title + '" href="javascript:void(0)"><i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[65] + '</a></li>';
        }
    } else if ($(this).hasClass('customShape')) {
        if (ROLE == 'admin' || ROLE == 'editor') {
            logger(1, 'DEBUG: opening text object context menu');
            var textObject_id = $(this).attr('data-path')
                , title = 'Edit: ' + $(this).attr('data-path')
                , body =
                '<li>' +
                      '<a class="context-collapsible  action-textobjectduplicate" href="javascript:void(0)" data-path="' + textObject_id + '">' +
                '<i class="glyphicon glyphicon-duplicate"></i> ' + MESSAGES[149] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="context-collapsible  action-textobjecttoback" href="javascript:void(0)" data-path="' + textObject_id + '">' +
                '<i class="glyphicon glyphicon-save"></i> ' + MESSAGES[147] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="context-collapsible  action-textobjecttofront" href="javascript:void(0)" data-path="' + textObject_id + '">' +
                '<i class="glyphicon glyphicon-open"></i> ' + MESSAGES[148] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="context-collapsible  action-textobjectedit" href="javascript:void(0)" data-path="' + textObject_id + '">' +
                '<i class="glyphicon glyphicon-edit"></i> ' + MESSAGES[71] +
                '</a>' +
                '</li>' +
                '<li>' +
                      '<a class="context-collapsible  action-textobjectdelete" href="javascript:void(0)" data-path="' + textObject_id + '">' +
                '<i class="glyphicon glyphicon-trash"></i> ' + MESSAGES[65] +
                '</a>' +
                '</li>';
        }
    } else {
        // Context menu not defined for this object
        return false;
    }
    if (body.length) {

        printContextMenu(title, body, e.pageX, e.pageY);

    }

});

/**
 * left click
 */
$(document).off('click', '.context-menu')
    .on('click', '.context-menu', function (e) {

        if (islinkActive() && (ROLE == 'admin' || ROLE == 'editor')) {
            e.preventDefault();
            e.stopPropagation();

            var title = $(this).attr('data-name');
            var node_id = $(this).attr('data-path');

            contextMenuInterfaces(title, node_id, e);
        }
    })


// Window resize
$(window).resize(function () {
    if ($('#lab-viewport').length) {
        // Update topology on window resize
        jsPlumb.repaintEverything();
        // Update picture map on window resize
        $('map').imageMapResize();
    }
});

/***************************************************************************
 * Actions links
 **************************************************************************/

// startup-config menu
$(document).on('click', '.action-configsget', function (e) {
    logger(1, 'DEBUG: action = configsget');
    $.when(getNodeConfigs(null)).done(function (configs) {
        var body = '<div class="row"><div class="config-list col-md-2 col-lg-2"><ul>';
        $.each(configs, function (key, config) {
            var title = (config['config'] == 0) ? MESSAGES[122] : MESSAGES[121];
            body += '<li><a class="action-configget" data-path="' + key + '" href="javascript:void(0)" title="' + title + '">' + config['name'];
            if (config['config'] == 1) {
                body += ' <i class="glyphicon glyphicon-floppy-saved"></i>';
            }
            body += '</a></li>';
        });
        body += '</ul></div><div id="config-data" class="col-md-10 col-lg-10"></div></div>';
        addModalWide(MESSAGES[120], body, '');
    }).fail(function (message) {
        addModalError(message);
    });
});

// Change opacity
$(document).on('click', '.action-changeopacity', function (e) {
    if ($(this).data("transparent")) {
        $('.modal-content').fadeTo("fast", 1);
        $(this).data("transparent", false);
    } else {
        $('.modal-content').fadeTo("fast", 0.3);
        $(this).data("transparent", true);
    }
});

// Get startup-config
$(document).on('click', '.action-configget', function (e) {
    logger(1, 'DEBUG: action = configget');
    var id = $(this).attr('data-path');
    $.when(getNodeConfigs(id)).done(function (config) {
        printFormNodeConfigs(config);
        $('#config-data').find('.form-control').focusout(function () {
            saveLab();
        })
    }).fail(function (message) {
        addModalError(message);
    });
    $('#context-menu').remove();
});

// Add a new folder
$(document).on('click', '.action-folderadd', function (e) {
    logger(1, 'DEBUG: action = folderadd');
    var data = {};
    data['path'] = $('#list-folders').attr('data-path');
    printFormFolder('add', data);
});

// Open an existent folder
$(document).on('dblclick', '.action-folderopen', function (e) {
    logger(1, 'DEBUG: opening folder "' + $(this).attr('data-path') + '".');
    printPageLabList($(this).attr('data-path'));
});

// Rename an existent folder
$(document).on('click', '.action-folderrename', function (e) {
    logger(1, 'DEBUG: action = folderrename');
    var data = {};
    data['path'] = dirname($('#list-folders').attr('data-path'));
    data['name'] = basename($('#list-folders').attr('data-path'));
    printFormFolder('rename', data);
});

// Import labs
$(document).on('click', '.action-import', function (e) {
    logger(1, 'DEBUG: action = import');
    printFormImport($('#list-folders').attr('data-path'));
});

// Add a new lab
$(document).on('click', '.action-labadd', function (e) {
    logger(1, 'DEBUG: action = labadd');
    var values = {};
    values['path'] = $('#list-folders').attr('data-path');
    printFormLab('add', values);
});

// Print lab body
$(document).on('click', '.action-labbodyget', function (e) {
    logger(1, 'DEBUG: action = labbodyget');
    $.when(getLabInfo($('#lab-viewport').attr('data-path')), getLabBody()).done(function (info, body) {
        addModalWide(MESSAGES[64], '<h1>' + info['name'] + '</h1><p>' + info['description'] + '</p><p><code>ID: ' + info['id'] + '</code></p>' + body, '')
    }).fail(function (message1, message2) {
        if (message1 != null) {
            addModalError(message1);
        } else {
            addModalError(message2)
        }
        ;
    });
});

// Edit/print lab network
$(document).on('click', '.action-networkedit', function (e) {

    $('#context-menu').remove();
    logger(1, 'DEBUG: action = action-networkedit');
    var id = $(this).attr('data-path');
    $.when(getNetworks(id)).done(function (values) {
        values['id'] = id;
        printFormNetwork('edit', values)
        // window.closeModal = true;
    }).fail(function (message) {
        addModalError(message);
    });
});

// Edit/print lab network
$(document).on('click', '.action-networkdeatach', function (e) {

    $('#context-menu').remove();
    logger(1, 'DEBUG: action = action-networkdeatach');
    var node_id = $(this).attr('node-id');
    var interface_id = $(this).attr('interface-id');

    $.when(setNodeInterface(node_id, '', interface_id))
        .done(function (values) {

            window.location.reload();
        }).fail(function (message) {
        addModalError(message);
    });
});

// Print lab networks
$(document).on('click', '.action-networksget', function (e) {
    logger(1, 'DEBUG: action = networksget');
    $.when(getNetworks(null)).done(function (networks) {
        printListNetworks(networks);
    }).fail(function (message) {
        addModalError(message);
    });


});

// Delete lab network
$(document).on('click', '.action-networkdelete', function (e) {

    $('#context-menu').remove();
    if (!confirm('Are you sure ?')) return;

    logger(1, 'DEBUG: action = action-networkdelete');
    var id = $(this).attr('data-path');
    $.when(deleteNetwork(id)).done(function (values) {
        $('.network' + id).remove();
        window.closeModal = true;
    }).fail(function (message) {
        addModalError(message);
    });

    $('#context-menu').remove();

});


/**
 * reload on close
 */
$(document).on('hide.bs.modal', function (e) {

    if (window.closeModal) {
        printLabTopology();
        window.closeModal = false;
    }

});


// Delete lab node

$(document).on('click', '.action-nodedelete, .action-nodedelete-group', function (e) {
    if (!confirm('Are you sure ?')) return;
    logger(1, 'DEBUG: action = action-nodedelete');
    var node_id = $(this).attr('data-path')
        , isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        ;

    if (isFreeSelectMode) {
        window.freeSelectedNodes = window.freeSelectedNodes.sort(function (a, b) {
            return a.path < b.path ? -1 : 1
        });
        recursionNodeDelete(window.freeSelectedNodes);
    }
    else {
        $.when(deleteNode(node_id)).done(function (values) {
            $('.node' + node_id).remove();
        }).fail(function (message) {
            addModalError(message);
        });
    }
    $('#context-menu').remove();
});


function recursionNodeDelete(restOfList) {
    var node = restOfList.pop();

    if (!node) {
        return 1;
    }

    console.log("Deleting... ", node.path);
    $.when(deleteNode(node.path)).done(function (values) {
        $('.node' + node.path).remove();
        recursionNodeDelete(restOfList);
    }).fail(function (message) {
        addModalError(message);
        recursionNodeDelete(restOfList);
    });
}

// Edit/print node interfaces
$(document).on('click', '.action-nodeinterfaces', function (e) {
    logger(1, 'DEBUG: action = action-nodeinterfaces');
    var id = $(this).attr('data-path');
    var name = $(this).attr('data-name');
    $.when(getNodeInterfaces(id)).done(function (values) {
        values['node_id'] = id;
        values['node_name'] = name;
        printFormNodeInterfaces(values)
    }).fail(function (message) {
        addModalError(message);
    });
    $('#context-menu').remove();
});

// Deatach network lab node


$(document).on('click', '.action-nodeedit', function (e) {
    logger(1, 'DEBUG: action = action-nodeedit');
    var id = $(this).attr('data-path');
    $.when(getNodes(id)).done(function (values) {
        values['id'] = id;
        printFormNode('edit', values)
    }).fail(function (message) {
        addModalError(message);
    });
    $('#context-menu').remove();
});


// Print lab nodes
$(document).on('click', '.action-nodesget', function (e) {
    logger(1, 'DEBUG: action = nodesget');
    $("#lab-viewport").append("<div id='nodelist-loader'><label style='float:left'>Generating node list...</label><div class='loader'></div></div>")
    $.when(getNodes(null)).done(function (nodes) {
        printListNodes(nodes);
    }).fail(function (message) {
        addModalError(message);
    });
});

// Lab close
$(document).on('click', '.action-labclose', function (e) {
    logger(1, 'DEBUG: action = labclose');
    $.when(closeLab()).done(function () {
        localStorage.setItem('action-nodelink',false);
        postLogin();
    }).fail(function (message) {
        addModalError(message);
    });
});

// Edit a lab
$(document).on('click', '.action-labedit', function (e) {
    logger(1, 'DEBUG: action = labedit');
    $.when(getLabInfo($('#lab-viewport').attr('data-path'))).done(function (values) {
        values['path'] = dirname($('#lab-viewport').attr('data-path'));
        printFormLab('edit', values);
    }).fail(function (message) {
        addModalError(message);
    });
    $('#context-menu').remove();
});

// Edit a lab inline
$(document).on('click', '.action-labedit-inline', function (e) {
    logger(1, 'DEBUG: action = labedit');
    $.when(getLabInfo($('.action-labedit-inline').attr('data-path'))).done(function (values) {
        values['path'] = dirname($('.action-labedit-inline').attr('data-path'));
        printFormLab('edit', values);
    }).fail(function (message) {
        addModalError(message);
    });
    $('#context-menu').remove();
});

// List all labs
$(document).on('click', '.action-lablist', function (e) {
    bodyAddClass('folders');
    logger(1, 'DEBUG: action = lablist');

    if ($('#list-folders').length > 0) {
        // Already on lab_list view -> open /
        printPageLabList('/');
    } else {
        printPageLabList(FOLDER);
    }

});

// Open a lab
$(document).on('click', '.action-labopen', function (e) {
    logger(1, 'DEBUG: action = labopen');
    var self = this;
    $.when(getUserInfo()).done(function () {
        postLogin($(self).attr('data-path'));
    }).fail(function () {
        // User is not authenticated, or error on API
        logger(1, 'DEBUG: loading authentication page.');
        printPageAuthentication();
    });
});

// Preview a lab
$(document).on('dblclick', '.action-labpreview', function (e) {
    logger(1, 'DEBUG: opening a preview of lab "' + $(this).attr('data-path') + '".');
    $('.lab-opened').each(function () {
        // Remove all previous selected lab
        $(this).removeClass('lab-opened');
    });
    $(this).addClass('lab-opened');
    printLabPreview($(this).attr('data-path'));
});

// Action menu
$(document).on('click', '.action-moreactions', function (e) {
    logger(1, 'DEBUG: action = moreactions');
    var body = '';
    body += '<li><a class="action-nodesstart" href="javascript:void(0)"><i class="glyphicon glyphicon-play"></i> ' + MESSAGES[126] + '</a></li>';
    body += '<li><a class="action-nodesstop" href="javascript:void(0)"><i class="glyphicon glyphicon-stop"></i> ' + MESSAGES[127] + '</a></li>';
    body += '<li><a class="action-nodeswipe" href="javascript:void(0)"><i class="glyphicon glyphicon-erase"></i> ' + MESSAGES[128] + '</a></li>';
    if (ROLE == 'admin' || ROLE == 'editor') {
        body += '<li><a class="action-nodesexport" href="javascript:void(0)"><i class="glyphicon glyphicon-save"></i> ' + MESSAGES[129] + '</a></li>';
        body += '<li><a class="action-labedit" href="javascript:void(0)"><i class="glyphicon glyphicon-pencil"></i> ' + MESSAGES[87] + '</a></li>';
        body += '<li><a class="action-nodesbootsaved" href="javascript:void(0)"><i class="glyphicon glyphicon-floppy-saved"></i> ' + MESSAGES[139] + '</a></li>';
        body += '<li><a class="action-nodesbootscratch" href="javascript:void(0)"><i class="glyphicon glyphicon-floppy-save"></i> ' + MESSAGES[140] + '</a></li>';
        body += '<li><a class="action-nodesbootdelete" href="javascript:void(0)"><i class="glyphicon glyphicon-floppy-remove"></i> ' + MESSAGES[141] + '</a></li>';
    }
    printContextMenu(MESSAGES[125], body, e.pageX + 3, e.pageY + 3, true);
});

// Redraw topology
$(document).on('click', '.action-labtopologyrefresh', function (e) {
    logger(1, 'DEBUG: action = labtopologyrefresh');
    detachNodeLink();
    printLabTopology();

});

// Logout
$(document).on('click', '.action-logout', function (e) {
    logger(1, 'DEBUG: action = logout');
    $.when(logoutUser()).done(function () {
        localStorage.setItem('action-nodelink',false);
        printPageAuthentication();
    }).fail(function (message) {
        addModalError(message);
    });
});

// Add object in lab_view
$(document).on('click', '.action-labobjectadd', function (e) {
    logger(1, 'DEBUG: action = labobjectadd');
    var body = '';
    body += '<li><a class="action-nodeplace" href="javascript:void(0)"><i class="glyphicon glyphicon-hdd"></i> ' + MESSAGES[81] + '</a></li>';
    body += '<li><a class="action-networkplace" href="javascript:void(0)"><i class="glyphicon glyphicon-transfer"></i> ' + MESSAGES[82] + '</a></li>';
    body += '<li><a class="action-pictureadd" href="javascript:void(0)"><i class="glyphicon glyphicon-picture"></i> ' + MESSAGES[83] + '</a></li>';
  body += '<li><a class="action-customshapeadd" href="javascript:void(0)"><i class="glyphicon glyphicon-unchecked"></i> ' + MESSAGES[145] + '</a></li>';
  body += '<li><a class="action-textadd" href="javascript:void(0)"><i class="glyphicon glyphicon-font"></i> ' + MESSAGES[146] + '</a></li>';
    printContextMenu(MESSAGES[80], body, e.pageX, e.pageY, true);
});

// Add network
$(document).on('click', '.action-networkadd', function (e) {
    logger(1, 'DEBUG: action = networkadd');
    printFormNetwork('add', null);
});

// Place an object
$(document).on('click', '.action-nodeplace, .action-networkplace, .action-customshapeadd, .action-textadd', function (e) {
    var target = $(this)
        , object
        , frame = ''
        ;

    $("#lab-viewport").data("prevent-contextmenu", true);

    if (target.hasClass('action-customshapeadd')) {
        logger(1, 'DEBUG: action = customshapeadd');
    } else {
        logger(1, 'DEBUG: action = nodeplace');
    }

    $('#context-menu').remove();

    if (target.hasClass('action-nodeplace')) {
        object = 'node';
        frame = '<div id="mouse_frame" class="context-menu node_frame"><img src="/images/icons/Router.png"/></div>';
        $("#lab-viewport").addClass('lab-viewport-click-catcher');
    } else if (target.hasClass('action-networkplace')) {
        object = 'network';
        frame = '<div id="mouse_frame" class="context-menu network_frame"><img src="/images/lan.png"/></div>';
        $("#lab-viewport").addClass('lab-viewport-click-catcher');
    } else if (target.hasClass('action-customshapeadd')) {
        object = 'shape';
        frame = '<div id="mouse_frame" class="context-menu network_frame"><img src="/images/icons/CustomShape.png"/></div>';
        $("#lab-viewport").addClass('lab-viewport-click-catcher');
    } else if (target.hasClass('action-textadd')) {
        object = 'text';
        frame = '<div id="mouse_frame" class="context-menu network_frame"><img src="/images/icons/CustomShape.png"/></div>';
        $("#lab-viewport").addClass('lab-viewport-click-catcher');
    } else {
        return false;
    }

    addMessage('info', MESSAGES[100]);
    if (!$('#mouse_frame').length) {
        // Add the frame container if not exists
        $('#lab-viewport').append(frame);
    } else {
        $('#mouse_frame').remove();
        $('#lab-viewport').append(frame);
    }

    // On mouse move, adjust css
    $('#lab-viewport').off("mousemove").on("mousemove", function (e1) {
        $('#mouse_frame').css({
            'left': e1.pageX - 30,
            'top': e1.pageY
        });
    });

    // On click open the form
    $('.lab-viewport-click-catcher').off("click").on("click", function (e2) {
        $("#lab-viewport").data("prevent-contextmenu", false);

        if ($(e2.target).is('#lab-viewport, #lab-viewport *')) {
            // Click is within viewport
            if ($('#mouse_frame').length > 0) {
                // ESC not pressed
                var values = {};
                values['left'] = e2.pageX - 30;
                values['top'] = e2.pageY;
                if (object == 'node') {
                    printFormNode('add', values);
                } else if (object == 'network') {
                    printFormNetwork('add', values);
                } else if (object == 'shape') {
                    printFormCustomShape(values);
                } else if (object == 'text') {
                    printFormText(values);
                }
                $('#mouse_frame').remove();
            }
            $('#mouse_frame').remove();
            $('.lab-viewport-click-catcher').off();
        } else {
            addMessage('warning', MESSAGES[101]);
            $('#mouse_frame').remove();
            $('.lab-viewport-click-catcher').off();
        }
    });
});

// Add picture
$(document).on('click', '.action-pictureadd', function (e) {
    logger(1, 'DEBUG: action = pictureadd');
    $('#context-menu').remove();
    displayPictureForm();
    //printFormPicture('add', null);
});

// Attach files
var attachments;
$('body').on('change', 'input[type=file]', function (e) {
    attachments = e.target.files;
});

// Add picture form
$('body').on('submit', '#form-picture-add', function (e) {
    // lab_file = getCurrentLab//getParameter('filename');
    var lab_file = $('#lab-viewport').attr('data-path');
    var form_data = new FormData();
    var picture_name = $('form :input[name^="picture[name]"]').val();
    // Setting options
    $('form :input[name^="picture["]').each(function (id, object) {
        form_data.append($(this).attr('name').substr(8, $(this).attr('name').length - 9), $(this).val());
    });

    // Add attachments
    $.each(attachments, function (key, value) {
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
        success: function (data) {
            if (data['status'] == 'success') {
                addMessage('SUCCESS', 'Picture "' + picture_name + '" added.');
                // Picture added -> reopen this page (not reload, or will be posted twice)
                // window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                addMessage('DANGER', data['status']);
            }
        },
        error: function (data) {
            addMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('body').children('.modal').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Edit picture
$(document).on('click', '.action-pictureedit', function (e) {
    logger(1, 'DEBUG: action = pictureedit');
    $('#context-menu').remove();
    var picture_id = $(this).attr('data-path');
    $.when(getPictures(picture_id)).done(function (picture) {
        picture['id'] = picture_id;
        printFormPicture('edit', picture);
    }).fail(function (message) {
        addModalError(message);
    });
});

// Get picture
$(document).on('click', '.action-pictureget', function (e) {
    logger(1, 'DEBUG: action = pictureget');
    $('#context-menu').remove();
    var picture_id = $(this).attr('data-path');
    printPictureInForm(picture_id);

});

//Show circle under cursor
$(document).on('mousemove', '.follower-wrapper', function (e) {
    var offset = $('.follower-wrapper img').offset()
        , limitY = $('.follower-wrapper img').height()
        , limitX = $('.follower-wrapper img').width()
        , mouseX = Math.min(e.pageX - offset.left, limitX)
        , mouseY = Math.min(e.pageY - offset.top, limitY);

    if (mouseX < 0) mouseX = 0;
    if (mouseY < 0) mouseY = 0;

    $('#follower').css({left: mouseX, top: mouseY});
    $("#follower").data("data_x", mouseX);
    $("#follower").data("data_y", mouseY);
});

$(document).on('click', '#follower', function (e) {
    e.preventDefault();
    e.folowerPosition = {
        left: parseFloat($("#follower").css("left")) - 30,
        top: parseFloat($("#follower").css("top")) + 30
    };
});

// Get pictures list
$(document).on('click', '.action-picturesget', function (e) {
    logger(1, 'DEBUG: action = picturesget');
    $.when(getPictures()).done(function (pictures) {
        if (!$.isEmptyObject(pictures)) {
            var body = '<div class="row"><div class="picture-list col-md-1 col-lg-1"><ul class="map">';
            $.each(pictures, function (key, picture) {
                var title = picture['name'] || "pic name";
                body += '<li>';
                if (ROLE != "user")
                    body += '<a class="delete-picture" href="javascript:void(0)" data-path="' + key + '"><i class="glyphicon glyphicon-trash delete-picture" title="Delete"></i> ';
                body += '<a class="action-pictureget" data-path="' + key + '" href="javascript:void(0)" title="' + title + '">' + picture['name'].split(' ')[0] + '</a>';
                body += '</a></li>';
            });
            body += '</ul></div><div id="config-data" class="col-md-11 col-lg-11"></div></div>';
            addModalWide(MESSAGES[59], body, '', "modal-ultra-wide");
        } else {
            addMessage('info', MESSAGES[134]);
        }
    }).fail(function (message) {
        addModalError(message);
    });
});

// Get picture list old
$(document).on('click', '.action-picturesget-stop', function (e) {
    logger(1, 'DEBUG: action = picturesget');
    $.when(getPictures()).done(function (pictures) {
        if (!$.isEmptyObject(pictures)) {
            var body = '';
            $.each(pictures, function (key, picture) {
                body += '<li><a class="action-pictureget" data-path="' + key + '" href="javascript:void(0)" title="' + picture['name'] + '"><i class="glyphicon glyphicon-picture"></i> ' + picture['name'] + '</a></li>';
            });
            printContextMenu(MESSAGES[59], body, e.pageX, e.pageY);
        } else {
            addMessage('info', MESSAGES[134]);
        }
    }).fail(function (message) {
        addModalError(message);
    });
});

//Detele picture
$(document).on('click', '.delete-picture', function (e) {
    e.stopPropagation();  // Prevent default behaviour
    logger(1, 'DEBUG: action = pictureremove');
    var $self = $(this);

    var picture_id = $self.parent().attr('data-path');
    var lab_filename = $('#lab-viewport').attr('data-path');
    var body = '<form id="form-picture-delete" data-path="' + picture_id + '" class="form-horizontal form-picture" novalidate="novalidate"><div class="form-group"><div class="col-md-5 col-md-offset-3"><button type="submit" class="btn btn-success">Delete</button><button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button></div></div></form>'
    var title = "Delete this picture?"
    addModal(title, body, "", "second-win");
});

// Clone selected labs
$(document).on('click', '.action-selectedclone', function (e) {
    if ($('.selected').size() > 0) {
        logger(1, 'DEBUG: action = selectedclone');
        $('.selected').each(function (id, object) {
            form_data = {};
            form_data['name'] = 'Copy of ' + $(this).text().slice(0, -4);
            form_data['source'] = $(this).attr('data-path');
            $.when(cloneLab(form_data)).done(function () {
                // Lab cloned -> reload the folder
                printPageLabList($('#list-folders').attr('data-path'));
            }).fail(function (message) {
                // Error on clone
                addModalError(message);
            });
        });
    }
});

// Delete selected folders and labs
$(document).on('click', '.action-selecteddelete', function (e) {
    if ($('.selected').size() > 0) {
        logger(1, 'DEBUG: action = selecteddelete');
        if (!confirm('Are you sure ?'))
            return;
        $('.selected').each(function (id, object) {
            var path = $(this).attr('data-path');
            if ($(this).hasClass('folder')) {
                $.when(deleteFolder(path)).done(function () {
                    // Folder deleted
                    $('.folder[data-path="' + path + '"]').fadeOut(300, function () {
                        $(this).remove();
                    });
                }).fail(function (message) {
                    // Cannot delete folder
                    addModalError(message);
                });
            } else if ($(this).hasClass('lab')) {
                $.when(deleteLab(path)).done(function () {
                    // Lab deleted
                    $('.lab[data-path="' + path + '"]').fadeOut(300, function () {
                        $(this).remove();
                    });
                }).fail(function (message) {
                    // Cannot delete lab
                    addModalError(message);
                });
            } else if ($(this).hasClass('user')) {
                $.when(deleteUser(path)).done(function () {
                    // User deleted
                    $('.user[data-path="' + path + '"]').fadeOut(300, function () {
                        $(this).remove();
                    });
                }).fail(function (message) {
                    // Cannot delete user
                    addModalError(message);
                });
            } else {
                // Invalid object
                logger(1, 'DEBUG: cannot delete, invalid object.');
                return;
            }
        });
    }
});

// Export selected folders and labs
$(document).on('click', '.action-selectedexport', function (e) {
    if ($('.selected').size() > 0) {
        logger(1, 'DEBUG: action = selectedexport');
        var form_data = {};
        var i = 0;
        form_data['path'] = $('#list-folders').attr('data-path')
        $('.selected').each(function (id, object) {
            form_data[i] = $(this).attr('data-path');
            i++;
        });
        $.when(exportObjects(form_data)).done(function (url) {
            // Export done
            window.location = url;
        }).fail(function (message) {
            // Cannot export objects
            addModalError(message);
        });
    }
});

// Delete all startup-config
$(document).on('click', '.action-nodesbootdelete, .action-nodesbootdelete-group', function (e) {
    $('#context-menu').remove();
    var isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        ;
    if (isFreeSelectMode) {
        var nodeLenght = window.freeSelectedNodes.length;
        var lab_filename = $('#lab-viewport').attr('data-path');
        $.each(window.freeSelectedNodes, function (i, node) {
            var form_data = {};
            form_data['id'] = node.path;
            form_data['data'] = '';
            var url = '/api/labs' + lab_filename + '/configs/' + node.path;
            var type = 'PUT';
            $.when($.ajax({
                timeout: TIMEOUT,
                type: type,
                url: encodeURI(url),
                dataType: 'json',
                data: JSON.stringify(form_data)
            })).done(function (message) {
                // Config deleted
                nodeLenght--;
                if (nodeLenght < 1) {
                    addMessage('success', MESSAGES[160])
                }
                ;
            }).fail(function (message) {
                // Cannot delete config
                nodeLenght--;
                if (nodeLenght < 1) {
                    addMessage('danger', node.name + ': ' + message);
                }
                ;
            });
        });
    } else {
        $.when(getNodes(null)).done(function (nodes) {
            var nodeLenght = Object.keys(nodes).length;
            $.each(nodes, function (key, values) {
                var lab_filename = $('#lab-viewport').attr('data-path');
                var form_data = {};
                form_data['id'] = key;
                form_data['data'] = '';
                var url = '/api/labs' + lab_filename + '/configs/' + key;
                var type = 'PUT';
                $.when($.ajax({
                    timeout: TIMEOUT,
                    type: type,
                    url: encodeURI(url),
                    dataType: 'json',
                    data: JSON.stringify(form_data)
                })).done(function (message) {
                    // Config deleted
                    nodeLenght--;
                    if (nodeLenght < 1) {
                        addMessage('success', MESSAGES[142])
                    }
                    ;
                }).fail(function (message) {
                    // Cannot delete config
                    nodeLenght--;
                    if (nodeLenght < 1) {
                        addMessage('danger', values['name'] + ': ' + message);
                    }
                    ;
                });
            });
        }).fail(function (message) {
            addModalError(message);
        });
    }
});

// Configure nodes to boot from scratch
$(document).on('click', '.action-nodesbootscratch, .action-nodesbootscratch-group', function (e) {
    $('#context-menu').remove();

    var isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        ;

    if (isFreeSelectMode) {
        $.each(window.freeSelectedNodes, function (i, node) {
            $.when(setNodeBoot(node.path, 0)).done(function () {
                addMessage('success', node.name + ': ' + MESSAGES[144]);
            }).fail(function (message) {
                // Cannot configure
                addMessage('danger', node.name + ': ' + message);
            });
        });
    }
    else {
        $.when(getNodes(null)).done(function (nodes) {
            $.each(nodes, function (key, values) {
                $.when(setNodeBoot(key, 0)).done(function () {
                    // Node configured -> print a small green message
                    addMessage('success', values['name'] + ': ' + MESSAGES[144])
                }).fail(function (message) {
                    // Cannot start
                    addMessage('danger', values['name'] + ': ' + message);
                });
            });
        }).fail(function (message) {
            addModalError(message);
        });
    }
});

// Configure nodes to boot from startup-config
$(document).on('click', '.action-nodesbootsaved, .action-nodesbootsaved-group', function (e) {
    $('#context-menu').remove();

    var isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        ;

    if (isFreeSelectMode) {
        $.each(window.freeSelectedNodes, function (i, node) {
            $.when(setNodeBoot(node.path, 1)).done(function () {
                addMessage('success', node.name + ': ' + MESSAGES[143]);
            }).fail(function (message) {
                // Cannot configure
                addMessage('danger', node.name + ': ' + message);
            });
        });
    }
    else {
        $.when(getNodes(null)).done(function (nodes) {
            $.each(nodes, function (key, values) {
                $.when(setNodeBoot(key, 1)).done(function () {
                    // Node configured -> print a small green message
                    addMessage('success', values['name'] + ': ' + MESSAGES[143])
                }).fail(function (message) {
                    // Cannot configure
                    addMessage('danger', values['name'] + ': ' + message);
                });
            });
        }).fail(function (message) {
            addModalError(message);
        });
    }
});

// Export a config
$(document).on('click', '.action-nodeexport, .action-nodesexport, .action-nodeexport-group', function (e) {
    $('#context-menu').remove();

    var node_id
        , isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        , exportAll = false
        , nodesLength
        ;

    if ($(this).hasClass('action-nodeexport')) {
        logger(1, 'DEBUG: action = nodeexport');
        node_id = $(this).attr('data-path');
    } else {
        logger(1, 'DEBUG: action = nodesexport');
        exportAll = true;
    }

    $.when(getNodes(null)).done(function (nodes) {
        if (isFreeSelectMode) {
            nodesLenght = window.freeSelectedNodes.length;
            addMessage('info', 'Export Selected:  Starting');
            $.when(recursive_cfg_export(window.freeSelectedNodes, nodesLenght)).done(function () {
            }).fail(function (message) {
                addMessage('danger', 'Export Selected: Error');
            });
        }
        else if (node_id) {
            addMessage('info', nodes[node_id]['name'] + ': ' + MESSAGES[138]);
            $.when(cfg_export(node_id)).done(function () {
                // Node exported -> print a small green message
                setNodeBoot(node_id, '1');
                addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[79])
            }).fail(function (message) {
                // Cannot export
                addMessage('danger', nodes[node_id]['name'] + ': ' + message);
            });
        } else if (exportAll) {
            /*
             * Parallel call for each node
             */
            nodesLenght = Object.keys(nodes).length;
            addMessage('info', 'Export all:  Starting');
            $.when(recursive_cfg_export(nodes, nodesLenght)).done(function () {
            }).fail(function (message) {
                addMessage('danger', 'Export all: Error');
            });
        }
    }).fail(function (message) {
        addModalError(message);
    });
});

// Start a node
$(document).on('click', '.action-nodestart, .action-nodesstart, .action-nodestart-group', function (e) {
    $('#context-menu').remove();
    var node_id
        , startAll
        , isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        , nodeLenght
        ;

    if ($(this).hasClass('action-nodestart')) {
        logger(1, 'DEBUG: action = nodestart');
        node_id = $(this).attr('data-path');
    } else {
        logger(1, 'DEBUG: action = nodesstart');
        startAll = true;
    }

    $.when(getNodes(null)).done(function (nodes) {
        if (isFreeSelectMode) {
            nodeLenght = window.freeSelectedNodes.length;
            addMessage('info', 'Start selected nodes...');
            $.when(recursive_start(window.freeSelectedNodes, nodeLenght)).done(function () {
            }).fail(function (message) {
                addMessage('danger', 'Start all: Error');
            });

        }
        else if (node_id != null) {
            $.when(start(node_id)).done(function () {
                // Node started -> print a small green message
                addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[76]);
                printLabStatus();
            }).fail(function (message) {
                // Cannot start
                addMessage('danger', nodes[node_id]['name'] + ': ' + message);
            });
        }
        else if (startAll) {
            nodesLenght = Object.keys(nodes).length;
            addMessage('info', 'Start all...');
            $.when(recursive_start(nodes, nodesLenght)).done(function () {
            }).fail(function (message) {
                addMessage('danger', 'Start all: Error');
            });
            /*
             $.each(nodes, function(key, values) {
             $.when(start(key)).done(function() {
             // Node started -> print a small green message
             addMessage('success', values['name'] + ': ' + MESSAGES[76]);
             nodeLenght--;
             if(nodeLenght < 1){
             printLabStatus();
             }
             }).fail(function(message) {
             // Cannot start
             addMessage('danger', values['name'] + ': ' + message);
             nodeLenght--;
             if(nodeLenght < 1){
             printLabStatus();
             }
             });
             });
             */
        }


    }).fail(function (message) {
        addModalError(message);
    });
});

// Stop a node
$(document).on('click', '.action-nodestop, .action-nodesstop, .action-nodestop-group', function (e) {
    $('#context-menu').remove();

    var node_id
        , nodeLenght
        , isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        , stopAll
        ;

    if ($(this).hasClass('action-nodestop')) {
        logger(1, 'DEBUG: action = nodestop');
        node_id = $(this).attr('data-path');
    } else {
        logger(1, 'DEBUG: action = nodesstop');
        stopAll = true;
    }

    $.when(getNodes(null)).done(function (nodes) {
        if (isFreeSelectMode) {
            nodeLenght = window.freeSelectedNodes.length;
            $.each(window.freeSelectedNodes, function (i, node) {
                $.when(stop(node.path)).done(function () {
                    // Node stopped -> print a small green message
                    addMessage('success', node.name + ': ' + MESSAGES[77]);
                    nodeLenght--;
                    if (nodeLenght < 1) {
                        setTimeout(printLabStatus, 3000);
                    }
                }).fail(function (message) {
                    // Cannot stopped
                    addMessage('danger', node.name + ': ' + message);
                    nodeLenght--;
                    if (nodeLenght < 1) {
                        setTimeout(printLabStatus, 3000);
                    }
                });
            });
        }
        else if (node_id != null) {
            $.when(stop(node_id)).done(function () {
                // Node stopped -> print a small green message
                addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[77])
                printLabStatus();
            }).fail(function (message) {
                // Cannot stop
                addMessage('danger', nodes[node_id]['name'] + ': ' + message);
            });
        }
        else if (stopAll) {
            nodeLenght = Object.keys(nodes).length;
            $.each(nodes, function (key, values) {
                $.when(stop(key)).done(function () {
                    // Node stopped -> print a small green message
                    addMessage('success', values['name'] + ': ' + MESSAGES[77]);
                    nodeLenght--;
                    if (nodeLenght < 1) {
                        setTimeout(printLabStatus, 3000);
                    }

                    $('#node' + values['id']).attr('data-status', 0);
                }).fail(function (message) {
                    // Cannot stopped
                    addMessage('danger', values['name'] + ': ' + message);
                    nodeLenght--;
                    if (nodeLenght < 1) {
                        setTimeout(printLabStatus, 3000);
                    }
                });
            });
        }
    }).fail(function (message) {
        addModalError(message);
    });
});

// Wipe a node
$(document).on('click', '.action-nodewipe, .action-nodeswipe, .action-nodewipe-group', function (e) {
    $('#context-menu').remove();

    var node_id
        , isFreeSelectMode = $("#lab-viewport").hasClass("freeSelectMode")
        , wipeAll
        ;

    if ($(this).hasClass('action-nodewipe')) {
        logger(1, 'DEBUG: action = nodewipe');
        node_id = $(this).attr('data-path');
    } else {
        logger(1, 'DEBUG: action = nodeswipe');
        wipeAll = true;
    }

    $.when(getNodes(null)).done(function (nodes) {
        if (isFreeSelectMode) {
            $.each(window.freeSelectedNodes, function (i, node) {
                $.when(setTimeout(function () {
                    wipe(node.path);
                }, nodes[node.path]['delay'] * 10)).done(function (res) {
                    // Node wiped -> print a small green message
                    addMessage('success', node.name + ': ' + MESSAGES[78])
                }).fail(function (message) {
                    // Cannot wiped
                    addMessage('danger', node.name + ': ' + message);
                });
            });
        }
        else if (node_id != null) {
            $.when(wipe(node_id)).done(function () {
                // Node wiped -> print a small green message
                addMessage('success', nodes[node_id]['name'] + ': ' + MESSAGES[78])
            }).fail(function (message) {
                // Cannot wipe
                addMessage('danger', nodes[node_id]['name'] + ': ' + message);
            });
        }
        else if (wipeAll) {
            $.each(nodes, function (key, values) {
                $.when(setTimeout(function () {
                    wipe(key);
                }, values['delay'] * 10)).done(function () {
                    // Node wiped -> print a small green message
                    addMessage('success', values['name'] + ': ' + MESSAGES[78])
                }).fail(function (message) {
                    // Cannot wiped
                    addMessage('danger', values['name'] + ': ' + message);
                });
            });
        }
    }).fail(function (message) {
        addModalError(message);
    });
});

// Stop all nodes
$(document).on('click', '.action-stopall', function (e) {
    logger(1, 'DEBUG: action = stopall');
    $.when(stopAll()).done(function () {
        // Stopped all nodes -> reload status page
        printSystemStats();
    }).fail(function (message) {
        // Cannot stop all nodes
        addModalError(message);
    });
});

// Load system status page
$(document).on('click', '.action-sysstatus', function (e) {
    bodyAddClass('status');
    logger(1, 'DEBUG: action = sysstatus');

    //printSystemStats();
    $.when(getSystemStats()).done(function (data) {
        // Main: title
        var html_title = '' +
            '<div class="row row-eq-height"><div id="list-title-folders" class="col-md-12 col-lg-12">' +
            '<span title="' + MESSAGES[13] + '">' + MESSAGES[13] + '</span>' +
            '</div>' +
            '</div>';

        // Main
        var html = '' +
            '<div id="systemStats" class="container col-md-12 col-lg-12">' +
            '<div class="fill-height row row-eq-height">' +
            '<div id="stats-text" class="col-md-3 col-lg-3">' +
            '<ul></ul>' +
            '</div>' +
            '<div id="stats-graph" class="col-md-9 col-lg-9">' +
            '<ul></ul>' +
            '</div>' +
            '</div>' +
            '</div>';

        // Footer
        html += '</div>';

        $('#main-title').html(html_title);
        $('#main-title').show();
        $('#main').html(html);

        printSystemStats(data);

        var statusIntervalID = setInterval(function () {
            $.when(getSystemStats()).done(function (data) {
                updateStatus(statusIntervalID, data);
            }).fail(function (message) {
                // Cannot get status
                addModalError(message);
                clearInterval(statusIntervalID);
            });
        }, 5000);

        bodyAddClass('status');

    }).fail(function (message) {
        addModalError(message);
    });


});

// Add a user
$(document).on('click', '.action-useradd', function (e) {
    logger(1, 'DEBUG: action = useradd');
    printFormUser('add', {});
});

// Edit a user
$(document).on('dblclick', '.action-useredit', function (e) {
    logger(1, 'DEBUG: action = useredit');
    $.when(getUsers($(this).attr('data-path'))).done(function (user) {
        // Got user
        printFormUser('edit', user);
    }).fail(function (message) {
        // Cannot get user
        addModalError(message);
    });
});

// Load user management page
$(document).on('click', '.action-update', function (e) {
    logger(1, 'DEBUG: action = update');
    addMessage('info', MESSAGES[133], true);
    $.when(update()).done(function (message) {
        // Got user
        addMessage('success', message, true);
    }).fail(function (message) {
        // Cannot get user
        addMessage('alert', message, true);
    });
});

// Load user management page
$(document).on('click', '.action-usermgmt', function (e) {
    bodyAddClass('users');
    logger(1, 'DEBUG: action = usermgmt');
    printUserManagement();
});

// Show status
$(document).on('click', '.action-status', function (e) {
    logger(1, 'DEBUG: action = show status');
    $.when(getSystemStats()).done(function (data) {

        // Body
        var html = '<div id="statusModal" class="container col-md-12 col-lg-12">' +
            '<div class="fill-height row row-eq-height">' +
            '<div id="stats-text" class="col-md-3 col-lg-3">' +
            '<ul></ul>' +
            '</div>' +
            '<div id="stats-graph" class="col-md-9 col-lg-9">' +
            '<ul></ul>' +
            '</div>' +
            '</div>' +
            '</div>';

        addModalWide("STATUS", html, '');
        drawStatusInModal(data);

    }).fail(function (message) {
        // Cannot get status
        addModalError(message);
    });

    var statusModalIntervalID = setInterval(function () {
        $.when(getSystemStats()).done(function (data) {
            updateStatusInModal(statusModalIntervalID, data);
        }).fail(function (message) {
            // Cannot get status
            addModalError(message);
            clearInterval(statusModalIntervalID);
        });
    }, 5000);
});

/***************************************************************************
 * Submit
 **************************************************************************/

// Submit folder form
$(document).on('submit', '#form-folder-add, #form-folder-rename', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var form_data = form2Array('folder');
    if ($(this).attr('id') == 'form-folder-add') {
        logger(1, 'DEBUG: posting form-folder-add form.');
        var url = '/api/folders';
        var type = 'POST';
    } else {
        logger(1, 'DEBUG: posting form-folder-rename form.');
        form_data['path'] = (form_data['path'] == '/') ? '/' + form_data['name'] : form_data['path'] + '/' + form_data['name'];
        var url = '/api/folders' + form_data['original'];
        var type = 'PUT';
    }
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: folder "' + form_data['name'] + '" added.');
                // Close the modal
                $(e.target).parents('.modal').attr('skipRedraw', true);
                $(e.target).parents('.modal').modal('hide');
                // Reload the folder list
                printPageLabList(form_data['path']);
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
});

// Submit import form
$(document).on('submit', '#form-import', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var form_data = new FormData();
    var form_name = 'import';
    var url = '/api/import';
    var type = 'POST';
    // Setting options: cannot use form2Array() because not using JSON to send data
    $('form :input[name^="' + form_name + '["]').each(function (id, object) {
        // INPUT name is in the form of "form_name[value]", get value only
        form_data.append($(this).attr('name').substr(form_name.length + 1, $(this).attr('name').length - form_name.length - 2), $(this).val());
    });
    // Add attachments
    $.each(ATTACHMENTS, function (key, value) {
        form_data.append(key, value);
    });
    $.ajax({
        timeout: LONGTIMEOUT,
        type: type,
        url: encodeURI(url),
        contentType: false, // Set content type to false as jQuery will tell the server its a query string request
        processData: false, // Don't process the files
        dataType: 'json',
        data: form_data,
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: labs imported.');
                // Close the modal
                $(e.target).parents('.modal').attr('skipRedraw', true);
                $(e.target).parents('.modal').modal('hide');
                // Reload the folder list
                printPageLabList($('#list-folders').attr('data-path'));
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
});

// Submit lab form
$(document).on('submit', '#form-lab-add, #form-lab-edit', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = form2Array('lab');
    if ($(this).attr('id') == 'form-lab-add') {
        logger(1, 'DEBUG: posting form-lab-add form.');
        var url = '/api/labs';
        var type = 'POST';
    } else {
        logger(1, 'DEBUG: posting form-lab-edit form.');
        var url = '/api/labs' + form_data['path'];
        var type = 'PUT';
    }

    if ($(this).attr('id') == 'form-node-add') {
        // If adding need to manage multiple add
        if (form_data['count'] > 1) {
            form_data['postfix'] = 1;
        } else {
            form_data['postfix'] = 0;
        }
    } else {
        // If editing need to post once
        form_data['count'] = 1;
        form_data['postfix'] = 0;
    }

    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: lab "' + form_data['name'] + '" saved.');
                // Close the modal
                $(e.target).parents('.modal').attr('skipRedraw', true);
                $(e.target).parents('.modal').modal('hide');
                if (type == 'POST') {
                    // Reload the lab list
                    logger(1, 'DEBUG: lab "' + form_data['name'] + '" renamed.');
                    printPageLabList(form_data['path']);
                } else if (basename(form_data['path']) != form_data['name'] + '.unl') {
                    // Lab has been renamed, need to close it.
                    logger(1, 'DEBUG: lab "' + form_data['name'] + '" renamed.');
                    if ($('#lab-viewport').length) {
                        $('#lab-viewport').attr({'data-path': dirname(form_data['path']) + '/' + form_data['name'] + '.unl'});
                        printLabTopology();
                    } else {
                        $.when(closeLab()).done(function () {
                            postLogin();
                            printLabPreview(dirname(form_data['path']) + '/' + form_data['name'] + '.unl');
                        }).fail(function (message) {
                            addModalError(message);
                        });

                    }

                } else {
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
});

// Submit network form
$(document).on('submit', '#form-network-add, #form-network-edit', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = form2Array('network');
    var promises = [];
    if ($(this).attr('id') == 'form-network-add') {
        logger(1, 'DEBUG: posting form-network-add form.');
        var url = '/api/labs' + lab_filename + '/networks';
        var type = 'POST';
    } else {
        logger(1, 'DEBUG: posting form-network-edit form.');
        var url = '/api/labs' + lab_filename + '/networks/' + form_data['id'];
        var type = 'PUT';
    }

    if ($(this).attr('id') == 'form-network-add') {
        // If adding need to manage multiple add
        if (form_data['count'] > 1) {
            form_data['postfix'] = 1;
        } else {
            form_data['postfix'] = 0;
        }
    } else {
        // If editing need to post once
        form_data['count'] = 1;
        form_data['postfix'] = 0;
    }

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
                    logger(1, 'DEBUG: network "' + form_data['name'] + '" saved.');
                    $(".network" + form_data['id'] + " td:nth-child(2)").text(form_data['name']);
                    $(".network" + form_data['id'] + " td:nth-child(3)").text(form_data['type']);
                    
                    // Close the modal
                    $('body').children('.modal').attr('skipRedraw', true);
                    $('body').children('.modal.second-win').modal('hide');
                    $('body').children('.modal.fade.in').focus();
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
        printLabTopology();
    });
    return false;  // Stop to avoid POST
});

// Submit node interfaces form
$(document).on('submit', '#form-node-connect', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = form2Array('interfc');
    var node_id = $('form :input[name="node_id"]').val();
    var url = '/api/labs' + lab_filename + '/nodes/' + node_id + '/interfaces';
    var type = 'PUT';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: node "' + node_id + '" saved.');
                // Close the modal
                $('body').children('.modal').attr('skipRedraw', true);
                $('body').children('.modal.second-win').modal('hide');
                $('body').children('.modal.fade.in').focus();
                addMessage(data['status'], data['message']);
                printLabTopology();
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
});

// Submit node form
$(document).on('submit', '#form-node-add, #form-node-edit', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var self = $(this);
    var lab_filename = $('#lab-viewport').attr('data-path');
    var form_data = form2Array('node');
    var promises = [];
    if ($(this).attr('id') == 'form-node-add') {
        logger(1, 'DEBUG: posting form-node-add form.');
        var url = '/api/labs' + lab_filename + '/nodes';
        var type = 'POST';
    } else {
        logger(1, 'DEBUG: posting form-node-edit form.');
        var url = '/api/labs' + lab_filename + '/nodes/' + form_data['id'];
        var type = 'PUT';
    }

    if ($(this).attr('id') == 'form-node-add') {
        // If adding need to manage multiple add
        if (form_data['count'] > 1) {
            form_data['postfix'] = 1;
        } else {
            form_data['postfix'] = 0;
        }
    } else {
        // If editing need to post once
        form_data['count'] = 1;
        form_data['postfix'] = 0;
    }

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
                    $('body').children('.modal').attr('skipRedraw', true);
                    $('body').children('.modal.second-win').modal('hide');
                    $('body').children('.modal.fade.in').focus();
                    addMessage(data['status'], data['message']);
                    $(".modal .node" + form_data['id'] + " td:nth-child(2)").text(form_data["name"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(3)").text(form_data["template"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(4)").text(form_data["image"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(5)").text(form_data["cpu"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(7)").text(form_data["nvram"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(8)").text(form_data["ram"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(9)").text(form_data["ethernet"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(10)").text(form_data["serial"]);
                    $(".modal .node" + form_data['id'] + " td:nth-child(11)").text(form_data["console"]);

                    $("#node" + form_data['id'] + " .node_name").html('<i class="node' + form_data['id'] + '_status glyphicon glyphicon-stop"></i>' + form_data['name'])
                    $("#node" + form_data['id'] + " a img").attr("src", "/images/icons/" + form_data['icon'])

                    $("#form-node-edit-table input[name='node[name]'][data-path='" + form_data['id'] + "']").val(form_data["name"])
                    $("#form-node-edit-table select[name='node[image]'][data-path='" + form_data['id'] + "']").val(form_data["image"])
                    $("#form-node-edit-table input[name='node[cpu]'][data-path='" + form_data['id'] + "']").val(form_data["cpu"])
                    $("#form-node-edit-table input[name='node[nvram]'][data-path='" + form_data['id'] + "']").val(form_data["nvram"])
                    $("#form-node-edit-table input[name='node[serial]'][data-path='" + form_data['id'] + "']").val(form_data["serial"])
                    $("#form-node-edit-table input[name='node[ethernet]'][data-path='" + form_data['id'] + "']").val(form_data["ethernet"])
                    $("#form-node-edit-table select[name='node[console]'][data-path='" + form_data['id'] + "']").val(form_data["console"])
                    $("#form-node-edit-table select[name='node[icon]'][data-path='" + form_data['id'] + "']").val(form_data["icon"])
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
        if (self.attr('id') == 'form-node-add') {
            printLabTopology();
        }
    });
    return false;  // Stop to avoid POST
});

// submit nodeList form by input focusout
$(document).on('focusout', '.configured-nodes-input', function(e){
    e.preventDefault();  // Prevent default behaviour
    if(!$(this).attr("readonly")){
        var id = $(this).attr('data-path')
        setNodeData(id);
    }
});

// submit nodeList form
$(document).on('change', '.configured-nods-select', function(e){
    e.preventDefault();  // Prevent default behaviour
    var id = $(this).attr('data-path')
    setNodeData(id);
});

// Submit config form
$(document).on('submit', '#form-node-config', function (e) {
    e.preventDefault();  // Prevent default behaviour
    saveLab('form-node-config');
});

// Submit login form
$(document).on('submit', '#form-login', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var form_data = form2Array('login');
    var url = '/api/auth/login';
    var type = 'POST';
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: user is authenticated.');
                // Close the modal
                $(e.target).parents('.modal').attr('skipRedraw', true);
                $(e.target).parents('.modal').modal('hide');
                $.when(getUserInfo()).done(function () {
                    // User is authenticated
                    logger(1, 'DEBUG: user authenticated.');
                    postLogin();
                }).fail(function () {
                    // User is not authenticated, or error on API
                    logger(1, 'DEBUG: loading authentication page.');
                    printPageAuthentication();
                });
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
});

// Submit user form
$(document).on('submit', '#form-user-add, #form-user-edit', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var form_data = form2Array('user');
    // Converting data
    if (form_data['expiration'] == '') {
        form_data['expiration'] = -1;
    } else {
        form_data['expiration'] = Math.floor($.datepicker.formatDate('@', new Date(form_data['expiration'])) / 1000);
    }
    if (form_data['pexpiration'] == '') {
        form_data['pexpiration'] = -1;
    } else {
        form_data['pexpiration'] = Math.floor($.datepicker.formatDate('@', new Date(form_data['pexpiration'])) / 1000);
    }
    if (form_data['pod'] == '') {
        form_data['pod'] = -1;
    }

    var username = form_data['username'];
    if ($(this).attr('id') == 'form-user-add') {
        logger(1, 'DEBUG: posting form-user-add form.');
        var url = '/api/users';
        var type = 'POST';
    } else {
        logger(1, 'DEBUG: posting form-user-edit form.');
        var url = '/api/users/' + username;
        var type = 'PUT';
    }
    $.ajax({
        timeout: TIMEOUT,
        type: type,
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                logger(1, 'DEBUG: user "' + username + '" saved.');
                // Close the modal
                $(e.target).parents('.modal').attr('skipRedraw', true);
                $(e.target).parents('.modal').modal('hide');
                // Reload the user list
                printUserManagement();
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
});

// Edit picture form
$('body').on('submit', '#form-picture-edit', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var lab_file = $('#lab-viewport').attr('data-path');
    var form_data = {};
    var picture_id = $(this).attr('data-path');

    // Setting options
    $('form :input[name^="picture["]').each(function (id, object) {
        // Standard options
        var field_name = $(this).attr('name').replace(/^picture\[([a-z]+)\]$/, '$1');
        form_data[field_name] = $(this).val();
    });

    // Get action URL
    var url = '/api/labs' + lab_file + '/pictures/' + picture_id;//form_data['id'];
    $.ajax({
        timeout: TIMEOUT,
        type: 'PUT',
        url: encodeURI(url),
        dataType: 'json',
        data: JSON.stringify(form_data),
        success: function (data) {
            if (data['status'] == 'success') {
                // Fetching ok
                addMessage('SUCCESS', 'Picture "' + form_data['name'] + '" saved.');
                printPictureInForm(picture_id);
                $('ul.map a.action-pictureget[data-path="' + picture_id + '"]').attr('title', form_data['name']);
                $('ul.map a.action-pictureget[data-path="' + picture_id + '"]').text(form_data['name'].split(" ")[0]);
                $('body').children('.modal.second-win').modal('hide');
                // Picture saved  -> reopen this page (not reload, or will be posted twice)
                // window.location.href = '/lab_edit.php' + window.location.search;
            } else {
                // Fetching failed
                addMessage('DANGER', data['status']);
            }
        },
        error: function (data) {
            addMessage('DANGER', getJsonMessage(data['responseText']));
        }
    });

    // Hide and delete the modal (or will be posted twice)
    $('#form_frame > div').modal('hide');

    // Stop or form will follow the action link
    return false;
});

// Edit picture form
$('body').on('submit', '#form-picture-delete', function (e) {
    e.preventDefault();  // Prevent default behaviour
    var lab_filename = $('#lab-viewport').attr('data-path');
    var picture_id = $(this).attr('data-path');
    var picture_name = $('li a[data-path="' + picture_id + '"]').attr("title");
    $.when(deletePicture(lab_filename, picture_id)).done(function () {
        addMessage('SUCCESS', 'Picture "' + picture_name + '" deleted.');
        $('li a[data-path="' + picture_id + '"]').parent().remove();
        $("#config-data").html("");
    }).fail(function (message) {
        addModalError(message);
    });

    // Hide and delete the modal (or will be posted twice)
    $('body').children('.modal.second-win').modal('hide');

    // Stop or form will follow the action link
    return false;
});

/*******************************************************************************
 * Custom Shape/Text Functions
 * *****************************************************************************/
// Add Custom Shape
$('body').on('submit', '.custom-shape-form', function (e) {
    var shape_options = {}
        , shape_html
        , dashed = ''
        , dash_spase_length = '10'
        , dash_line_length = '10'
        , z_index = 999
        , radius
        , coordinates
        , current_lab
        , customShape_id = ''
        , generateName = false
        ;

    shape_options['id'] = new Date().getTime();
    shape_options['shape_type'] = $('.custom-shape-form .shape-type-select').val();
    // shape_options['shape_name'] = $('.custom-shape-form .shape_name').val();
    if(!$('.custom-shape-form .shape_name').val()){
        generateName = true;
        shape_options['shape_name'] = $('.custom-shape-form .shape-type-select').val() + customShape_id;
    } else {
        shape_options['shape_name'] = $('.custom-shape-form .shape_name').val();
    }
    shape_options['shape_border_type'] = $('.custom-shape-form .border-type-select').val();
    shape_options['shape_border_color'] = $('.custom-shape-form .shape_border_color').val();
    shape_options['shape_background_color'] = $('.custom-shape-form .shape_background_color').val();
    shape_options['shape_width/height'] = 120;
    shape_options['shape_border_width'] = $('.custom-shape-form .shape_border_width').val();
    shape_options['shape_left_coordinate'] = $('.custom-shape-form .left-coordinate').val();
    shape_options['shape_top_coordinate'] = $('.custom-shape-form .top-coordinate').val();

    coordinates = 'position:absolute;left:' + shape_options['shape_left_coordinate'] + 'px;top:' + shape_options['shape_top_coordinate'] + 'px;';

    if (shape_options['shape_border_type'] == 'dashed') {
        dashed = ' stroke-dasharray = "' + dash_line_length + ',' + dash_spase_length + '" '
    } else {
        dashed = ''
    }

    if (shape_options['shape_type'] == 'square') {
        shape_html =
            '<div id="customShape' + shape_options['id'] + '" class="customShape context-menu" data-path="' + customShape_id + '" ' +
            'style="display:inline;z-index:' + z_index + ';' + coordinates + '" ' +
            'width="' + shape_options['shape_width/height'] + 'px" height="' + shape_options['shape_width/height'] + 'px" >' +
            '<svg width="' + shape_options['shape_width/height'] + '" height="' + shape_options['shape_width/height'] + '">' +
            '<rect width="' + shape_options['shape_width/height'] + '" ' +
            'height="' + shape_options['shape_width/height'] + '" ' +
            'fill ="' + shape_options['shape_background_color'] + '" ' +
            'stroke-width ="' + shape_options['shape_border_width'] + '" ' +
            'stroke ="' + shape_options['shape_border_color'] + '" ' + dashed +
            '"/>' +
            'Sorry, your browser does not support inline SVG.' +
            '</svg>' +
            '</div>';
    } else if (shape_options['shape_type'] == 'circle') {
        radius = shape_options['shape_width/height'] / 2 - shape_options['shape_border_width'] / 2;

        shape_html =
            '<div id="customShape' + shape_options['id'] + '" class="customShape context-menu" data-path="' + customShape_id + '" ' +
            'style="display:inline;z-index:' + z_index + ';' + coordinates + '"' +
            'width="' + shape_options['shape_width/height'] + 'px" height="' + shape_options['shape_width/height'] + 'px" >' +
            '<svg width="' + shape_options['shape_width/height'] + '" height="' + shape_options['shape_width/height'] + '">' +
            '<ellipse cx="' + (radius + shape_options['shape_border_width'] / 2 ) + '" ' +
            'cy="' + (radius + shape_options['shape_border_width'] / 2 ) + '" ' +
            'rx="' + radius + '" ' +
            'ry="' + radius + '" ' +
            'stroke ="' + shape_options['shape_border_color'] + '" ' +
            'stroke-width="' + shape_options['shape_border_width'] / 2 + '" ' + dashed +
            'fill ="' + shape_options['shape_background_color'] + '" ' +
            '/>' +
            'Sorry, your browser does not support inline SVG.' +
            '</svg>' +
            '</div>';
    }

    current_lab = $('#lab-viewport').attr('data-path');

    // Get action URL
    var url = '/api/labs' + current_lab + '/textobjects';
    var form_data = {};

    form_data['data'] = shape_html;
    form_data['name'] = shape_options["shape_name"];
    form_data['type'] = shape_options["shape_type"];

    createTextObject(form_data).done(function (textObjData) {
        $('#lab-viewport').prepend(shape_html);

        var $added_shape = $("#customShape" + shape_options['id']);
        $added_shape
            .draggable({
                stop: textObjectDragStop
            })
            .resizable({
                autoHide: true,
                resize: function (event, ui) {
                    textObjectResize(event, ui, shape_options);
                },
                stop: textObjectDragStop
            });

        getTextObjects().done(function (textObjects) {
            $added_shape.attr("id", "customShape" + textObjData.id);
            $added_shape.attr("data-path", textObjData.id);
            var nameObj = generateName ? shape_options['shape_type'] + textObjData.id.toString() : shape_options['shape_name'];
            $added_shape.attr("name", nameObj);
            $added_shape.attr("data-path", textObjData.id);
            var new_data = document.getElementById($added_shape.attr("id")).outerHTML;
            
            editTextObject(textObjData.id, {data: new_data, name: nameObj})
            .done(function(){
                if ($("customShape" + textObjData.id).length > 1) {
                    // reload lab
                    addMessage('warning', MESSAGES[156]);
                    printLabTopology();
                }

                // Hide and delete the modal (or will be posted twice)
                $('body').children('.modal').modal('hide');
            }).fail(function(){

            });
        }).fail(function (message) {
            addMessage('DANGER', getJsonMessage(message));
        });
    }).done(function () {
        addMessage('SUCCESS', 'Lab has been saved (60023).');
    }).fail(function (message) {
        addMessage('DANGER', getJsonMessage(message));
    });

    // Stop or form will follow the action link
    return false;
});

// Add Text
$('body').on('submit', '.add-text-form', function (e) {
    var text_options = {}
        , text_html
        , coordinates
        , z_index = 1001
        , text_style = ''
        , customShape_id = ''
        , form_data = {}
        ;

    text_options['id'] = new Date().getTime();
    text_options['text_left_coordinate'] = $('.add-text-form .left-coordinate').val();
    text_options['text_top_coordinate'] = $('.add-text-form .top-coordinate').val();
    text_options['text'] = $('.add-text-form .main-text').val().replace(/\n/g, '<br>');
    text_options['alignment'] = 'center';
    text_options['vertical-alignment'] = 'top';
    text_options['color'] = $('.add-text-form .text_font_color').val();
    text_options['background-color'] = $('.add-text-form .text_background_color').val();
    text_options['text-size'] = $('.add-text-form .text_font_size').val();
    text_options['text-style'] = $('.add-text-form .text-font-style-select').val();

    if (text_options['text-style'] == 'normal') {
        text_style = 'font-weight: normal;';
    } else if (text_options['text-style'] == 'bold') {
        text_style = 'font-weight: bold;';
    } else if (text_options['text-style'] == 'italic') {
        text_style = 'font-style: italic;';
    } else {
        text_style = '';
    }

    coordinates = 'position:absolute;left:' + text_options['text_left_coordinate'] + 'px;top:' + text_options['text_top_coordinate'] + 'px;';

    text_html =
        '<div id="customText' + text_options['id'] + '" class="customShape customText context-menu" data-path="' + customShape_id + '" ' +
        'style="display:inline;' + coordinates + ' cursor:move; ;z-index:' + z_index + ';" >' +
        '<p align="' + text_options['alignment'] + '" style="' +
        'vertical-align:' + text_options['vertical-alignment'] + ';' +
        'color:' + text_options['color'] + ';' +
        'background-color:' + text_options['background-color'] + ';' +
        'font-size:' + text_options['text-size'] + 'px;' +
        text_style + '">' +
        text_options['text'] +
        '</p>' +
        '</div>';

    form_data['data'] = text_html;
    form_data['name'] = "txt " + ($(".customShape").length + 1);
    form_data['type'] = "text";

    createTextObject(form_data).done(function (data) {
        $('#lab-viewport').prepend(text_html);

        var $added_shape = $("#customText" + text_options['id']);
        $added_shape
            .draggable({
                stop: textObjectDragStop
            })
            .resizable({
                autoHide: true,
                resize: function (event, ui) {
                    textObjectResize(event, ui, text_options);
                },
                stop: textObjectDragStop
            });

        getTextObjects().done(function (textObjects) {
            var id = data.id;
            $added_shape.attr("id", "customText" + id);
            $added_shape.attr("data-path", id);

            if ($("customText" + id).length > 1) {
                addMessage('warning', MESSAGES[156]);
                printLabTopology();
            }

            // Hide and delete the modal (or will be posted twice)
            $('body').children('.modal').modal('hide');
        }).fail(function (message) {
            addMessage('DANGER', getJsonMessage(message));
        });
    }).done(function () {
        addMessage('SUCCESS', 'Lab has been saved (60023).');
    }).fail(function (message) {
        addMessage('DANGER', getJsonMessage(message));
    });

    return false;
});

// Edit Custom Shape/Edit Text

$('body').on('click', '.action-textobjectduplicate', function (e) {
    logger(1, 'DEBUG: action = action-textobjectduplicate');
    var id = $(this).attr('data-path')
        , $selected_shape
        , $duplicated_shape
        , new_id
        , textObjectsLength
        , shape_border_width
        , form_data = {}
        , new_data_html;

    $selected_shape = $("#customShape" + id + " svg").children();
    shape_border_width = $("#customShape" + id + " svg").children().attr('stroke-width');

    function getSizeObj(obj) {
        var size = 0, key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) size++;
        }
        return size;
    }

    if ($("#customShape" + id).length) {
        $selected_shape = $("#customShape" + id);
        $selected_shape.resizable("destroy");
        $selected_shape.draggable("destroy");
        $duplicated_shape = $selected_shape.clone();

        $selected_shape.draggable({
            stop: textObjectDragStop
        }).resizable({
            autoHide: true,
            resize: function (event, ui) {
                textObjectResize(event, ui, {"shape_border_width": shape_border_width});
            },
            stop: textObjectDragStop
        });

        getTextObjects().done(function (textObjects) {

            textObjectsLength = getSizeObj(textObjects);

            for (var i = 1; i <= textObjectsLength; i++) {
                if (textObjects['' + i + ''] == undefined) {
                    new_id = i;
                    break
                }
                if (textObjectsLength == i) {
                    new_id = i + 1;
                }
            }

            $duplicated_shape.css('top', parseInt($selected_shape.css('top')) + parseInt($selected_shape.css('width')) / 2);
            $duplicated_shape.css('left', parseInt($selected_shape.css('left')) + parseInt($selected_shape.css('height')) / 2);
            $duplicated_shape.attr("id", "customShape" + new_id);
            $duplicated_shape.attr("data-path", new_id);

            new_data_html = $duplicated_shape[0].outerHTML;
            form_data['data'] = new_data_html;
            form_data['name'] = textObjects[id]["name"];
            form_data['type'] = textObjects[id]["type"];

            createTextObject(form_data).done(function () {
                $('#lab-viewport').prepend(new_data_html);

                $('#customShape' + new_id).draggable({
                    stop: textObjectDragStop
                }).resizable({
                    autoHide: true,
                    resize: function (event, ui) {
                        textObjectResize(event, ui, {"shape_border_width": shape_border_width});
                    },
                    stop: textObjectDragStop
                });
                addMessage('SUCCESS', 'Lab has been saved (60023).');
            }).fail(function (message) {
                addMessage('DANGER', getJsonMessage(message));
            })
        }).fail(function (message) {
            addMessage('DANGER', getJsonMessage(message));
        });
    } else if ($("#customText" + id).length) {
        $selected_shape = $("#customText" + id);
        $selected_shape.resizable("destroy");
        $selected_shape.draggable("destroy");
        $duplicated_shape = $selected_shape.clone();

        $selected_shape.draggable({
            stop: textObjectDragStop
        }).resizable({
            autoHide: true,
            resize: function (event, ui) {
                textObjectResize(event, ui, {"shape_border_width": shape_border_width});
            },
            stop: textObjectDragStop
        });

        getTextObjects().done(function (textObjects) {

            textObjectsLength = getSizeObj(textObjects);

            for (var i = 1; i <= textObjectsLength; i++) {
                if (textObjects['' + i + ''] == undefined) {
                    new_id = i;
                    break
                }
                if (textObjectsLength == i) {
                    new_id = i + 1;
                }
            }

            $duplicated_shape.css('top', parseInt($selected_shape.css('top')) + parseInt($selected_shape.css('width')) / 2);
            $duplicated_shape.css('left', parseInt($selected_shape.css('left')) + parseInt($selected_shape.css('height')) / 2);
            $duplicated_shape.attr("id", "customText" + new_id);
            $duplicated_shape.attr("data-path", new_id);

            new_data_html = $duplicated_shape[0].outerHTML;
            form_data['data'] = new_data_html;
            form_data['name'] = 'txt ' + new_id;
            form_data['type'] = textObjects[id]["type"];

            createTextObject(form_data).done(function () {
                $('#lab-viewport').prepend(new_data_html);

                $('#customText' + new_id).draggable({
                    stop: textObjectDragStop
                }).resizable({
                    autoHide: true,
                    resize: function (event, ui) {
                        textObjectResize(event, ui, {"shape_border_width": shape_border_width});
                    },
                    stop: textObjectDragStop
                });
                addMessage('SUCCESS', 'Lab has been saved (60023).');
            }).fail(function (message) {
                addMessage('DANGER', getJsonMessage(message));
            })
        }).fail(function (message) {
            addMessage('DANGER', getJsonMessage(message));
        });
    }
    $('#context-menu').remove();
});

$('body').on('click', '.action-textobjecttoback', function (e) {
    logger(1, 'DEBUG: action = action-textobjecttoback');
    var id = $(this).attr('data-path')
        , old_z_index
        , shape_border_width
        , new_data
        , $selected_shape = '';

    shape_border_width = $("#customShape" + id + " svg").children().attr('stroke-width');
    if ($("#customShape" + id).length) {
        $selected_shape = $("#customShape" + id);
        old_z_index = $selected_shape.css('z-index');
        $selected_shape.css('z-index', parseInt(old_z_index) - 1);
        $selected_shape.resizable("destroy");
        new_data = document.getElementById("customShape" + id).outerHTML;
        $selected_shape.resizable({
            autoHide: true,
            resize: function (event, ui) {
                textObjectResize(event, ui, {"shape_border_width": shape_border_width});
            },
            stop: textObjectDragStop
        });
    } else if ($("#customText" + id).length) {
        $selected_shape = $("#customText" + id);
        old_z_index = $selected_shape.css('z-index');
        $selected_shape.css('z-index', parseInt(old_z_index) - 1);
        $selected_shape.resizable("destroy");
        new_data = document.getElementById("customText" + id).outerHTML;
        $selected_shape.resizable({
            autoHide: true,
            resize: function (event, ui) {
                textObjectResize(event, ui, {"shape_border_width": 5});
            },
            stop: textObjectDragStop
        });
    }
    editTextObject(id, {data: new_data}).done(function () {

    }).fail(function () {
        addMessage('DANGER', getJsonMessage(message));
    });
    $('#context-menu').remove();
});

$('body').on('click', '.action-textobjecttofront', function (e) {
    logger(1, 'DEBUG: action = action-textobjecttofront');
    var id = $(this).attr('data-path')
        , old_z_index
        , shape_border_width
        , new_data
        , $selected_shape = '';

    shape_border_width = $("#customShape" + id + " svg").children().attr('stroke-width');
    if ($("#customShape" + id).length) {
        $selected_shape = $("#customShape" + id);
        old_z_index = $selected_shape.css('z-index');
        $selected_shape.css('z-index', parseInt(old_z_index) + 1);
        $selected_shape.resizable("destroy");
        new_data = document.getElementById("customShape" + id).outerHTML;
        $('#context-menu').remove();
        $selected_shape.resizable({
            autoHide: true,
            resize: function (event, ui) {
                textObjectResize(event, ui, {"shape_border_width": shape_border_width});
            },
            stop: textObjectDragStop
        });
    } else if ($("#customText" + id).length) {
        $selected_shape = $("#customText" + id);
        old_z_index = $selected_shape.css('z-index');
        $selected_shape.css('z-index', parseInt(old_z_index) + 1);
        $selected_shape.resizable("destroy");
        new_data = document.getElementById("customText" + id).outerHTML;
        $selected_shape.resizable({
            autoHide: true,
            resize: function (event, ui) {
                textObjectResize(event, ui, {"shape_border_width": 5});
            },
            stop: textObjectDragStop
        });
        $('#context-menu').remove();
    }
    editTextObject(id, {data: new_data}).done(function () {

    }).fail(function () {
        addMessage('DANGER', getJsonMessage(message));
    });
    $('#context-menu').remove();
});

$('body').on('click', '.action-textobjectedit', function (e) {
    logger(1, 'DEBUG: action = action-textobjectedit');
    var id = $(this).attr('data-path');

    if ($("#customShape" + id).length) {
        printFormEditCustomShape(id);
    } else if ($("#customText" + id).length) {
        printFormEditText(id);
    }
    $('#context-menu').remove();
});

$('body').on('click', '.action-textobjectdelete', function (e) {
    logger(1, 'DEBUG: action = action-textobjectdelete');
    var id = $(this).attr('data-path')
        , $table = $(this).closest('table')
        , $selected_shape = '';
    if ($("#customShape" + id).length) {
        $selected_shape = $("#customShape" + id);
    } else if ($("#customText" + id).length) {
        $selected_shape = $("#customText" + id);
    }
    deleteTextObject(id).done(function () {
        if ($(this).parent('tr')) {
            $('.textObject' + id, $table).remove();
        }
        $('#context-menu').remove();
        $selected_shape.remove();
    }).fail(function (message) {
        addModalError(message);
    });
});

$('body').on('contextmenu', '.edit-custom-shape-form, .edit-custom-text-form, #context-menu', function (e) {
    e.preventDefault();
    e.stopPropagation();
});

/*******************************************************************************
 * Text Edit Form
 * *****************************************************************************/

$('body').on('click', '.edit-custom-text-form .btn-align-left', function (e) {
    logger(1, 'DEBUG: action = action-set/delete left alignment');
    var id = $(this).attr('data-path');

    $("#customText" + id + " p").attr('align', 'left');

    if ($('.edit-custom-text-form .btn-align-left').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-left').removeClass('active');
    } else if ($('.edit-custom-text-form .btn-align-center').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-center').removeClass('active');
    } else if ($('.edit-custom-text-form .btn-align-right').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-right').removeClass('active');
    }
    $('.edit-custom-text-form .btn-align-left').addClass('active');
});

$('body').on('click', '.edit-custom-text-form .btn-align-center', function (e) {
    logger(1, 'DEBUG: action = action-set/delete center alignment');
    var id = $(this).attr('data-path');
    $("#customText" + id + " p").attr('align', 'center');

    if ($('.edit-custom-text-form .btn-align-left').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-left').removeClass('active');
    } else if ($('.edit-custom-text-form .btn-align-center').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-center').removeClass('active');
    } else if ($('.edit-custom-text-form .btn-align-right').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-right').removeClass('active');
    }
    $('.edit-custom-text-form .btn-align-center').addClass('active');
});

$('body').on('click', '.edit-custom-text-form .btn-align-right', function (e) {
    logger(1, 'DEBUG: action = action-set/delete left alignment');
    var id = $(this).attr('data-path');
    $("#customText" + id + " p").attr('align', 'right');

    if ($('.edit-custom-text-form .btn-align-left').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-left').removeClass('active');
    } else if ($('.edit-custom-text-form .btn-align-center').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-center').removeClass('active');
    } else if ($('.edit-custom-text-form .btn-align-right').hasClass('active')) {
        $('.edit-custom-text-form .btn-align-right').removeClass('active');
    }
    $('.edit-custom-text-form .btn-align-right').addClass('active');
});

$('body').on('click', '.edit-custom-text-form .btn-text-italic', function (e) {
    logger(1, 'DEBUG: action = action-set/delete font style');
    var id = $(this).attr('data-path');

    if ($('.edit-custom-text-form .btn-text-italic').hasClass('active')) {
        $('.edit-custom-text-form .btn-text-italic').removeClass('active');
        $("#customText" + id + " p").css('font-style', 'normal');
    } else if (!$('.edit-custom-text-form .btn-text-italic').hasClass('active')) {
        $('.edit-custom-text-form .btn-text-italic').addClass('active');
        $("#customText" + id + " p").css('font-style', 'italic');
    }
});

$('body').on('click', '.edit-custom-text-form .btn-text-bold', function (e) {
    logger(1, 'DEBUG: action = action-set/delete font weight');
    var id = $(this).attr('data-path');

    if ($('.edit-custom-text-form .btn-text-bold').hasClass('active')) {
        $('.edit-custom-text-form .btn-text-bold').removeClass('active');
        $("#customText" + id + " p").css('font-weight', 'normal');
    } else if (!$('.edit-custom-text-form .btn-text-bold').hasClass('active')) {
        $('.edit-custom-text-form .btn-text-bold').addClass('active');
        $("#customText" + id + " p").css('font-weight', 'bold');
    }
});

$('body').on('change', '.edit-custom-text-form .text-z_index-input', function (e) {
    logger(1, 'DEBUG: action = action-change text z-index');
    var id = $(this).attr('data-path');
    $("#customText" + id).css('z-index', parseInt($(".edit-custom-text-form .text-z_index-input").val()) + 1000);
});

$('body').on('change', '.edit-custom-text-form .text_background_color', function (e) {
    logger(1, 'DEBUG: action = action-change text background color');
    var id = $(this).attr('data-path');
    $('.edit-custom-text-form .text_background_transparent').removeClass('active  btn-success').text('Off');
    $("#customText" + id + " p").css('background-color', $(".edit-custom-text-form .text_background_color").val());
});

$('body').on('click', '.edit-custom-text-form .text_background_transparent', function (e) {
    logger(1, 'DEBUG: action = action-change text background color');
    var id = $(this).attr('data-path');

    if ($('.edit-custom-text-form .text_background_transparent').hasClass('active')) {
        $('.edit-custom-text-form .text_background_transparent').removeClass('active  btn-success').text('Off');
        $("#customText" + id + " p").css('background-color', $(".edit-custom-text-form .text_background_color").val());
    } else {
        $('.edit-custom-text-form .text_background_transparent').addClass('active  btn-success').text('On');
        $("#customText" + id + " p").css('background-color', hex2rgb($(".edit-custom-text-form .text_background_color").val(), 0));
    }
});

$('body').on('change', '.edit-custom-text-form .text_color', function (e) {
    logger(1, 'DEBUG: action = action-change text color');
    var id = $(this).attr('data-path');
    $("#customText" + id + " p").css('color', $(".edit-custom-text-form .text_color").val());
});

$('body').on('change', '.edit-custom-text-form .text-rotation-input', function (e) {
    logger(1, 'DEBUG: action = action-rotate shape');
    var id = $(this).attr('data-path')
        , angle = parseInt(this.value);

    $("#customText" + id).css("-ms-transform", "rotate(" + angle + "deg)");
    $("#customText" + id).css("-webkit-transform", "rotate(" + angle + "deg)");
    $("#customText" + id).css("transform", "rotate(" + angle + "deg)");
});

$('body').on('click', '.edit-custom-text-form .cancelForm', function (e) {
    logger(1, 'DEBUG: action = action-return old text values');
    var id = $(this).attr('data-path')
        , angle = $('.edit-custom-text-form .firstTextValues-rotation').val();

    //Return z-index value
    $("#customText" + id).css('z-index', parseInt($('.edit-custom-text-form .firstTextValues-z_index').val()));

    // Return alignment value
    $('.edit-custom-text-form .btn-align-left').removeClass('active');
    $('.edit-custom-text-form .btn-align-center').removeClass('active');
    $('.edit-custom-text-form .btn-align-right').removeClass('active');

    if ($('.edit-custom-text-form .firstTextValues-align').val() == "left") {
        $("#customText" + id + " p").attr('align', 'left');
    } else if ($('.edit-custom-text-form .firstTextValues-align').val() == "center") {
        $("#customText" + id + " p").attr('align', 'center');
    } else if ($('.edit-custom-text-form .firstTextValues-align').val() == "right") {
        $("#customText" + id + " p").attr('align', 'right');
    }

    // Return text type value
    $('.edit-custom-text-form .btn-text-bold').removeClass('active');
    $('.edit-custom-text-form .btn-text-italic').removeClass('active');

    if ($('.edit-custom-text-form .firstTextValues-italic').val()) {
        $("#customText" + id + " p").css('font-style', 'italic');
    } else if ($('.edit-custom-text-form .firstTextValues-bold').val()) {
        $("#customText" + id + " p").css('font-weight', 'bold');
    }

    // Return text color value
    $("#customText" + id + " p").css('color', $('.edit-custom-text-form .firstTextValues-color').val());

    // Return background color value
    $("#customText" + id + " p").css('background-color', $(".edit-custom-text-form .firstTextValues-background-color").val());

    // Return rotation angle
    $("#customText" + id).css("-ms-transform", "rotate(" + angle + "deg)");
    $("#customText" + id).css("-webkit-transform", "rotate(" + angle + "deg)");
    $("#customText" + id).css("transform", "rotate(" + angle + "deg)");

    // Remove edit class
    $("#customText" + id).removeClass('in-editing');

    $('.edit-custom-text-form').remove();
});

$('body').on('click', '.edit-custom-text-form-save', function (e) {
    logger(1, 'DEBUG: action = action-save new text values');
    var id = $(this).attr('data-path')
        , $selected_shape = $("#customText" + id)
        , new_data;

    $selected_shape.resizable("destroy");
    $selected_shape.removeClass('in-editing');
    new_data = document.getElementById("customText" + id).outerHTML;
    $selected_shape.resizable({
        autoHide: true,
        resize: function (event, ui) {
            textObjectResize(event, ui, {"shape_border_width": 5});
        },
        stop: textObjectDragStop
    });

    editTextObject(id, {data: new_data}).done(function () {
        addMessage('SUCCESS', 'Lab has been saved (60023).');
    }).fail(function (message) {
        addModalError(message);
    });
    $('.edit-custom-text-form').remove();
});

$(document).on('dblclick', '.customText', function (e) {
    logger(1, 'DEBUG: action = action-edit text');
    var id = $(this).attr('data-path')
        , $selectedCustomText = $("#customText" + id + " p")
        ;

    // Disable draggable and resizable before sending request
    try {
        $(this).draggable("destroy").resizable("destroy");
    }
    catch (e) {
        console.warn(e);
    }

    $selectedCustomText.attr('contenteditable', 'true').focus().addClass('editable');
});

$(document).on('paste', '[contenteditable="true"]', function (e) {
    e.preventDefault();
    var text = null;
    text = (e.originalEvent || e).clipboardData.getData('text/plain') || prompt('Paste Your Text Here');
    document.execCommand("insertText", false, text);
});

$(document).on('focusout', '.editable', function (e) {
    var new_data
        , id = $(this).parent().attr('data-path')
        , $selected_shape = $("#customText" + id)
        , innerHtml = $("p", $selected_shape).html()
        , textLines = 0
        ;

    $("#customText" + id + " p").removeClass('editable');
    $("#customText" + id + " p").attr('contenteditable', 'false');

    // trim whitespace in the start and end of string
    innerHtml = innerHtml.replace(/^(<br>)+/, "").replace(/(<br>)+$/, "");

    // replace all HTML tags except <br>, replace closing DIV </div> with br
    innerHtml = innerHtml.replace(/<(\w+\b)[^>]*>([^<>]*)<\/\1>/g, '$2<br>');

    if (!innerHtml) {
        innerHtml = "<br>";
    }

    $("p", $selected_shape).html(innerHtml);
    // Calculate and apply new Width / Height based lines count
    textLines = $("br", $selected_shape).size();
    if (textLines) {
        // multilines text
        $selected_shape.css("height", parseFloat($("p", $selected_shape).css("font-size")) * (textLines * 1.5 + 1) + "px");
    }
    else {
        // 1 line text
        $selected_shape.css("height", parseFloat($("p", $selected_shape).css("font-size")) * 2 + "px");
    }
    $selected_shape.css("width", "auto");

    new_data = document.getElementById("customText" + id).outerHTML;
    editTextObject(id, {data: new_data}).done(function () {
        addMessage('SUCCESS', 'Lab has been saved (60023).');
    }).fail(function (message) {
        addModalError(message);
    });

    $selected_shape.draggable({
        stop: textObjectDragStop
    }).resizable({
        autoHide: true,
        resize: function (event, ui) {
            textObjectResize(event, ui, {"shape_border_width": 5});
        },
        stop: textObjectDragStop
    });
});

// Fix "Enter" behaviour in contenteditable elements
$(document).on('keydown', '.editable', function (e) {
    var editableText = $('.editable')
        ;

    if (KEY_CODES.enter == e.which) {
        function brQuantity() {
            if (parseInt(editableText.text().length) <= getCharacterOffsetWithin(window.getSelection().getRangeAt(0), document.getElementsByClassName("editable")[0])) {
                return '<br><br>'
            } else {
                return '<br>'
            }
        };
        document.execCommand('insertHTML', false, brQuantity());
        return false;
    }
});

//Get caret position
// node - need to get by pure js
function getCharacterOffsetWithin(range, node) {
    var treeWalker = document.createTreeWalker(
        node,
        NodeFilter.SHOW_TEXT,
        function (node) {
            var nodeRange = document.createRange();
            nodeRange.selectNodeContents(node);
            return nodeRange.compareBoundaryPoints(Range.END_TO_END, range) < 1 ?
                NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        },
        false
    );

    var charCount = 0;
    while (treeWalker.nextNode()) {
        charCount += treeWalker.currentNode.length;
    }
    if (range.startContainer.nodeType == 3) {
        charCount += range.startOffset;
    }
    return charCount;
}

/*******************************************************************************
 * Custom Shape Edit Form
 * *****************************************************************************/

$('body').on('click', '.edit-custom-shape-form .cancelForm', function (e) {
    logger(1, 'DEBUG: action = action-return old shape values');
    var id = $(this).attr('data-path')
        , angle = $(".edit-custom-shape-form .firstShapeValues-rotation").val();

    //Return z-index value
    $("#customShape" + id).css('z-index', parseInt($('.edit-custom-shape-form .firstShapeValues-z_index').val()));

    //Return border width value
    if ($("#customShape" + id + " svg").children().attr('cx')) {
        $("#customShape" + id + " svg").children().attr('stroke-width', $('.edit-custom-shape-form .firstShapeValues-border-width').val() / 2);
    } else {
        $("#customShape" + id + " svg").children().attr('stroke-width', $('.edit-custom-shape-form .firstShapeValues-border-width').val());
    }

    //Return border type value
    if ($('.edit-custom-shape-form .firstShapeValues-border-type').val() == 'solid') {
        $("#customShape" + id + " svg").children().removeAttr('stroke-dasharray');
    } else if ($('.edit-custom-shape-form .firstShapeValues-border-type').val() == 'dashed') {
        if (!$("#customShape" + id + " svg").children().attr('stroke-dasharray')) {
            $("#customShape" + id + " svg").children().attr('stroke-dasharray', '10,10');
        }
    }

    //Return border color value
    $("#customShape" + id + " svg").children().attr('stroke', $(".edit-custom-shape-form .firstShapeValues-border-color").val());

    //Return background color value
    $("#customShape" + id + " svg").children().attr('fill', $(".edit-custom-shape-form .firstShapeValues-background-color").val());

    //Return rotation angle
    $("#customShape" + id).css("-ms-transform", "rotate(" + angle + "deg)");
    $("#customShape" + id).css("-webkit-transform", "rotate(" + angle + "deg)");
    $("#customShape" + id).css("transform", "rotate(" + angle + "deg)");

    $("#customShape" + id).removeClass('in-editing');

    $('.edit-custom-shape-form').remove();
});

$('body').on('change', '.edit-custom-shape-form .shape-z_index-input', function (e) {
    logger(1, 'DEBUG: action = action-change shape z-index');
    var id = $(this).attr('data-path');
    $("#customShape" + id).css('z-index', parseInt($(".edit-custom-shape-form .shape-z_index-input").val()) + 1000);
});

$('body').on('change', '.edit-custom-shape-form .shape_border_width', function (e) {
    logger(1, 'DEBUG: action = action-change shape border width');
    var id = $(this).attr('data-path');

    if ($("#customShape" + id + " svg").children().attr('cx')) {
        $("#customShape" + id + " svg").children().attr('stroke-width', $(".edit-custom-shape-form .shape_border_width").val() / 2);
    } else {
        $("#customShape" + id + " svg").children().attr('stroke-width', $(".edit-custom-shape-form .shape_border_width").val());
    }
});

$('body').on('change', '.edit-custom-shape-form .border-type-select', function (e) {
    logger(1, 'DEBUG: action = action-change shape border type');
    var id = $(this).attr('data-path');

    if ($(".edit-custom-shape-form .border-type-select").val() == 'solid') {
        if ($("#customShape" + id + " svg").children().attr('stroke-dasharray')) {
            $("#customShape" + id + " svg").children().removeAttr('stroke-dasharray');
        }
    } else if ($(".edit-custom-shape-form .border-type-select").val() == 'dashed') {
        if (!$("#customShape" + id + " svg").children().attr('stroke-dasharray')) {
            $("#customShape" + id + " svg").children().attr('stroke-dasharray', '10,10');
        }
    }
});

$('body').on('change', '.edit-custom-shape-form .shape_background_color', function (e) {
    logger(1, 'DEBUG: action = action-change shape background color');
    var id = $(this).attr('data-path');
    $("#customShape" + id + " svg").children().attr('fill', $(".edit-custom-shape-form .shape_background_color").val());
    $('.edit-custom-shape-form .shape_background_transparent').removeClass('active  btn-success').text('Off');
});

$('body').on('click', '.edit-custom-shape-form .shape_background_transparent', function (e) {
    logger(1, 'DEBUG: action = action-change shape background color');
    var id = $(this).closest('form').attr('data-path');

    if ($('.edit-custom-shape-form .shape_background_transparent').hasClass('active')) {
        $('.edit-custom-shape-form .shape_background_transparent').removeClass('active  btn-success').text('Off');
        $("#customShape" + id + " svg").children().attr('fill', $(".edit-custom-shape-form .shape_background_color").val());
    }
    else {
        $('.edit-custom-shape-form .shape_background_transparent').addClass('active  btn-success').text('On');
        $("#customShape" + id + " svg").children().attr('fill', hex2rgb($(".edit-custom-shape-form .shape_background_color").val(), 0));
    }
});

$('body').on('change', '.edit-custom-shape-form .shape_border_color', function (e) {
    logger(1, 'DEBUG: action = action-change shape border color');
    var id = $(this).attr('data-path');
    $("#customShape" + id + " svg").children().attr('stroke', $(".edit-custom-shape-form .shape_border_color").val());
});

$('body').on('change', '.edit-custom-shape-form .shape-rotation-input', function (e) {
    logger(1, 'DEBUG: action = action-rotate shape');
    var id = $(this).attr('data-path')
        , angle = parseInt(this.value);

    $("#customShape" + id).css("-ms-transform", "rotate(" + angle + "deg)");
    $("#customShape" + id).css("-webkit-transform", "rotate(" + angle + "deg)");
    $("#customShape" + id).css("transform", "rotate(" + angle + "deg)");
});

$('body').on('click', '.edit-custom-shape-form-save', function (e) {
    logger(1, 'DEBUG: action = action-save new shape values');
    var id = $(this).attr('data-path')
        , $selected_shape = $("#customShape" + id)
        , shape_border_width
        , new_data
        , shape_name = $(".shape-name-input").val()
        ;

    $('.edit-custom-shape-form .firstShapeValues-background-color').val($(".edit-custom-shape-form .shape_background_color").val());
    shape_border_width = $("#customShape" + id + " svg").children().attr('stroke-width');
    $selected_shape.resizable("destroy");
    $("#customShape" + id).removeClass('in-editing');
    new_data = document.getElementById("customShape" + id).outerHTML;
    $('#context-menu').remove();
    $selected_shape.resizable({
        autoHide: true,
        resize: function (event, ui) {
            textObjectResize(event, ui, {"shape_border_width": shape_border_width});
        },
        stop: textObjectDragStop
    });

    editTextObject(id, {data: new_data, name: shape_name}).done(function () {
        $("#customShape" + id ).attr('name', shape_name);
        addMessage('SUCCESS', 'Lab has been saved (60023).');
    }).fail(function (message) {
        addModalError(message);
    });
    $('.edit-custom-shape-form').remove();
});

// Print lab textobjects
$(document).on('click', '.action-textobjectsget', function (e) {
    logger(1, 'DEBUG: action = textobjectsget');
    $.when(getTextObjects()).done(function (textobjects) {
        printListTextobjects(textobjects);
    }).fail(function (message) {
        addModalError(message);
    });
});


/*******************************************************************************
 * Free Select
 * ****************************************************************************/
window.freeSelectedNodes = [];
$(document).on("click", ".action-freeselect", function (event) {
    var self = this
        , isFreeSelectMode = $(self).hasClass("active")
        ;

    if (isFreeSelectMode) {
        // TODO: disable Free Select Mode
        $(".node_frame").removeClass("free-selected");
    }
    else {
        // TODO: activate Free Select Mode

    }

    window.freeSelectedNodes = [];
    $(self).toggleClass("active", !isFreeSelectMode);
    $("#lab-viewport").toggleClass("freeSelectMode", !isFreeSelectMode);

    //disable node link
    $('.action-nodelink.active').trigger('click');
});

$(document).on("click", "#lab-viewport.freeSelectMode .node_frame", function (event) {
    event.preventDefault();
    event.stopPropagation();

    var self = this
        , isFreeSelected = $(self).hasClass("free-selected")
        , name = $(self).data("name")
        , path = $(self).data("path")
        ;

    if (isFreeSelected) {   // already present window.freeSelectedNodes = [];
        window.freeSelectedNodes = window.freeSelectedNodes.filter(function (node) {
            return node.name !== name && node.path !== path;
        });
    }
    else {                  // add to window.freeSelectedNodes = [];
        window.freeSelectedNodes.push({
            name: name
            , path: path
        });
    }

    $(self).toggleClass("free-selected", !isFreeSelected);
});

$(document).on("click", ".user-settings", function () {
    var user = $(this).attr("user");
    $.when(getUsers(user)).done(function (user) {
        // Got user
        printFormUser('edit', user);
    }).fail(function (message) {
        // Cannot get user
        addModalError(message);
    });
});


// Load logs page
$(document).on('click', '.action-logs', function(e) {
    logger(1, 'DEBUG: action = logs');
    printLogs('access.txt', 10, "");
    bodyAddClass('logs');
});

/*******************************************************************************
 * Node link
 * ****************************************************************************/

/**
 *
 * @returns {*|jQuery|boolean}
 */
function islinkActive() {

    return $(".action-nodelink").hasClass("active") || false;

}

/**
 * context menu for node link
 * @param node_id
 */

function nodeClicked(title, node_id, e) {
    return $.when(
        getNodeInterfaces(node_id),
        getNetworks(),
        getNodes())
        .done(function (nodeInterfaces, networks, nodes) {

            var interfaces = '';
            var iol_interfc ={};
            var iol_interfc1 = {};


            if (nodeInterfaces['sort'] == 'iol') {
                // IOL nodes need to reorder interfaces
                // i = x/y with x = i % 16 and y = (i - x) / 16

                $.each(nodeInterfaces['ethernet'], function (interfc_id, interfc) {
                    var x = interfc_id % 16;
                    var y = (interfc_id - x) / 16;
                    interfc['id']=interfc_id;
                    iol_interfc[4 * x + y] = interfc;
                });

                 nodeInterfaces['ethernet']=iol_interfc;

                // IOL nodes need to reorder interfaces
                // i = x/y with x = i % 16 and y = (i - x) / 16

                $.each(nodeInterfaces['serial'], function (interfc_id, interfc) {
                    var x = interfc_id % 16;
                    var y = (interfc_id - x) / 16;
                    interfc['id']=interfc_id;
                    iol_interfc1[4 * x + y] = interfc;

                });

                 nodeInterfaces['serial']=iol_interfc1;
            }



            $.each(nodeInterfaces, function (key, value) {

                if ($.inArray(key, ['ethernet', 'serial']) > -1)
                    $.each(value, function (id, object) {

                        var network = '';
                        var remoteIf = '';
                        var networkId = 0;

                        if (nodeInterfaces['sort'] != 'iol') {
                            object.id = id;
                        }

                        if (networks[object['network_id']]) {
                            network = ' <i class="glyphicon glyphicon-transfer" title="Connected"></i> ' +
                                networks[object['network_id']].name;

                            network +=
                                //edit
                                '<a class="action-networkedit" data-path="' + object['network_id'] + '" ' +
                                'data-name="' + object['name'] + '" href="#" title="Edit network">' +
                                '<i class="glyphicon glyphicon-pencil"></i></a>' +
                                //deatach
                                '<a class="action-networkdeatach" data-path="' + object['network_id'] + '" ' +
                                'data-name="' + object['name'] + '" href="#" title="Detach interface"' +
                                'node-id="' + node_id + '"' +
                                'interface-id="' + object.id + '"' +
                                'network-id="' + networkId + '" >' +
                                '<i class="glyphicon glyphicon-export"></i></a>';

                            networkId = object['network_id'];
                        }


                        if (object['remote_if']) {

                            remoteIf =
                                ' <i class="glyphicon glyphicon-transfer" title="Connected"></i> ' +
                                nodes[object['remote_id']].name + ' ' +
                                object['remote_if_name'];
                        }

                        if (key == 'ethernet') {

                            interfaces += '<li class="action-nodelink-li">' +
                                '<a class="context-collapsible interfaces" ' +
                                'href="#" interface-name="' + object['name'] + '" ' +
                                'node-id="' + node_id + '" ' +
                                'interface-id="' + object.id + '" ' +
                                'network-id="' + networkId + '" ' +
                                '>' +
                                '<i class="glyphicon glyphicon-link"></i>' + object['name'] +
                                network +
                                '</a>' +
                                '</li>';
                        }
                        else {

                            interfaces += '<li class="action-nodelink-li">' +
                                '<a class="action-nodeinterfaces context-collapsible menu-edit" ' +
                                'href="#"' +
                                'data-path="' + node_id + '" ' +
                                'data-name="' + object['name'] + '"' +
                                '>' +
                                '<i class="glyphicon glyphicon-link"></i>' + object['name'] +
                                remoteIf +
                                ' </a>' +
                                '</li>';
                        }

                    });
            });

            printContextMenu(title, interfaces, e.pageX, e.pageY);

        }).fail(function (message) {
            // Error on getting node interfaces
            addModalError(message);
        });
}


/**
 *
 * @param title
 * @param node_id
 * @param e
 */
function networkClicked(title, node_id, e) {

    var network = $(e.target).closest('.network_frame');
    var network_id = network.attr('data-path');


    // Network clicked first
    if (!window.startNode) {

        logger(1, 'Link DEBUG: Network clicked first');
        window.startNode = {
            'networkId': network_id,
            'interfaceId': 0,
            'nodeId': 0,
            'created': 0
        };

        selected_active($('#network' + network_id));


    }
    //Network clicked second
    else {

        logger(1, 'Link DEBUG: Network clicked second');

        var start_node = window.startNode.nodeId;
        var interface_id = window.startNode.interfaceId;
        var start_network_id = window.startNode.networkId;

        //different start and end network
        if (start_network_id != network_id) {

            $.when(getNodes(null))
                .then(function (nodes) {
                    //all nodes
                    var arr = [];
                    $.each(nodes, function (id, object) {
                        arr.push(getNodeInterfaces(object.id));
                    });

                    return $.when.apply(this, arr)
                })
                .then(function (res) {

                    // all node interfaces
                    var network = [];
                    var interfaces = arguments;


                    //--------------------------------------------------------------------------
                    $.each(interfaces, function (id, nodeInterface) {
                        $.each(nodeInterface['ethernet'], function (id, object) {

                            if (object.network_id == start_network_id) {
                                network.push(setNodeInterface(nodeInterface.id, network_id, id))
                            }
                        })
                    });


                    return $.when.apply(this, network)
                })
                .then(function () {
                    return $.when(deleteNetwork(start_network_id))
                })
                .done(function (result) {

                    delete window.startNode
                    // var pos = result.data;
                    // return $.when(setNetworkPosition(network_id,pos.left,pos.top));
                   // return $.when(setNodeInterface(start_node, network_id, interface_id))


                    window.location.reload();
                })
                .fail(function (message) {
                    // Error on save
                    addModalError(message);
                });

        }


    }

}

/**
 * context menu
 * @param title
 * @param node_id
 * @param e
 */

function contextMenuInterfaces(title, node_id, e) {

    //test ot start/stop node
    if (!node_id) {
        return true;
    }

    if ($(e.target).closest('.node.node_frame').length) { //node clicked
        nodeClicked(title, node_id, e);
    }
    else {
        //the network was clicked second
        if ($(e.target).closest('.network.network_frame').length) {
            networkClicked(title, node_id, e);
        }
    }
}

/**
 * select/deselect on active link
 * @param element
 */

function selected_active(element) {
    $(element).toggleClass('link_selected');

    jsPlumb.ready(function () {


        var offset = $(element).offset()

        var destination = $("<div/>", {id: "inner"}).draggable().appendTo('#lab-viewport');
        destination.css({"position": "absolute", 'top': offset.top, 'left': offset.left, 'opacity': 1});
        destination.html('<img class="selector" src="/images/link_selector.png">')


        // Create jsPlumb topology
        var lab_topology = jsPlumb.getInstance();

        var source = $(element).attr('id');


        lab_topology.importDefaults({
            Anchor: 'Continuous',
            Connector: ['Straight'],
            Endpoint: 'Blank',
            PaintStyle: {lineWidth: 2, strokeStyle: '#58585a'},
            cssClass: 'link'
        });


        var conn = lab_topology.connect({
            source: source,       // Must attach to the IMG's parent or not printed correctly
            target: $(destination).attr('id'),  // Must attach to the IMG's parent or not printed correctly
            cssClass: source + ' ' + destination + ' frame_ethernet new_network',
            isSource: true
        });

        window.conn = conn;

        $(document).on("mousemove", function (e) {

            lab_topology.animate(
                destination,
                {
                    left: e.pageX - $('.selector').width() / 2 - 25,
                    top: e.pageY - $('.selector').height() / 2
                },
                {duration: 0});
        })

    })
}


$(document).on("click", ".action-nodelink", function (event) {
    var self = this;
    var isNodeSelectMode = $(self).hasClass("active");

    $('.action-freeselect.active').trigger('click');

    if (isNodeSelectMode) {
        $(".node_frame").removeClass("node-selected");
        detachNodeLink();
        localStorage.setItem('action-nodelink',false)
    }
    else {
        localStorage.setItem('action-nodelink',true)
    }


    $(self).toggleClass("active", !isNodeSelectMode);
    $("#lab-viewport").toggleClass("nodeSelectMode", !isNodeSelectMode);
});


//add interfaces dinamicaly (new)
$(document).on('click', 'a.interfaces', function (e) {
    e.preventDefault();


    //deactivate on disabled nodelink
    if (!islinkActive()) return true;

    var network_frame = $('.node_frame, .network_frame');
    var interface_id = $(this).attr('interface-id')
    var interface_name = $(this).attr('interface-name')
    var isStartNode = typeof window.startNode !== 'undefined';
    var isNetworkId = typeof $(this).attr('network-id') !== 'undefined' ? $(this).attr('network-id') : 0;


    //the node is clicked
    if (isStartNode) {
        var end_node = $(this).attr('node-id');
        var network_id = isNetworkId > 0 ? isNetworkId : window.startNode.networkId;

        //step 3
        if (network_id > 0 && end_node > 0) {


            logger(1, 'Link DEBUG: node clicked second ');

            $.when(getNodeInterfaces(end_node))
                .then(function (nodeInterface) {

                    var hasNetwork = 0;

                    $.each(nodeInterface['ethernet'], function (id, object) {
                        if (interface_id == id && object.network_id > 0) {
                            hasNetwork = 1;
                            return;
                        }
                    });

                    //if end note has network attached, and start network is created
                    if (hasNetwork && window.startNode.created) {


                        return setNodeInterface(window.startNode.nodeId, isNetworkId, interface_id)
                    }
                    else {

                        //connect to clicked network
                        return setNodeInterface(end_node, window.startNode.networkId, interface_id)
                    }
                })
                .done(function (response) {

                    delete window.startNode
                    window.location.reload();
                })
                .fail(function (message) {
                    // Error on save
                    addModalError(message);
                });
        }

    }
    else {

        logger(1, 'Link DEBUG: node clicked first ');
        //add new network
        window.startNode = {};
        var start_node = $(this).attr('node-id');
        var node_name = $('.node' + start_node).attr('data-name') + '-' + interface_name
        var offset = $('#node' + start_node).offset()

        $('.node' + start_node).addClass('startNode');

        if (isNetworkId == 0) {


            $.when(setNetwork(node_name, offset.left + 20, offset.top + 40))
            //step 1
                .then(function (response) {
                    var networkId = response.data.id;

                    logger(1, 'Link DEBUG: new network created ' + networkId);

                    window.startNode = {
                        'networkId': networkId,
                        'interfaceId': interface_id,
                        'nodeId': start_node,
                        'created': 1
                    };

                    return setNodeInterface(start_node, networkId, interface_id)
                })
                //step 2
                .then(function (response) {
                    jsPlumb.repaint(network_frame);
                    selected_active($('.startNode'));
                })
                .done()
                .fail(function (message) {
                    // Error on save
                    addModalError(message);
                });
        }
        else {

            logger(1, 'Link DEBUG: only atach');
            window.startNode = {
                'networkId': isNetworkId,
                'interfaceId': interface_id,
                'nodeId': start_node,
                'created': 0
            };

            selected_active($('#node' + start_node));


        }

    }

    $('#context-menu').remove();
})

//disble click on serial
$(document).on('click', 'a.interfaces.serial', function (e) {
    e.preventDefault();
})

//show context menu when node is off
$(document).on('click', '.node.node_frame a', function (e) {

    var node = $(this).parent();
    var node_id = node.attr('data-path');
    var status = parseInt(node.attr('data-status'));
    var $labViewport = $("#lab-viewport")
        , isFreeSelectMode = $labViewport.hasClass("freeSelectMode")

    if (islinkActive() || isFreeSelectMode) return true;

    if (!status) {

        e.preventDefault();

        $.when(getNodes(node_id))
            .then(function (node) {

                var network = '<li><a class="action-nodestart menu-manage" data-path="' + node_id +
                    '" data-name="' + node.name + '" href="#"><i class="glyphicon glyphicon-play"></i> Start</a></li>';
                network += '<li><a style="display: block;" class="action-nodeedit " data-path="' + node_id +
                    '" data-name="' + node.name + '" href="#"><i class="glyphicon glyphicon-edit"></i> Edit</a></li>';

                printContextMenu(node.name, network, e.pageX, e.pageY);
            })
            .fail(function (message) {
                addMessage('danger', message);
            });

        return false;
    }

})

/**
 *
 * @returns {*}
 */
function detachNodeLink() {

            if (window.conn || window.startNode) {
                var source = $('#inner').attr('data-source');
                $('#inner').remove();
                $('.link_selected').removeClass('link_selected');
                $('.startNode').removeClass('startNode');
                jsPlumb.detach(window.conn);
                delete window.startNode;
                delete window.conn;
            }


}
