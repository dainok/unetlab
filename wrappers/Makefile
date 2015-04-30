CC=gcc
CFLAGS=-Wall -O2
INC=include/ts.c include/serial2udp.c include/afsocket.c include/tap.c include/cmd.c include/functions.c
DST=/opt/unetlab/wrappers

all:
	mkdir -p $(DST)

	$(CC) $(CFLAGS) -o $(DST)/iol_wrapper $(INC) iol_wrapper.c iol_functions.c
	chmod 755 $(DST)/iol_wrapper
	chown root:root $(DST)/iol_wrapper
	cp -a unl_profile $(DST)/unl_profile

	$(CC) $(CFLAGS) -o $(DST)/qemu_wrapper $(INC) qemu_wrapper.c qemu_functions.c
	chmod 755 $(DST)/qemu_wrapper
	chown root:root $(DST)/qemu_wrapper

	$(CC) $(CFLAGS) -o $(DST)/dynamips_wrapper $(INC) dynamips_wrapper.c dynamips_functions.c
	chmod 755 $(DST)/dynamips_wrapper
	chown root:root $(DST)/dynamips_wrapper

	cp -a unl_wrapper.php $(DST)/unl_wrapper
	chmod 755 $(DST)/unl_wrapper
	chown root:root $(DST)/unl_wrapper

	cp -a vnc_wrapper.sh $(DST)/vnc_wrapper
	chmod 755 $(DST)/vnc_wrapper
	chown root:root $(DST)/vnc_wrapper

uninstall:
	rm -f $(DST)/iol_wrapper
	rm -f $(DST)/vios_wrapper
	rm -f $(DST)/vios_ifup
	rm -f $(DST)/unl_wrapper
