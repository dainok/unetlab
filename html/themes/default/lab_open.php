<?php
$section = 'Labs';
$subsection = 'Open';
$title = 'UNetLab - Open Lab';

include('/opt/unetlab/html/themes/default/includes/header.php');
include('/opt/unetlab/html/themes/default/includes/navbar.php');
?>
        <div class="container">
            <div class="starter-template">
                <ul id="mainTab" class="nav nav-tabs" role="tablist">
                    <li><a href="#lab_info" role="tab" data-toggle="tab">Info</a></li>
                    <li class="active"><a href="#lab_topology" role="tab" data-toggle="tab">Topology</a></li>
                    <li><a href="#lab_objects" role="tab" data-toggle="tab">Objects</a></li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Attachments <span class="caret"></span></a>
                        <ul class="dropdown-menu" role="menu">
                            <li><a href="#lab_pictures" tabindex="-1" role="tab" data-toggle="tab">Pictures</a></li>
                            <li><a href="#lab_configs" tabindex="-1" role="tab" data-toggle="tab">Config</a></li>
                        </ul>
                    </li>
                </ul>
                <div class="tab-content">
                    <div id="lab_info" class="tab-pane fade in">
                        <div class="progress">
                            <div class="progress-bar progress-bar-info progress-bar-striped active" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                    <div id="lab_topology" class="tab-pane fade in active">
                        <div class="progress">
                            <div class="progress-bar progress-bar-info progress-bar-striped active" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                    <div id="lab_objects" class="tab-pane fade in">
                        <h2>Networks</h2>
                        <div id="lab_networks" class="tab-pane fade in">
                            <div class="progress">
                                <div class="progress-bar progress-bar-info progress-bar-striped active" style="width: 100%">Loading content...</div>
                            </div>
                        </div>
                        <h2>Nodes</h2>
                        <div id="lab_nodes" class="tab-pane fade in">
                            <div class="progress">
                                <div class="progress-bar progress-bar-info progress-bar-striped active" style="width: 100%">Loading content...</div>
                            </div>
                        </div>
                    </div>
                    <div id="lab_pictures" class="tab-pane fade in">
                        <div class="progress">
                            <div class="progress-bar progress-bar-info progress-bar-striped active" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                    <div id="lab_configs" class="tab-pane fade in">
                        <div class="progress">
                            <div class="progress-bar progress-bar-info progress-bar-striped active" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
<?php
include('/opt/unetlab/html/themes/default/includes/footer.php');
?>
