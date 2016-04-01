CC=gcc
CXX=g++
CFLAGS=-Wall -O2
CXXFLAGS=$(CFLAGS) -Wno-write-strings
INC=include/ts.c include/serial2udp.c include/afsocket.c include/tap.c include/cmd.c include/functions.c include/log.c
DST=/opt/unetlab/wrappers

all:
	mkdir -p $(DST)

	$(CXX) $(CXXFLAGS) -o $(DST)/simple_forwarder $(INC) simple_forwarder.cpp iol_functions.c
	chmod 755 $(DST)/simple_forwarder
	chown root:root $(DST)/simple_forwarder

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

	$(CC) $(CFLAGS) -o $(DST)/docker_wrapper $(INC) docker_wrapper.c docker_functions.c
	chmod 755 $(DST)/docker_wrapper
	chown root:root $(DST)/docker_wrapper

	cp -a nsenter $(DST)/nsenter
	chmod 755 $(DST)/nsenter
	chown root:root $(DST)/nsenter

	cp -a unl_wrapper.php $(DST)/unl_wrapper
	chmod 755 $(DST)/unl_wrapper
	chown root:root $(DST)/unl_wrapper

uninstall:
	rm -f $(DST)/simple_forwarder
	rm -f $(DST)/iol_wrapper
	rm -f $(DST)/qemu_wrapper
	rm -f $(DST)/dynamips_wrapper
	rm -f $(DST)/docker_wrapper
	rm -f $(DST)/unl_wrapper
	rm -f $(DST)/nsenter
