<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/includes/messages_en.php
 *
 * English messages for UNetLab.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

/***************************************************************************
 * Return Codes (0-127)
 ***************************************************************************/
$messages[1] = 'Must be executed from CLI (1).';
$messages[2] = 'Must be executed by root (2).';
$messages[3] = 'Flag -a is missing (3).';
$messages[4] = 'Flag -T is missing (4).';
$messages[5] = 'Flag -T is not valid (5).';
$messages[6] = 'File not found (6).';
$messages[7] = 'Lab file is not valid (7).';
$messages[8] = 'Flag -D is not valid (8).';
$messages[9] = 'Flag -a is not valid (9).';
$messages[10] = 'Interface is set but network does not exist (10).';
$messages[11] = 'Failed to create network (11).';
$messages[12] = 'Failed to start node (12).';
$messages[13] = 'Unable to wipe node(s) (13).';
$messages[14] = 'Cannot create username (14).';
$messages[15] = 'Cannot remove UUID from exported labs (15).';
$messages[16] = 'Failed to export config (16).';
$messages[17] = 'Failed to upgrade UNetLab (17).';
$messages[18] = 'Unable to connect to Internet (18).';
$messages[19] = 'Export not supported (19).';

/***************************************************************************
 * Classes
 ***************************************************************************/
// __interfc.php (10000-19999)
$messages[10000] = 'Cannot create interface, invalid or missing mandatory parameters (10000).';
$messages[10001] = 'Cannot create interface, invalid interface_type (10001).';
$messages[10002] = 'Attribute ignored, invalid interface_name (10002).';
$messages[10003] = 'Attribute ignored, invalid interface_network_id (10003).';
$messages[10004] = 'Attribute ignored, unneeded remote_id/remote_if (10004).';
$messages[10005] = 'Attribute ignored, unneeded network_id (10005).';
$messages[10006] = 'Attribute ignored, invalid interface_remote_id (10006).';
$messages[10007] = 'Attribute ignored, invalid interface_remote_id (10007).';
$messages[10008] = 'Interface has not been modified (10008).';

// __lab.php (20000-29999)
$messages[20000] = 'Create a new lab, file does not exists (20000).';
$messages[20001] = 'Cannot load lab, invalid filename (20001).';
$messages[20002] = 'Cannot load lab, invalid folder (20002).';
$messages[20003] = 'Cannot load lab, invalid XML document (20003).';
$messages[20004] = 'Cannot load lab, Invalid UNetLab file, attribute is missing (20004).';
$messages[20005] = 'Cannot load lab, invalid lab_name attribute (20005).';
$messages[20006] = 'Attribute ignored, invalid lab_description (20006).';
$messages[20007] = 'Attribute ignored, invalid lab_author (20007).';
$messages[20008] = 'Attribute ignored, invalid lab_version (20008).';
$messages[20009] = 'Network ignored, invalid network (20009).';
$messages[20010] = 'Node ignored, invalid node (20010).';
$messages[20011] = 'Attribute lab_id does not exist, a new one has been generated (20011).';
$messages[20012] = 'Attribute lab_id is not valid, a new one has been generated (20012).';
$messages[20013] = 'Node slot ignored, invalid slot (20013).';
$messages[20014] = 'Node interface ignored, invalid ethernet interface (20014).';
$messages[20015] = 'Node interface ignored, invalid serial interface (20015).';
$messages[20016] = 'Interface ignored, invalid type (20016).';
$messages[20017] = 'Cannot add picture to the lab (20017).';
$messages[20018] = 'Cannot find picture in the selected lab (20018).';
$messages[20019] = 'Cannot edit picture in the selected lab (20019).';
$messages[20020] = 'Picture ignored, invalid picture (20020).';
$messages[20021] = 'Cannot add network to the lab (20021).';
$messages[20022] = 'Cannot add node to the lab (20022).';
$messages[20023] = 'Cannot find network in the selected lab (20023).';
$messages[20024] = 'Cannot find node in the selected lab (20024).';
$messages[20025] = 'Cannot edit network in the selected lab (20025).';
$messages[20026] = 'Cannot edit node in the selected lab (20026).';
$messages[20027] = 'Cannot write file to disk (20027).';
$messages[20028] = 'Cannot delete original lab (20028).';
$messages[20029] = 'Cannot move swap lab file (20029).';
$messages[20030] = 'Lab has not been modified (20030).';
$messages[20031] = 'Lab has been saved (20031).';
$messages[20032] = 'Cannot link node, invalid node_id (20032).';
$messages[20033] = 'Cannot link node, invalid network_id (20033).';
$messages[20034] = 'Cannot link node (20034).';
$messages[20035] = 'Cannot unlink node (20035).';
$messages[20036] = 'Cannot save startup-config in the selected lab (20036).';
$messages[20037] = 'Config ignored, cannot load it (20037).';
$messages[20038] = 'Attribute ignored, invalid lab_name (20038).';
$messages[20039] = 'Lab already exists (20039).';
$messages[20040] = 'Attribute ignored, invalid lab_body (20040).';
$messages[20041] = 'cwObjectPicture ignored, invalid object (20041).';
$messages[20042] = 'Cannot add object to the lab (20042).';
$messages[20043] = 'Cannot find object in the selected lab (20043).';
$messages[20044] = 'Cannot edit object in the selected lab (20044).';
$messages[20045] = 'Attribute ignored, invalid script timeout - set to default value 300 (20045).';

