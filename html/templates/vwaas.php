<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/vwaas.php
 *
 * vwaas template for UNetLab.
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
$p['name'] = 'WAAS';
$p['icon'] = 'Cisco WAAS.png';
$p['cpu'] = 1;
$p['ram'] = 2048;
$p['ethernet'] = 2;
$p['console'] = 'vnc';
$p['qemu_arch'] = 'x86_64';
$p['qemu_options'] = '-machine type=pc-1.0,accel=kvm -smbios type=1,manufacturer=\"VMware Inc.\",product=\"VMware Virtual Platform\",serial=\"VMware-12 00 11 22 33 44 55 66-77 88 99 aa bb cc dd ee\"';
?>
