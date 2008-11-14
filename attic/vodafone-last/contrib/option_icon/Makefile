# In order to be able to compile icon_switch.c you'll need libusb-dev
# (Ubuntu/Debian name)

all: compile install

install:
	cp files/99-option-icon.rules /etc/udev/rules.d/
	cp files/icon_switch /usr/sbin
	udevcontrol reload_rules # not necessary in kernels with inotify (2.6.13+)

compile:
	gcc files/icon_switch.c -lusb -o files/icon_switch

clean:
	rm -f files/icon_switch