// __network.php (30000-39999)
$messages[30000] = 'Cannot create network, invalid or missing mandatory parameters (30000).';
$messages[30001] = 'Cannot create network, invalid network_type (30001).';
$messages[30002] = 'Attribute ignored, invalid network_name (30002).';
$messages[30003] = 'Attribute ignored, invalid network_left (30003).';
$messages[30004] = 'Attribute ignored, invalid network_top (30004).';
$messages[30005] = 'Attribute ignored, invalid network_type (30005).';
$messages[30006] = 'Network has not been modified (30006).';
$messages[30007] = 'Attribute ignored, invalid network_count (30007).';
$messages[30008] = 'Cannot edit network, invalid network_count (30008).';

// __node.php (40000-49999)
$messages[40000] = 'Cannot create node, invalid or missing mandatory parameters (40000).';
$messages[40001] = 'Cannot create node, invalid node_type (40001).';
$messages[40002] = 'Cannot create node, invalid node_template (40002).';
$messages[40003] = 'Attribute ignored, invalid node_config (40003).';
$messages[40004] = 'Attribute ignored, invalid node_delay (40004).';
$messages[40005] = 'Attribute ignored, invalid node_icon (40005).';
$messages[40006] = 'Attribute ignored, invalid node_image (40006).';
$messages[40007] = 'Attribute ignored, invalid node_left (40007).';
$messages[40008] = 'Attribute ignored, invalid node_name (40008).';
$messages[40009] = 'Attribute ignored, invalid node_ram (40009).';
$messages[40010] = 'Attribute ignored, invalid node_top (40010).';
$messages[40011] = 'Attribute ignored, invalid node_nvram (40011).';
$messages[40012] = 'Attribute ignored, invalid node_ethernet (40012).';
$messages[40013] = 'Attribute ignored, invalid node_serial (40013).';
$messages[40014] = 'Attribute ignored, invalid node_idlepc (40014).';
$messages[40015] = 'Attribute ignored, invalid node_cpu (40015).';
$messages[40016] = 'Node has not been modified (40016).';
$messages[40017] = 'Cannot connect interface, invalid interface_id (40017).';
$messages[40018] = 'Cannot connect interface, interface_id does not exist (40018).';
$messages[40019] = 'Cannot create interface, invalid node_type (40019).';
$messages[40020] = 'Cannot create Ethernet interface (40020).';
$messages[40021] = 'Cannot create interface, invalid node_template (40021).';
$messages[40022] = 'Cannot create Serial interface (40022).';
$messages[40023] = 'Cannot configure slot on non Dynamips node (40023).';
$messages[40024] = 'Cannot configure slot, invalid slot type (40024).';
$messages[40025] = 'Node has no valid image (40025).';
$messages[40026] = 'Attribute ignored, invalid node_uuid (40026).';
$messages[40027] = 'Attribute ignored, invalid node_console (40027).';

// __picture.php (50000-50999)
$messages[50000] = 'Cannot create picture, invalid or missing mandatory parameters (50000).';
$messages[50002] = 'Cannot create picture, invalid picture_data (50002).';
$messages[50003] = 'Attribute ignored, invalid picture_name (50003).';
$messages[50004] = 'Cannot create picture, invalid picture_type (50004).';
$messages[50005] = 'Attribute ignored, invalid picture_map (50005).';
$messages[50006] = 'Picture has not been modified (50006).';

