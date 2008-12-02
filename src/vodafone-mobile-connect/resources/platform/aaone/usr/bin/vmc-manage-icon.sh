#!/bin/bash

cmd="$1"

if [ -z "$2" ] ; then
	user=${USER}
	root=no
else
	user="$2"
	root=yes
	if [ ! "$(id -u)" = "0" ] ; then
		echo "only root can run this command for other users"	
		exit 1
	fi
fi

# work out home area
hdir="$(getent passwd ${user} | cut -d: -f6)"

# let postinstall succeed too
cd ${hdir}/.config/xfce4/desktop || exit 0

function install() {
# make first backup
	[ -f group-app.vmc ] || cp -p group-app.xml group-app.vmc
# create new
	rm -f group-app.new
	python /usr/libexec/vmc-manage-icon.py
# install
	[ -s group-app.new ] && mv -f group-app.new group-app.xml
	if [ ${root} = "yes" ] ; then
		chown ${user} group-app.???
	fi
}

function remove() {
	[ -s group-app.vmc ] && mv -f group-app.vmc group-app.xml
}

function default() {
	cp /etc/xdg/xfce4/desktop/group-app.xml .
}

function update() {
	pkill -HUP xfdesktop2

	if [ ${root} = "yes" ] ; then
		su - ${user} -c xfdesktop2 </dev/null >/dev/null 2>&1 &
	else
		xfdesktop2 </dev/null >/dev/null 2>&1 &
	fi
}

case ${cmd} in
	install)
		install
		;;
	remove)
		remove
		;;
	default)
		default
		;;
	update)
		update
		;;
	*)
		echo "Usage $0: install|remove|default|update [username]"
		echo "     username: requires root priviledges"
		;;
esac



