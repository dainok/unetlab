<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/timos.php
 *
 * timos template for UNetLab.
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
$p['name'] = '7750SR';
$p['icon'] = 'Router.png';
if (function_exists('isVirtual') && isVirtual()) {
	$p['cpu'] = 1;
} else {
	$p['cpu'] = 2;
}
$p['ram'] = 2048; 
$p['ethernet'] = 6; 
$p['console'] = 'telnet'; 
$p['qemu_arch'] = 'x86_64';
if (function_exists('isVirtual') && isVirtual()) {
	$p['qemu_options'] = '-machine type=pc-1.0,accel=tcg';
} else {
	$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm';
}
$p['qemu_options'] .= ' -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc';
?>
