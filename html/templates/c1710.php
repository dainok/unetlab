<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/c1710.php
 *
 * c1710 template for UNetLab.
 * You should have received a copy of the GNU General Public License
 * along with UNetLab.If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

$p['type'] = 'dynamips';
$p['name'] = '1710';
$p['icon'] = 'Router.png';
$p['idlepc'] = '0x80369ac4';
$p['nvram'] = 128;
$p['ram'] = 96; 
$p['dynamips_options'] = '-P 1700 -t 1710 -o 4 -c 0x2102 -X';
?>
