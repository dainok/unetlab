1 <?php 
2 # vim: syntax=php tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler 
3  
4 /** 
5  * html/templates/xrv9k.php 
6  * 
7  * Cisco XRv 9000 template for UNetLab. 
8  * 
9  * LICENSE: 
10  * 
11  * This file is part of UNetLab (Unified Networking Lab). 
12  * 
13  * UNetLab is free software: you can redistribute it and/or modify 
14  * it under the terms of the GNU General Public License as published by 
15  * the Free Software Foundation, either version 3 of the License, or 
16  * (at your option) any later version. 
17  * 
18  * UNetLab is distributed in the hope that it will be useful, 
19  * but WITHOUT ANY WARRANTY; without even the implied warranty of 
20  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
21  * GNU General Public License for more details. 
22  * 
23  * You should have received a copy of the GNU General Public License 
24  * along with UNetLab. If not, see <http://www.gnu.org/licenses/>. 
25  * 
26  * @author Andrea Dainese <andrea.dainese@gmail.com> 
27  * @copyright 2014-2016 Andrea Dainese 
28  * @license http://www.gnu.org/licenses/gpl.html 
29  * @link http://www.unetlab.com/ 
30  * @version 20151116 
31  */ 
32  
33 $p['type'] = 'qemu'; 
34 $p['name'] = 'xrv9k'; 
35 $p['icon'] = 'Router.png'; 
36 $p['cpu'] = 1; 
37 $p['ram'] = 3072; 
38 $p['qemu_nic'] = 'virtio-net-pci'; 
39 $p['ethernet'] = 4; 
40 $p['console'] = 'telnet'; 
41 $p['qemu_arch'] = 'x86_64'; 
42 $p['qemu_options'] = '-machine type=pc,accel=kvm,usb=off -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc,driftfix=slew -global kvm-pit.lost_tick_policy=discard -no-hpet -realtime mlock=off -no-shutdown -boot order=c'; 
43 ?> 
