<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/c7200.php
 *
 * c7200 template for UNetLab.
 *
 * LICENSE:
 *
 * This file is part of UNetLab (Unified Networking Lab).
 *
 * UNetLab is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * UNetLab is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with UNetLab.If not, see <http:
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2015 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20150521
 */

$p['type'] = 'dynamips'; 
$p['name'] = '7206VXR';
$p['icon'] = 'Router.png'; 
$p['idlepc'] = '0x60630d5c'; 
$p['nvram'] = 128; 
$p['ram'] = 512; 
$p['slot1'] = '';
$p['slot2'] = '';
$p['slot3'] = '';
$p['slot4'] = '';
$p['slot5'] = '';
$p['slot6'] = '';
$p['modules'] = Array(
	'' => 'Empty', 
'PA-FE-TX' => 'PA-FE-TX',
'PA-4E' => 'PA-4E',
'PA-8E' => 'PA-8E' 
);
$p['dynamips_options'] = '-P 7200 -t npe-400 -o 4 -c 0x2102 -X --disk0 128 --disk1 128';
?>
