// Calculating context menu position
function setMenuPosition(e, m) {
    // Calculating position
    if (e.pageX + m.width() > $(window).width()) {
        // Dropright
        var left = e.pageX - m.width();
    } else {
        // Dropleft
        var left = e.pageX;
    }
    if (e.pageY + m.height() > $(window).height()) {
        // Dropup
        var top = e.pageY - m.height();
    } else {
        // Dropdown
        var top = e.pageY;
    }

    // Setting position via CSS
    m.css({
        display: 'block',
        left: left,
        position: 'absolute',
        top: top,
        zIndex: 5200
    });
}

// Hide context menu on click
$(document).click(function() {
    $('#contextmenu_frame').hide();
});

// Manage links on dynamic context menu
$('body').on('click', '#contextmenu_frame a', function(e) {
    var lab_file = getParameter('filename');
    var action = $(this).attr('data-action');
    var id = $(this).attr('data-id');

    if ($.isFunction(window[action])) {
        // Function exists
        window[action](lab_file, id);
    } else {
        // Should not be here
        raiseMessage('DANGER', 'Invalid action "' + action + '".');
    }
});

// Display folder context menu
$('body').on('contextmenu', '.folder_menu', function(e) {
    var folder_name = $(this).attr('data-name');
    var folder_path = $(this).attr('data-path');

    // Building the menu
    var menu = '<div class="dropdown clearfix">';
    menu += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
    menu += '<li role="presentation" class="dropdown-header">' + folder_name + '</li>';
    menu += '<li><a data-action="deleteFolder" data-id="' + folder_path + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-trash"></i> Delete</a></span></li>';
    menu += '</ul>';
    menu += '</div>';

    var $contextMenu = $('#contextmenu_frame');
    $contextMenu.html(menu);

    // Setting position
    setMenuPosition(e, $contextMenu);

    // Disable the browser context menu
    return false;
});

// Display lab context menu
$('body').on('contextmenu', '.lab_menu', function(e) {
    var lab_file = $(this).attr('data-file');
    var lab_path = $(this).attr('data-path');

    // Building the menu
    var menu = '<div class="dropdown clearfix">';
    menu += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
    menu += '<li role="presentation" class="dropdown-header">' + lab_file + '</li>';
    menu += '<li><a data-action="editLab" data-id="' + lab_path + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-edit"></i> Edit</a></span></li>';
    menu += '<li><a data-action="deleteLab" data-id="' + lab_path + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-trash"></i> Delete</a></span></li>';
    menu += '</ul>';
    menu += '</div>';

    var $contextMenu = $('#contextmenu_frame');
    $contextMenu.html(menu);

    // Setting position
    setMenuPosition(e, $contextMenu);

    // Disable the browser context menu
    return false;
});

// Display node context menu
$('body').on('contextmenu', '.node_menu', function(e) {
    var node_id = $(this).attr('data-id');
    var node_name = $(this).attr('data-name');

    // Building the menu
    if ($(location).attr('pathname') == '/lab_edit.php') {
        // Menu for edit lab
        var menu = '<div class="dropdown clearfix">';
        menu += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
        menu += '<li role="presentation" class="dropdown-header">' + node_name + '</li>';
        menu += '<li><a data-action="displayNodeInterfacesForm" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-transfer"></i> Interfaces</a></span></li>';
        menu += '<li><a data-action="displayNodeForm" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-edit"></i> Edit</a></span></li>';
        menu += '<li><a data-action="deleteLabNode" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-trash"></i> Delete</a></span></li>';
        menu += '</ul>';
        menu += '</div>';
    } else {
        // Menu for open lab
        var menu = '<div class="dropdown clearfix">';
        menu += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
        menu += '<li role="presentation" class="dropdown-header">' + node_name + '</li>';
        menu += '<li><a data-action="startLabNodes" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-play"></i> Start</a></span></li>';
        menu += '<li><a data-action="stopLabNodes" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-stop"></i> Stop</a></span></li>';
        menu += '<li><a data-action="wipeLabNodes" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-trash"></i> Wipe</a></span></li>';
        menu += '<li><a data-action="exportLabNodes" data-id="' + node_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-save"></i> Export CFG</a></span></li>';
        menu += '</ul>';
        menu += '</div>';
    }

    var $contextMenu = $('#contextmenu_frame');
    $contextMenu.html(menu);

    // Setting position
    setMenuPosition(e, $contextMenu);

    // Disable the browser context menu
    return false;
});

// Display network context menu
$('body').on('contextmenu', '.network_menu', function(e) {
    var network_id = $(this).attr('data-id');
    var network_name = $(this).attr('data-name');

    // Building the menu
    if ($(location).attr('pathname') == '/lab_edit.php') {
        // Menu for edit lab
        var menu = '<div class="dropdown clearfix">';
        menu += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
        menu += '<li role="presentation" class="dropdown-header">' + network_name + '</li>';
        menu += '<li><a data-action="displayNetworkForm" data-id="' + network_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-edit"></i> Edit</a></span></li>';
        menu += '<li><a data-action="deleteLabNetwork" data-id="' + network_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-trash"></i> Delete</a></span></li>';
        menu += '</ul>';
        menu += '</div>';
    }

    var $contextMenu = $('#contextmenu_frame');
    $contextMenu.html(menu);

    // Setting position
    setMenuPosition(e, $contextMenu);

    // Disable the browser context menu
    return false;
});

// Display picture context menu
$('body').on('contextmenu', '.picture_menu', function(e) {
    var picture_id = $(this).attr('data-id');
    var picture_name = $(this).attr('data-name');

    // Building the menu
    if ($(location).attr('pathname') == '/lab_edit.php') {
        // Menu for edit lab
        var menu = '<div class="dropdown clearfix">';
        menu += '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
        menu += '<li role="presentation" class="dropdown-header">' + picture_name + '</li>';
        menu += '<li><a data-action="displayPictureForm" data-id="' + picture_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-edit"></i> Edit</a></span></li>';
        menu += '<li><a data-action="deletePicture" data-id="' + picture_id + '" tabindex="-1" href="#"><i class="glyphicon glyphicon-trash"></i> Delete</a></span></li>';
        menu += '</ul>';
        menu += '</div>';
    }

    var $contextMenu = $('#contextmenu_frame');
    $contextMenu.html(menu);

    // Setting position
    setMenuPosition(e, $contextMenu);

    // Disable the browser context menu
    return false;
});
