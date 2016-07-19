<?php 
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler 

/** 
 * html/templates/cda.php 
 * 
 * Cisco CDA template for UNetLab. 
 * You should have received a copy of the GNU General Public License 
 * along with UNetLab. If not, see <http: 
 * 
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license https://opensource.org/licenses/BSD-3-Clause
 * @link http://www.unetlab.com/
 * @version 20151019
 */ 
  
$p['type'] = 'qemu'; 
$p['name'] = 'cda'; 
$p['icon'] = 'Server.png'; 
$p['cpu'] = 2; 
$p['ram'] = 2048; 
$p['ethernet'] = 1; 
$p['console'] = 'vnc'; 
$p['qemu_arch'] = 'x86_64'; 
$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm -vga std -boot order=dc'; 
?> 
