<?php

// Include custom configuration
if (file_exists('/opt/unetlab/html/themes/default/includes/config.php')) {
    require_once('/opt/unetlab/html/themes/default/includes/config.php');
}

if (!defined('TIMEZONE')) define('TIMEZONE', 'Europe/Rome');

define('VERSION', '(development)');
define('BASE_THEME', '/themes/default');
?>
