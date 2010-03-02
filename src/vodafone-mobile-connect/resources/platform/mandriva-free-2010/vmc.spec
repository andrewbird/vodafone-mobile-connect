Name:		vmc
Version:	2.0.0
Release:	6%{?dist}
Summary:	3G Manager for Linux
Packager:	Andrew Bird <ajb@spheresystems.co.uk>

Group:		Applications/Telephony
License:	GPL
URL:		http://www.vodafonebetavine.net/web/linux_drivers
Source0:	vmc-2.0.0.tar.bz2
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	usb_modeswitch wvdial hal lsb python-serial python-twisted python-twisted-conch python-notify python-pytz python-gobject python-dbus python-cairo pycrypto pygtk2.0 >= 2.14.0 pygtk2.0-libglade gnome-python

%description
OSS 3G manager for Linux

%prep
%setup -q


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%attr(0755,root,root) /etc/ppp/ip-down.d/0095vmc
%attr(0755,root,root) /etc/ppp/ip-up.d/0095vmc
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-huawei.rules
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-novatel.rules
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-option.rules
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-zte.rules
%attr(0644,root,root) /etc/modprobe.d/blacklist-vmc.conf
#%attr(0644,root,root) /etc/dbus-1/system.d/vmc.conf

/usr

%doc

%post

groupadd -f dialout
chown :dialout /etc/ppp/chap-secrets /etc/ppp/pap-secrets /etc/ppp/peers
chmod 660 /etc/ppp/chap-secrets /etc/ppp/pap-secrets
chmod 775 /etc/ppp/peers

chown :dialout /usr/sbin/pppd
chmod 4754 /usr/sbin/pppd

# initialise Twisted's plugin cache
/usr/bin/twistd --help >/dev/null 2>&1

# tickle UDEV
(udevadm control --reload-rules 2>/dev/null || udevadm control --reload_rules)

%postun
if [ "$1" = "0" ] ; then # last instance of package being removed

	chown :root /usr/sbin/pppd
	chmod 555 /usr/sbin/pppd

	chown :root /etc/ppp/chap-secrets /etc/ppp/pap-secrets /etc/ppp/peers
	chmod 600 /etc/ppp/chap-secrets /etc/ppp/pap-secrets
	chmod 755 /etc/ppp/peers
	#groupdel dialout
fi


%changelog

