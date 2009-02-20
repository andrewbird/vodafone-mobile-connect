all:
	@echo Please call as \"make pkg TARGET=xxxxx RELEASE=x\"

tree:
	rm -rf tmp
	mkdir tmp
	# TARGET passed through environment
	# RELEASE passed through environment
	python package.py install
	-if [ -x tmp/*/postscript ] ; then \
		ROOT=`dirname tmp/*/postscript` ; \
		( cd $$ROOT && ./postscript ) ; \
	fi
	rm -f tmp/*/postscript

pkg: tree
	# RPM based distro
	[ -f tmp/*/vmc.spec ] && (cd tmp && rpmbuild -ta *.tar.bz2) || true
	# DEB based distro
	[ -d tmp/debian ] && (cd tmp && dpkg-buildpackage -rfakeroot -B -us -uc) || true

clean:
	rm -rf tmp build *.egg-info *.deb *.changes
	find . -name \*.pyc -exec rm {} \;
	find . -name \*.pyo -exec rm {} \;

distclean: clean
	rm -rf apidocs

apidocs:
	rm -rf apidocs
	pydoctor --add-package=$(shell pwd)/vmc \
		 --project-name="vodafone-mobile-connect" \
		 --make-html \
		 --html-output=apidocs

apiview:
	firefox file://$(shell pwd)/apidocs/index.html

.PHONY: apidocs apiview
