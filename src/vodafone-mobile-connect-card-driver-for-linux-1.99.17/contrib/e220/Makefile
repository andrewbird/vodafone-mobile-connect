# In order to be able to compile huaweiAktBbo.c you'll need libusb-dev
# (Ubuntu/Debian name)

all: compile install

install:
	cp files/99-huawei-e220.rules /etc/udev/rules.d/
	cp files/huaweiAktBbo /usr/sbin
	udevcontrol reload_rules # not necessary in kernels with inotify (2.6.13+)

compile:
	gcc files/huaweiAktBbo.c -lusb -o files/huaweiAktBbo

clean:
	rm -f files/huaweiAktBbo

