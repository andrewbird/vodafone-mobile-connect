all: install

install:
	cp files/99-novatel-ovation.rules /etc/udev/rules.d/
	cp files/ovation.sh /usr/sbin
	udevcontrol reload_rules # not necessary in kernels with inotify (2.6.13+)

clean:
	@echo "noop"

