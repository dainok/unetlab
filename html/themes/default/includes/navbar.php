        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="container">
                <div class="navbar-brand">Unified Networking Lab</div>
                <ul class="nav navbar-nav">
                    <li<?php if ($section == 'Home') print " class=\"active\""?>><a href="/">Home</a></li>
                    <li<?php if ($section == 'Labs') print " class=\"active\""?>><a href="/lab_list.php?path=/">Labs</a></li>
<?php
if ($section == 'Labs' && $subsection == 'List') {
?>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Actions<span class="caret"></span></a>
                        <ul class="dropdown-menu" role="menu">
                            <li><a class="folder_add" href="#"><i class="glyphicon glyphicon-folder-close"></i> Add a new folder</a></li>
                            <li><a class="lab_add" href="#"><i class="glyphicon glyphicon-file"></i> Add a new lab</a></li>
                        </ul>
                    </li>
<?php
} else if ($section == 'Labs' && $subsection == 'Edit') {
?>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Actions<span class="caret"></span></a>
                        <ul class="dropdown-menu" role="menu">
                        <li><a href="/lab_open.php?filename=<?php print $_GET['filename'] ?>"><i class="glyphicon glyphicon-folder-open"></i> Open this lab</a></li>
                            <li role="presentation" class="divider"></li>
                            <li role="presentation" class="dropdown-header">Add elements</li>
                            <li><a class="network_add" href="#"><i class="glyphicon glyphicon-transfer"></i> Networks</a></li>
                            <li><a class="node_add" href="#"><i class="glyphicon glyphicon-hdd"></i> Nodes</a></li>
                            <li><a class="picture_add" href="#"><i class="glyphicon glyphicon-picture"></i> Pictures</a></li>
                        </ul>
                    </li>
<?php
} else if ($section == 'Labs' && $subsection == 'Open') {
?>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Actions<span class="caret"></span></a>
                        <ul class="dropdown-menu" role="menu">
                            <li><a href="/lab_edit.php?filename=<?php print $_GET['filename'] ?>"><i class="glyphicon glyphicon-edit"></i> Edit this lab</a></li>
                            <li class="divider"></li>
                            <li><a class="node_start_all" href="#"><i class="glyphicon glyphicon-play"></i> Start all nodes</a></li>
                            <li><a class="node_stop_all" href="#"><i class="glyphicon glyphicon-stop"></i> Stop all nodes</a></li>
                            <li><a class="node_wipe_all" href="#"><i class="glyphicon glyphicon-trash"></i> Wipe all nodes</a></li>
                            <li><a class="node_export_all" href="#"><i class="glyphicon glyphicon-save"></i> Export all CFG</a></li>
                        </ul>
                    </li>
<?php
}
?>
                </ul>
                <ul id="auth" class="nav navbar-nav navbar-right">
					<li><a href="#" id="button-logout"><span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
                </ul>
            </div>
        </div>