// __object.php (51000-51999)
$messages[51000] = 'Cannot create object, invalid or missing mandatory parameters (51000).';
$messages[51001] = 'Cannot create object, invalid object_type (51001).';
$messages[51002] = 'Attribute ignored, invalid object_name (51002).';
$messages[51003] = 'Attribute ignored, invalid object_data (51003).';

/***************************************************************************
 * Functions and others
 ***************************************************************************/
// api.php (60000-69999)
$messages[60000] = 'Lab does not exist (60000).';
$messages[60001] = 'Fetched system status (60001).';
$messages[60002] = 'Successfully listed network types (60002).';
$messages[60003] = 'Successfully listed node templates (60003).';
$messages[60003] = 'Successfully listed node templates (60003).';
$messages[60004] = 'Successfully listed networks (60004).';
$messages[60005] = 'Successfully listed network (60005).';
$messages[60006] = 'Network has been added to the lab (60006).';
$messages[60007] = 'Successfully listed path (60007).';
$messages[60008] = 'Requested folder does not exist (60008).';
$messages[60009] = 'Requested folder is not valid (60009).';
$messages[60010] = 'Cannot delete root folder (60010).';
$messages[60011] = 'Failed to delete folder (60011).';
$messages[60012] = 'Folder has been deleted (60012).';
$messages[60013] = 'Folder already exists (60013).';
$messages[60014] = 'Folder has been created (60014).';
$messages[60015] = 'Failed to create folder (60015).';
$messages[60016] = 'Lab already exists (60016).';
$messages[60017] = 'Cannot create lab, invalid or missing mandatory parameters (60017).';
$messages[60018] = 'Cannot create lab, parent folder does not exist (60018).';
$messages[60019] = 'Lab has been created (60019).';
$messages[60020] = 'Lab has been loaded (60020).';
$messages[60021] = 'Failed to delete lab (60021).';
$messages[60022] = 'Lab has been deleted (60022).';
$messages[60023] = 'Lab has been saved (60023).';
$messages[60024] = 'Fetced all lab networks and serial endpoints (60024).';
$messages[60025] = 'Successfully listed node (60025).';
$messages[60026] = 'Successfully listed nodes (60026).';
$messages[60027] = 'Request not valid (60027).';
$messages[60028] = 'Successfully listed pictures (60028).';
$messages[60029] = 'Picture not found (60029).';
$messages[60030] = 'Successfully listed node interfaces (60030).';
$messages[60031] = 'Template does not exists or is not available (60031).';
$messages[60032] = 'Successfully listed node template (60032).';
$messages[60033] = 'Requested template is not valid (60033).';
$messages[60034] = 'Failed to move the lab (60034).';
$messages[60035] = 'Lab moved (60035).';
$messages[60036] = 'Lab cloned (60036).';
$messages[60037] = 'Failed to clone the lab (60037).';
$messages[60038] = 'Resource not found (60038).';
$messages[60039] = 'User not found (60039).';
$messages[60040] = 'Successfully listed users (60040).';
$messages[60041] = 'Successfully listed user roles (60041).';
$messages[60042] = 'User saved (60042).';
$messages[60043] = 'Cannot create user, missing mandatory parameters (60043).';
$messages[60044] = 'Cannot get QEMU version (60044).';
$messages[60045] = 'Cannot create user, check if already exists (60045).';
$messages[60046] = 'Destination folder already exists (60046).';
$messages[60047] = 'Destination folder is not valid (60047).';
$messages[60048] = 'Cannot move folder (60048).';
$messages[60049] = 'Folder moved (60049).';
$messages[60050] = 'Failed to stop all nodes (60050).';
$messages[60051] = 'All nodes has been stopped (60051).';
$messages[60052] = 'User does not have an assigned pod (60052).';
$messages[60053] = 'Lab has been closed (60053).';
$messages[60054] = 'Got lab body (60054).';
$messages[60055] = 'Successfully listed startup-configs (60055).';
$messages[60056] = 'Cannot load lab (60056).';
$messages[60057] = 'Got startup-config (60057).';
$messages[60058] = 'Startup config not available (60058).';
$messages[60059] = 'Failed to update UNetLab (60059).';
$messages[60060] = 'UNetLab is updated (60060).';
$messages[60061] = 'Failed to lock the lab (60061).';
$messages[60062] = 'Successfully listed textobjects (60062).';

