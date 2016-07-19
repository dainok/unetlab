<?php 
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler 
  
/** 
 * html/templates/pfsense.php
 * 
 * Linux template for UNetLab. 
 * You should have received a copy of the GNU General Public License 
 * along with UNetLab. If not, see <http: 
 * 
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */ 

$p['type'] = 'qemu'; 
$p['name'] = 'pfSense'; 
$p['icon'] = 'Firewall.png'; 
$p['cpu'] = 1; 
$p['ram'] = 2048; 
$p['ethernet'] = 2; 
$p['console'] = 'telnet'; 
$p['qemu_arch'] = 'x86_64'; 
$p['qemu_nic'] = 'virtio-net-pci';
$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm -nographic -usbdevice tablet -boot order=dc -serial mon:stdio'; 
?> 
