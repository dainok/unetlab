<?php
# vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

/**
 * html/templates/c3725.php
 *
 * c3725 template for UNetLab.
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
$p['name'] = '3725'; 
$p['icon'] = 'Router.png'; 
$p['idlepc'] = '0x60c08728'; 
$p['nvram'] = 128; 
$p['ram'] = 256; 
$p['slot1'] = '';
$p['slot2'] = '';
$p['modules'] = Array(
'' => 'Empty', 
'NM-1FE-TX' => 'NM-1FE-TX',
'NM-16ESW' => 'NM-16ESW' 
);
$p['dynamips_options'] = '-P 3725 -o 4 -c 0x2102 -X --disk0 128 --disk1 128';
?>
