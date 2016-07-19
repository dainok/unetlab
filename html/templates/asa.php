<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/asa.php
 *
 * asa template for UNetLab.
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
$p['name'] = 'ASA';
$p['icon'] = 'ASA.png';
$p['cpu'] = 1;
$p['ram'] = 512;
$p['ethernet'] = 4;
$p['console'] = 'telnet';
$p['qemu_arch'] = 'i386';
$p['qemu_nic'] = 'i82559er';
$p['qemu_options'] = '-machine type=pc-1.0,accel=tcg -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc -smbios type=1,product=asa5520 -icount 1';
?>
