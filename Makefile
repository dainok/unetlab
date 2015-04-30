prefix = /opt/unetlab

all:
	# Install
	mkdir -p $(prefix) $(prefix)/addons $(prefix)/data/Logs $(prefix)/labs $(prefix)/tmp/
	rsync -a --delete html $(prefix)/
	chown -R root:root $(prefix)
	chown -R www-data:www-data $(prefix)/data $(prefix)/labs
	chown -R root:unl $(prefix)/tmp
	chmod 2775 -R $(prefix)/data $(prefix)/labs $(prefix)/tmp
	cd wrappers; make
