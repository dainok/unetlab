<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/csr1000v.php
 *
 * csr1000v template for UNetLab.
 * You should have received a copy of the GNU General Public License
 * along with UNetLab.If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

$p['type'] = 'qemu';
$p['name'] = 'CSR'; 
$p['icon'] = 'CSRv1000.png';
$p['cpu'] = 1;
$p['ram'] = 3072; 
$p['ethernet'] = 4; 
$p['console'] = 'telnet'; 
$p['qemu_arch'] = 'x86_64';
$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm,usb=off -realtime mlock=off -serial mon:stdio -nographic -nodefconfig -nodefaults -display none -vga std -rtc base=utc,driftfix=slew -global kvm-pit.lost_tick_policy=discard -no-hpet -no-shutdown -boot strict=on -device piix3-usb-uhci,id=usb,bus=pci.0,addr=0x1.0x2';
?>
