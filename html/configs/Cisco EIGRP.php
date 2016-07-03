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
foreach ($node -> getEthernets() as $interface_id => $interface) {
    $network = $interface -> getNetworkId();
    if ($network !== False) {
?>
interface <?php print $interface -> getName()."\n" ?>
 ip address 10.<?php print $tenant ?>.<?php print $network ?>.<?php print $ip ?> 255.255.255.0
 no shutdown
<?php
    }
}
foreach ($node -> getSerials() as $interface_id => $interface) {
    if ($interface -> getRemoteId() !== False) {
        if ($node -> getId() > $interface -> getRemoteId()) {
            $network = $interface -> getRemoteId().$node -> getId();
        } else {
            $network = $node -> getId().$interface -> getRemoteId();
        }
?>
interface <?php print $interface -> getName()."\n" ?>
 ip address 10.<?php print $tenant ?>.<?php print $network ?>.<?php print $ip ?> 255.255.255.0
 no shutdown
<?php
    }
}
?>
router eigrp <?php print 65000 + $tenant."\n" ?>
 network 0.0.0.0
end
