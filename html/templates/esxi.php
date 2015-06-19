<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/esxi.php
 *
 * esxi template for UNetLab.
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

$p['type'] = 'qemu';
$p['name'] = 'esxi';
$p['icon'] = 'Server.png';
$p['cpu'] = 2;
$p['ram'] = 4096; 
$p['ethernet'] = 4; 
$p['console'] = 'vnc';
$p['qemu_arch'] = 'x86_64';
$p['qemu_version'] = '2.1.2-esxi';
$p['qemu_options'] = '-machine pc,accel=kvm -serial none -nographic -nodefconfig -nodefaults -display none -vga std -rtc base=utc -no-shutdown';
?>
