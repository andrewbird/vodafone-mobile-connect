#!/usr/bin/make -f

PROG=usb_modeswitch
BUILDDIR=debian/tmp

$(PROG): $(PROG).c
	$(CC) -o $@ -lusb $< 

build: $(PROG)
	mkdir -p $(BUILDDIR)/DEBIAN
	$(MAKE) install DESTDIR=$(BUILDDIR)
	dpkg-gencontrol
	dpkg-deb -b $(BUILDDIR) ..

binary: binary-arch binary-indep

binary-arch binary-indep: build

install: $(PROG)
	strip $<
	install -D -s $<	$(DESTDIR)/usr/sbin/$<
	install -D $(PROG).conf $(DESTDIR)/etc/$(PROG).conf

deb:
	dpkg-buildpackage -rfakeroot -B -us -uc
	
clean:
	rm -f $(PROG)
	rm -rf $(BUILDDIR)
	rm -f debian/files

.PHONY: build clean install binary binary-indep binary-arch

