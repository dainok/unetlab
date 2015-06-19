<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/c3725.php
 *
 * c3725 template for UNetLab.
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
$p['name'] = '3725'; 
$p['icon'] = 'Router.png'; 
$p['idlepc'] = '0x60c08728'; 
$p['nvram'] = 128; 
$p['ram'] = 256; 
$p['slot1'] = '';
$p['slot2'] = '';
$p['modules'] = Array(
'' => 'Empty', 
'NM-1FE-TX' => 'NM-1FE-TX',
'NM-16ESW' => 'NM-16ESW' 
);
$p['dynamips_options'] = '-P 3725 -o 4 -c 0x2102 -X --disk0 128 --disk1 128';
?>
