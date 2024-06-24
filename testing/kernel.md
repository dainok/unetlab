# Custom Kernel

Install dependencies and clone kernel patches provided by Proxmox:

```bash
apt-get install -y git build-essential dh-make dh-python sphinx-common asciidoc-base bison dwarves flex libdw-dev libelf-dev libiberty-dev libnuma-dev libslang2-dev libssl-dev lintian lz4 python3-dev xmlto zlib1g-dev
git clone git://git.proxmox.com/git/pve-kernel.git /usr/src/pve-kernel
cd /usr/src/pve-kernel
```

Check the current kernel version:

```bash
# uname -r
6.8.4-2-pve
```

In the [web repository](https://git.proxmox.com/?p=pve-kernel.git;a=summary "Linux Kernel for Proxmox projects"), look for the commit `update ABI file for 6.8.4-2-pve` and get the commit ID (`4cab886f26f9c8638593b8c553996c97ca9acc21`). Switch to the commit:

```bash
git checkout 4cab886f26f9c8638593b8c553996c97ca9acc21
```

Get the patch:

```bash
# cat << EOF > patches/kernel/9999-transparent-bridge.patch
diff --git a/net/bridge/br_input.c b/net/bridge/br_input.c
index 6bb272894..e82112071 100644
--- a/net/bridge/br_input.c
+++ b/net/bridge/br_input.c
@@ -351,7 +351,11 @@ static rx_handler_result_t br_handle_frame(struct sk_buff **pskb)
 			return RX_HANDLER_PASS;

 		case 0x01:	/* IEEE MAC (Pause) */
-			goto drop;
+			fwd_mask |= p->br->group_fwd_mask;
+			if (fwd_mask & (1u << dest[5]))
+				goto forward;
+			else
+				goto drop;

 		case 0x0E:	/* 802.1AB LLDP */
 			fwd_mask |= p->br->group_fwd_mask;
diff --git a/net/bridge/br_sysfs_br.c b/net/bridge/br_sysfs_br.c
index ea7335422..3a61599d9 100644
--- a/net/bridge/br_sysfs_br.c
+++ b/net/bridge/br_sysfs_br.c
@@ -179,9 +179,6 @@ static ssize_t group_fwd_mask_show(struct device *d,
 static int set_group_fwd_mask(struct net_bridge *br, unsigned long val,
 			      struct netlink_ext_ack *extack)
 {
-	if (val & BR_GROUPFWD_RESTRICTED)
-		return -EINVAL;
-
 	br->group_fwd_mask = val;

 	return 0;
EOF
```

Compile the kernel:

```bash
make
```







Add the patch to the patch list:

```bash
echo patches/kernel/9999-transparent-bridge.patch >> submodules/zfsonlinux/debian/patches/series

```



Install the kernel:

```bash
dpkg -i *.deb
```


./submodules/zfsonlinux/debian/patches/series


https://forum.proxmox.com/threads/compile-proxmox-ve-with-patched-intel-iommu-driver-to-remove-rmrr-check.36374/



















