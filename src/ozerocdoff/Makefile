#!/usr/bin/make -f

PROG=ozerocdoff
VER=0.4
RELEASE=2

BUILDDIR=debian/tmp

ifeq ($(ARCH),"")
   TARGET_ARCH+=""
else
   TARGET_ARCH+="-a$(ARCH)"
endif



$(PROG): $(PROG).c
	$(CC) -o $@ -lusb $< 

build: $(PROG)
	mkdir -p $(BUILDDIR)/DEBIAN
	$(MAKE) install DESTDIR=$(BUILDDIR)
	dpkg-gencontrol -v$(VER)-$(RELEASE)
	dpkg-deb -b $(BUILDDIR) ..

binary: binary-arch binary-indep

binary-arch binary-indep: build

install: $(PROG)
	strip $<
	install -D -s $<	$(DESTDIR)/usr/sbin/$<
	install -d $(DESTDIR)/etc/udev/rules.d
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

deb:
	dpkg-buildpackage $(TARGET_ARCH) -rfakeroot -B -us -uc

rpm:
	# you might want to setup your ~/.rpmmacros file to allow building by non root
	# create it and add the following
	# %_topdir    /home/username/rpm
	# then you should create the usual rpm directory structure underneath
	# so mkdir ~/rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	rm -rf rpm
	mkdir -p rpm/tmp/$(PROG)-$(VER)
	cp $(PROG).* osetsuspend hso-suspend.conf hso.udev *.fdi hal-serial-hsotype Makefile rpm/tmp/$(PROG)-$(VER)
	(cd rpm/tmp && tar -jcvf $(PROG)-$(VER).tar.bz2 $(PROG)-$(VER))
	rpmbuild -ta rpm/tmp/$(PROG)-$(VER).tar.bz2
	
clean:
	rm -f $(PROG)
	rm -rf $(BUILDDIR)
	rm -f debian/files
	rm -rf rpm

.PHONY: build clean install binary binary-indep binary-arch rpm

