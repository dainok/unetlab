<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/cips.php
 *
 * cips template for UNetLab.
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
 * along with UNetLab.If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20151116
 */

$p['type'] = 'qemu';
$p['name'] = 'IPS'; 
$p['icon'] = 'IPS.png';
$p['cpu'] = 1;
$p['ram'] = 2048; 
$p['ethernet'] = 5; 
$p['console'] = 'telnet'; 
$p['qemu_arch'] = 'i386';
$p['qemu_version'] = '1.3.1';
$p['qemu_options'] = '-machine type=pc-1.0 -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc -no-shutdown -boot order=c -smbios type=1,product=IPS-4240/4255,version=1.0,family=IPS-4240/4255';
?>
