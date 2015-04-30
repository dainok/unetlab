<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/asa.php
 *
 * asa template for UNetLab.
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
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with UNetLab.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2015 Andrea Dainese
 * @license http://www.gnu.org/licenses/gpl.html
 * @link http://www.unetlab.com/
 * @version 20150428
 */

$p['type'] = 'qemu';          // Must be iol, dynamips or qemu
$p['name'] = 'ASA';           // Can be empty
$p['icon'] = 'Firewall.png';  // Can be empty, or a icon inside /opt/unetlab/html/images/icons/
$p['cpu'] = 1;                // Must be integer
$p['ram'] = 1024;             // Must be integer
$p['ethernet'] = 4;           // Must be integer
$p['console'] = 'telnet';     // Must be telnet or vnc
$p['qemu_arch'] = 'i386';
$p['qemu_nic'] = 'i82559er';
$p['qemu_options'] = '-machine type=pc-1.0,accel=tcg -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc -no-shutdown -boot order=c -hdachs 980,16,32 -smbios type=1,product=asa5520 -icount 1';
?>