// Text (70000-79999)
$messages[70000] = 'Name/prefix';
$messages[70001] = 'Icon';
$messages[70002] = 'Image';
$messages[70003] = 'CPU';
$messages[70004] = 'RAM (MB)';
$messages[70005] = 'Ethernets';
$messages[70006] = 'Delay (s)';
$messages[70007] = 'Console';
$messages[70008] = 'UUID';
$messages[70009] = 'Idle PC';
$messages[70010] = 'NVRAM';
$messages[70011] = 'RAM';
$messages[70012] = 'Ethernets';
$messages[70013] = 'Startup configuration';
$messages[70014] = 'Delay (s)';
$messages[70015] = 'Console';
$messages[70016] = 'Slot';
$messages[70017] = 'Serial portgroups (4 int each)';
$messages[70018] = 'Ethernet portgroups (4 int each)';
$messages[70019] = 'Exported';
$messages[70020] = 'None';
$messages[70021] = 'First Eth MAC Address';

// CLI (80000-89999)
$messages[80009] = 'Failed to add the username (80009).';
$messages[80010] = 'Failed to create the home directory (80010).';
$messages[80011] = 'Failed to set the SETGID (80011).';
$messages[80012] = 'Failed to set owner/group (80012).';
$messages[80013] = 'Failed to link the profile (80013).';
$messages[80014] = 'Image not found (80014).';
$messages[80015] = 'QEMU Arch is not set (80015).';
$messages[80016] = 'QEMU not found (80016).';
$messages[80017] = 'Invalid QEMU NIC driver (80017).';
$messages[80018] = 'Invalid QEMU custom options (80018).';
$messages[80020] = 'Cannot create network, invalid network_type (80020).';
$messages[80021] = 'Cannot create network, missing mandatory parameters (80021).';
$messages[80022] = 'Cannot create network, network_name already in use (80022).';
$messages[80023] = 'Failed to add the OVS (80023).';
$messages[80024] = 'Failed to delete the OVS (80024).';
$messages[80025] = 'Failed to delete the Bridge (80025).';
$messages[80026] = 'Failed to add the Bridge (80026).';
$messages[80027] = 'Failed to activate the Bridge (80027).';
$messages[80028] = 'Failed to set group_fwd_mask on bridge (80028).';
$messages[80029] = 'Network not found (80029).';
$messages[80030] = 'Cannot add interface to bridge (80030).';
$messages[80031] = 'Cannot add interface to OVS (80031).';
$messages[80032] = 'Failed to add the TAP interface (80032).';
$messages[80033] = 'Failed to activate the TAP interface (80033).';
$messages[80034] = 'Failed to delete the TAP interface (80034).';
$messages[80035] = 'Failed to stop the node (80035).';
$messages[80036] = 'Failed to drop privileges (80036).';
$messages[80037] = 'Failed to create running directory (80037).';
$messages[80038] = 'Unsupported node_type (80038).';
$messages[80039] = 'Cannot find IOL license (80039).';
$messages[80040] = 'Cannot link IOL license (80040).';
$messages[80041] = 'Cannot lock running path (80041).';
$messages[80042] = 'Cannot unlock running path (80042).';
$messages[80043] = 'Cannot link CDROM (80043).';
$messages[80044] = 'Cannot write on running path (80044).';
$messages[80045] = 'Cannot create linked clone (80045).';
$messages[80046] = 'Failed to build CMD line (80046).';
$messages[80047] = 'Failed to change directory (80047).';
$messages[80048] = 'Nodes started (80048).';
$messages[80049] = 'Node started (80049).';
$messages[80050] = 'Nodes stopped (80050).';
$messages[80051] = 'Node stopped (80051).';
$messages[80052] = 'Nodes cleared (80052).';
$messages[80053] = 'Node cleared (80053).';
$messages[80054] = 'Dynamips not found (80054).';
$messages[80055] = 'Failed to set ageing on bridge (80055).';
$messages[80056] = 'Cloud interface does not exist (80056).';
$messages[80057] = 'Nodes exported (80057).';
$messages[80058] = 'Node exported (80058).';
$messages[80059] = 'Cannot delete tmp file (80059).';
$messages[80060] = 'Failed to export (80060).';
$messages[80061] = 'Node not supported for config export (80061).';
$messages[80062] = 'Config file not found (80062).';
$messages[80063] = 'Failed to save startup-config (80063).';
$messages[80064] = 'Cannot open tmp file (80064).';
$messages[80065] = 'Cannot read tmp file (80065).';
$messages[80066] = 'NVRAM file not found (80066).';
$messages[80067] = 'Failed to dump startup-config (80067).';
$messages[80068] = 'Cannot open startup-config file (80068).';
$messages[80069] = 'Cannot write startup-config file (80069).';
$messages[80070] = 'Failed to remove tmp file (80070).';
$messages[80071] = 'Failed to disable multicast_snooping on bridge (80071).';
$messages[80072] = 'Cannot change path (80072).';
$messages[80073] = 'Cannot ZIP file (80073).';
$messages[80074] = 'Cannot ZIP folder (80074).';
$messages[80075] = 'Export is ready (80075).';
$messages[80076] = 'Import path is not set (80076).';
$messages[80077] = 'Import path is not valid (80077).';
$messages[80078] = 'Import file must be a Zip file (80078).';
$messages[80079] = 'Cannot import UNeTLab file (80079).';
$messages[80080] = 'UNetLab file imported (80080).';
$messages[80081] = 'Failed to upload file, check file size (80081).';
$messages[80082] = 'Cannot find docker.io installation (80082).';
$messages[80083] = 'Cannot create docket container (80083).';
$messages[80084] = 'Skipping powered off and unsupported nodes (80084).';
$messages[80085] = 'Failed to set MTU 9000 on interface (80085).';
$messages[80086] = 'Cannot import iou-web file (80086).';
$messages[80087] = 'iou-web file imported (80087).';
$messages[80088] = 'Cannot find vpcs installation (80088).';

