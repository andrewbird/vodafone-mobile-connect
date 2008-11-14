#!/bin/sh
INSTALL_PREFIX=/opt/vmc
if [ `id -u` -ne 0 ]
then
	echo "You must be root!"
	exit
fi

#destroy me please :D
rm -f $0

echo "Copying files to $INSTALL_PREFIX..."
cp -fr . / 
rm -fr $INSTALL_PREFIX/lib/python
mv $INSTALL_PREFIX/lib/python2.* $INSTALL_PREFIX/lib/python

#wvdial fix (it doesn't see libxplc in the opt lib directory)
libxplc=`basename $INSTALL_PREFIX/lib/libxplc*`
if [ ! -e /usr/lib/$libxplc ]
then
	cp -l $INSTALL_PREFIX/lib/$libxplc /usr/lib
fi

echo "Configuring the system..."

#Adding group vmc
if [ -x /usr/sbin/addgroup ]
then
	/usr/sbin/addgroup vmc
elif [ -x /usr/sbin/groupadd ]
then
	/usr/sbin/groupadd vmc
fi

#Permissions for ppp files
chown :vmc -R $INSTALL_PREFIX/etc/ppp
chmod 0660 -R $INSTALL_PREFIX/etc/ppp
chmod +x $INSTALL_PREFIX/etc/ppp
chmod +x $INSTALL_PREFIX/etc/ppp/ip-up
chmod +x $INSTALL_PREFIX/etc/ppp/ip-down
chmod +x $INSTALL_PREFIX/etc/ppp/peers
chown :vmc $INSTALL_PREFIX/sbin/pppd
chmod +s $INSTALL_PREFIX/sbin/pppd
chmod +x $INSTALL_PREFIX/sbin/pppd

#Configure SELinux
selinux=1
if [ -x /usr/sbin/sestatus ]; then
if (/usr/sbin/sestatus | egrep "SELinux status:.*enabled"); then
	selinux=0
	echo "Configuring SELinux..."
	find $INSTALL_PREFIX/lib -name \*.so* -exec \
		/usr/bin/chcon -t texrel_shlib_t {} \;

	echo "Installing new SELinux modules..."
	for module in $INSTALL_PREFIX/selinux/*.pp; do
		/usr/sbin/semodule -i $module
	done
fi
fi

#udev configuration files
cp $INSTALL_PREFIX/etc/udev/rules.d/*.rules /etc/udev/rules.d/
/sbin/udevcontrol reload_rules

#i18n files
cp -r ./opt/vmc/usr/share/locale/* /usr/share/locale

#gdk-pixbuff generation
export LD_LIBRARY_PATH=$INSTALL_PREFIX/lib
export GDK_PIXBUF_MODULEDIR=$INSTALL_PREFIX/lib/pixbuf-loaders
export GDK_PIXBUF_MODULE_FILE=$INSTALL_PREFIX/etc/gtk/gdk-pixbuf.loaders
$INSTALL_PREFIX/bin/gdk-pixbuf-query-loaders > $INSTALL_PREFIX/etc/gtk/gdk-pixbuf.loaders

#pango.modules
export PANGO_RC_FILE=$INSTALL_PREFIX/etc/pango/pangorc
$INSTALL_PREFIX/bin/pango-querymodules > $INSTALL_PREFIX/etc/pango/pango.modules

#Notification daemon, if needed
#dbus-send --session --print-reply \
#	--dest=org.freedesktop.Notifications \
#	/org/freedesktop/Notifications \
#	org.freedesktop.DBus.Introspectable.Introspect > /dev/null
#if [ $? -eq 1 ]
if [ ! -e /usr/share/dbus-1/services/org.freedesktop.Notifications.service ]
then
	echo "Notification daemon not detected. It's going to be configured..."
	echo "Adding our services dir to file /etc/dbus-1/session.d/vmc.conf..."
	echo "<!DOCTYPE busconfig PUBLIC
 \"-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN\"
 \"http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd\">
<busconfig>
    <servicedir>$INSTALL_PREFIX/share/dbus-1/services/</servicedir>
</busconfig>
" 	> /etc/dbus-1/session.d/vmc.conf
fi

echo "Installing direct access..."
cp -f `find $INSTALL_PREFIX -name vmc.desktop` /usr/share/applications
cp -f `find $INSTALL_PREFIX -name vodafone.png` /usr/share/pixmaps

echo "#!/bin/sh
VMC_PREFIX=$INSTALL_PREFIX
export PATH=\$VMC_PREFIX/bin:\$VMC_PREFIX/sbin:\$VMC_PREFIX/usr/bin:\$PATH
export LD_LIBRARY_PATH=\$VMC_PREFIX/lib:\$LD_LIBRARY_PATH
export PYTHONPATH=\$VMC_PREFIX/lib/python/site-packages

export GDK_PIXBUF_MODULEDIR=\$VMC_PREFIX/lib/pixbuf-loaders
export GDK_PIXBUF_MODULE_FILE=\$VMC_PREFIX/etc/gtk/gdk-pixbuf.loaders

export PANGO_RC_FILE=\$VMC_PREFIX/etc/pango/pangorc
" > /tmp/vmc-bin
chmod +x /tmp/vmc-bin

cp /tmp/vmc-bin /usr/bin/vodafone-mobile-connect-card-driver-for-linux
echo "vodafone-mobile-connect-card-driver-for-linux" >> /usr/bin/vodafone-mobile-connect-card-driver-for-linux

cp /tmp/vmc-bin /usr/bin/vodafone-mobile-connect-card-driver-for-linux-debug
echo "vodafone-mobile-connect-card-driver-for-linux-debug" >> /usr/bin/vodafone-mobile-connect-card-driver-for-linux-debug

mv $INSTALL_PREFIX/libexec/notification-daemon $INSTALL_PREFIX/libexec/notification-daemon-bin
cp /tmp/vmc-bin $INSTALL_PREFIX/libexec/notification-daemon
echo "$INSTALL_PREFIX/libexec/notification-daemon-bin" >> $INSTALL_PREFIX/libexec/notification-daemon

if [ ! -f /etc/lsb-release ]; then
    echo "DISTRIB_ID=\"`cat /etc/*-release | head -n1`\"" > /etc/lsb-release
fi

$INSTALL_PREFIX/usr/bin/lsb_release -i | grep SUSE >/dev/null
suse=$?

if [ $suse -eq 0 ]; then
    chown :uucp /var/lock/
fi

echo -n "Insert users allowed to use this application (space separated): "
read users

if [ ${#users} -eq 0 ]; then
	echo "You can give privileges to users adding them to the groups 'vmc', 'dialout' and probably 'uucp'"
else
	if (cat /etc/group | grep uucp >/dev/null) then uucp=",uucp";fi
	if (cat /etc/group | grep dialout >/dev/null) then dialout=",dialout";fi
	if (cat /etc/group | grep lock > /dev/null) then lock=",lock";fi

	for user in $users
	do
		id $user > /dev/null
		if [ $? -eq 1 ]; then echo "Invalid user $user"; continue;fi

		if [ $suse -eq 0 ]
        	then
			/usr/sbin/usermod $user -A vmc$dialout$uucp$lock
		else
			/usr/sbin/usermod -a -G vmc$dialout$uucp$lock $user
		fi
	done
fi

echo
echo "Installation complete!"
echo
echo "Use vodafone-mobile-connect-card-driver-for-linux command or the direct access in your Internet menu in order to run the application."
