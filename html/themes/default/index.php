<?php
$section = 'Home';
$subsection = 'Home';
$title = 'UnetLab - Home';

include('/opt/unetlab/html/themes/default/includes/header.php');
include('/opt/unetlab/html/themes/default/includes/navbar.php');
?>
        <div class="jumbotron">
            <div class="container">
                <h1>Unified Networking Lab</h1>
                <p>Developed by network engineers for network engineers.</p>
                <p><a class="btn btn-primary btn-lg" role="button" href="http://www.unetlab.com/">Learn more &raquo;</a></p>
            </div>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-md-5">
                    <h2 id="status-version">Version (Loading content...)</h2>
                    <p>UNetLab is a new generation software for networking labs. It can be considered the next major version of iou-web, but the software has been rewritten from scratch. The major advantage over GNS3 and iou-web itself is about multi-hypervisor support within a single entity. UNetLab allows to design labs using IOU, Dynamips and QEMU nodes without dealing with multi virtual machines: everything run inside a UNetLab host, and a lab is a single file including all information needed.</p>
                    <p>Currenlty UNetLab is used by some of the top network engineers all around the world.</p>
                    <p><a class="btn btn-default" href="http://www.unetlab.com/tag/release/" role="button">View details &raquo;</a></p>
                </div>
                <div class="col-md-7">
                    <h2>System Status</h2>
                    <div>
                        <h4>CPU usage</h4>
                        <div class="progress">
                            <div id="status-cpu" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                    <div>
                        <h4>Memory usage</h4>
                        <div class="progress">
                            <div id="status-mem" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 100%">Loading content...</div>
                            <div id="status-mem_used" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 0%"></div>
                            <div id="status-mem_cached" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 0%"></div>
                        </div>
                    </div>
                    <div>
                        <h4>Swap usage</h4>
                        <div class="progress">
                            <div id="status-swap" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                    <div>
                        <h4>Disk usage on /</h4>
                        <div class="progress">
                            <div id="status-disk" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 100%">Loading content...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
<?php
include('/opt/unetlab/html/themes/default/includes/footer.php');
?>
