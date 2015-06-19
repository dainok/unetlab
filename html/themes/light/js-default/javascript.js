$(document).ready(function() {
    if ($(location).attr('pathname') == '/lab_list.php') {
        // Page: lab_list
        path = getParameter('path');

        // Display folder content
        displayFolder(path);
    } else if ($(location).attr('pathname') == '/lab_open.php') {
        // Page: lab_open
        lab_file = getParameter('filename');

        // Display lab info
        displayLabInfo(lab_file);

        // Display topology (after nodes and networks)
        $.when(displayLabNodes(lab_file), displayLabNetworks(lab_file)).done(function() {
            displayLabTopology(lab_file);
        });

        // Display pictures
        displayLabPictures(lab_file);

        // Update node status
        setInterval('displayLabStatus()', 5000);
    } else if ($(location).attr('pathname') == '/lab_edit.php') {
        // Page: lab_edit
        lab_file = getParameter('filename');

        // Pop up a warning message
        raisePermanentMessage('WARNING', 'You are using the edit mode.');

        // Display info edit form
        displayLabInfo(lab_file);

        // Display topology (after nodes and networks)
        $.when(displayLabNodes(lab_file), displayLabNetworks(lab_file)).done(function() {
            displayLabTopology(lab_file);
        });

        // Display pictures
        displayLabPictures(lab_file);
    } else {
        // Should be in the home page
        displaySystemStatus();
    }
});

$(window).resize(function(){
    if ($(location).attr('pathname') == '/lab_edit.php' || $(location).attr('pathname') == '/lab_open.php') {
        // Update topology on window resize
        jsPlumb.repaintEverything();
    }
});
