

OBJS = ozerocdoff.o

all: ozerocdoff

ozerocdoff: ozerocdoff.o
	$(CC) -l usb -o $@ ozerocdoff.o

%.o: %.c
	$(CC) -c $*.c -Wall -O

clean:
	rm -f $(OBJS) ozerocdoff

install: ozerocdoff
	install -d $(DESTDIR)/usr/sbin
	install -d $(DESTDIR)/etc/udev/rules.d
	install ozerocdoff $(DESTDIR)/usr/sbin
	cp hso.udev $(DESTDIR)/etc/udev/rules.d/51-hso-udev.rules
	install -d $(DESTDIR)/usr/share/hal/fdi/preprobe/20thirdparty
	cp 10-wwan-hso-preprobe.fdi $(DESTDIR)/usr/share/hal/fdi/preprobe/20thirdparty
	install -d $(DESTDIR)/usr/share/hal/fdi/information/20thirdparty
	cp 10-wwan-quirk.fdi $(DESTDIR)/usr/share/hal/fdi/information/20thirdparty
	install -d $(DESTDIR)/usr/lib/hal/scripts/
	install hal-serial-hsotype $(DESTDIR)/usr/lib/hal/scripts/
	install -d $(DESTDIR)/etc
	install osetsuspend $(DESTDIR)/usr/sbin
	cp hso-suspend.conf $(DESTDIR)/etc
