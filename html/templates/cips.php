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

$p['type'] = 'qemu';                  // Must be iol, dynamips or qemu
$p['name'] = 'IPS';                   // Can be empty
$p['icon'] = 'Network Analyzer.png';  // Can be empty, or a icon inside /opt/unetlab/html/images/icons/
$p['cpu'] = 1;                        // Must be integer
$p['ram'] = 2048;                     // Must be integer
$p['ethernet'] = 5;                   // Must be integer
$p['console'] = 'telnet';             // Must be telnet or vnc
$p['qemu_arch'] = 'i386';
$p['qemu_version'] = '1.3.1';
$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm:tcg -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc -no-shutdown -boot order=c -smbios type=1,product=IPS-4240,version=1.0,family=IPS-4240';
?>
