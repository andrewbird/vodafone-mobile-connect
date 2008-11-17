all:
	@echo Please call as \"make pkg TARGET=xxxxx RELEASE=x\"

tree:
	rm -rf tmp
	mkdir tmp
	# TARGET passed through environment
	# RELEASE passed through environment
	python package.py install

pkg: tree
	# RPM based distro
	[ -f tmp/*/vmc.spec ] && (cd tmp && rpmbuild -ta *.tar.bz2) || true
	# DEB based distro
	[ -d tmp/debian ] && (cd tmp && dpkg-buildpackage -rfakeroot -B -us -uc) || true

clean:
	rm -rf tmp build *.egg-info *.deb *.changes
	find . -name \*.pyc -exec rm {} \;
	find . -name \*.pyo -exec rm {} \;
