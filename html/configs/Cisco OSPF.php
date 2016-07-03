<?php
$hostname = $node -> getName();
$ip = $node -> getId() + 1;
?>
hostname <?php print $hostname."\n" ?>
no ip domain lookup
interface loopback 0
 ip address 10.<?php print $tenant ?>.255.<?php print $ip ?> 255.255.255.255
 no shutdown
<?php
if ($node -> getNType() == 'iol') {
    foreach ($node -> getEthernets() as $interface_id => $interface) {
        // i = x/y -> i = x + y * 16
        $x = $interface_id % 16;
        $y = floor($interface_id / 16);
        $network = $interface -> getNetworkId();
        if ($network !== False) {
?>
interface Ethernet<?php print $x ?>/<?php print $y."\n" ?>
 ip address 10.<?php print $tenant ?>.<?php print $network ?>.<?php print $ip ?> 255.255.255.0
 no shutdown
<?php
        }
    }
    foreach ($node -> getSerials() as $interface_id => $interface) {
        // i = x/y -> i = x + y * 16
        $x = $interface_id % 16;
        $y = floor($interface_id / 16);
        if ($interface -> getRemoteId() !== False) {
            if ($node -> getId() > $interface -> getRemoteId()) {
                $network = $interface -> getRemoteId().$node -> getId();
            } else {
                $network = $node -> getId().$interface -> getRemoteId();
            }
?>
interface Serial<?php print $x ?>/<?php print $y."\n" ?>
 ip address 10.<?php print $tenant ?>.<?php print $network ?>.<?php print $ip ?> 255.255.255.0
 no shutdown
<?php
        }
    }
}
?>
router ospf 1
 network 0.0.0.0 0.0.0.0 area 0
end