// Authentication (90000-99999)
$messages[90001] = 'User is not authenticated or session timed out (90001).';
$messages[90002] = 'User has been loaded (90002).';
$messages[90003] = 'Database error (90003).';
$messages[90004] = 'Created "users" table (90004).';
$messages[90005] = 'Failed to create "users" table, check also disk space (90005).';
$messages[90006] = 'Failed to update database, check also disk space (90006).';
$messages[90007] = 'Created "permissions" table (90007).';
$messages[90008] = 'Failed to create "permissions" table, check also disk space (90008).';
$messages[90009] = 'Created "pods" table (90009).';
$messages[90010] = 'Failed to create "pods" table, check also disk space (90010).';
$messages[90011] = 'Username not set (90011).';
$messages[90012] = 'Password not set (90012).';
$messages[90013] = 'User logged in (90013).';
$messages[90014] = 'Authentication failed: invalid username/password. Default username is "admin" with password "unl" (90014).';
$messages[90015] = 'Database corrupted (90015).';
$messages[90016] = 'Cannot set user expiration on database, check also disk space (90016).';
$messages[90017] = 'Cannot set user cookie on database, check also disk space (90017).';
$messages[90018] = 'Authentication failed: user has been expired (90018).';
$messages[90019] = 'User logged out (90019).';
$messages[90020] = 'Cannot query for expired PODS (90020).';
$messages[90021] = 'Cannot remove expired PODS from database (90021).';
$messages[90022] = 'No POD available (90022).';
$messages[90023] = 'Cannot assign POD to user (90023).';
$messages[90024] = 'Cannot check expiration on database (90024).';
$messages[90025] = 'Cannot list expired PODS (90025).';
$messages[90026] = 'Cannot query for users on (90026).';
$messages[90027] = 'Cannot query for pods on (90027).';
$messages[90028] = 'Created "sessions" table (90028).';
$messages[90029] = 'Failed to create "sessions" table (90029).';
$messages[90030] = 'Failed to update database to latest version (90030).';
$messages[90031] = 'Database updated (90031).';
$messages[90032] = 'Not enough access privileges for this operation (90032).';
$messages[90033] = 'Cannot set last seen folder on database, check also disk space (90033).';
$messages[90034] = 'Cannot set running lab on database, check also disk space (90034).';
?>
