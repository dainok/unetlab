<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/firepower.php
 *
 * firepower template for UNetLab.
 * You should have received a copy of the GNU General Public License
 * along with UNetLab. If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license https://opensource.org/licenses/BSD-3-Clause
 * @link http://www.unetlab.com/
 * @version 20160706
 */

$p['type'] = 'qemu';
$p['name'] = 'FirePower';
$p['icon'] = 'Server.png';
$p['cpu'] = 4;
$p['ram'] = 4096;
$p['ethernet'] = 4;
$p['console'] = 'vnc';
$p['qemu_arch'] = 'x86_64';
$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm -serial none -nographic -nodefconfig -nodefaults -display none -vga std -rtc base=utc';
?>
