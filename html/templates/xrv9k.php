<?php 
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler 
 
/** 
 * html/templates/xrv9k.php 
 * 
 * Cisco XRv 9000 template for UNetLab. 
  * You should have received a copy of the GNU General Public License 
  * along with UNetLab. If not, see <http://www.gnu.org/licenses/>. 
  * 
  * @author Andrea Dainese <andrea.dainese@gmail.com>
  * @copyright 2014-2016 Andrea Dainese
  * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
  * @link http://www.unetlab.com/
  * @version 20160719
  */ 
  
 $p['type'] = 'qemu'; 
 $p['name'] = 'xrv9k'; 
 $p['icon'] = 'XR.png'; 
 $p['cpu'] = 4; 
 $p['ram'] = 16384; 
 $p['qemu_nic'] = 'virtio-net-pci'; 
 $p['ethernet'] = 4; 
 $p['console'] = 'telnet'; 
 $p['qemu_arch'] = 'x86_64'; 
 $p['qemu_options'] = '-machine type=pc,accel=kvm,usb=off -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc,driftfix=slew -global kvm-pit.lost_tick_policy=discard -no-hpet -realtime mlock=off -no-shutdown -boot order=c'; 
?> 
