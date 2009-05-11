Name:		vmc
Version:	1.99.17
Release:	6%{?dist}
Summary:	3G Manager for Linux
Packager:	Andrew Bird <ajb@spheresystems.co.uk>

Group:		Applications/Telephony
License:	GPL	
URL:		http://www.vodafonebetavine.net/web/linux_drivers
Source0:	vmc-1.99.17.tar.bz2
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	usb_modeswitch >= 0.9.7, redhat-lsb, pyserial, python-sqlite2, python-twisted, pytz, gnome-python2-libegg

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

%attr(0755,root,root) /etc/ppp/ip-down.local
%attr(0755,root,root) /etc/ppp/ip-up.local
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-huawei.rules
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-novatel.rules
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-option.rules
%attr(0644,root,root) /etc/udev/rules.d/45-vmc-zte.rules
%attr(0644,root,root) /etc/modprobe.d/blacklist-vmc

/usr

%doc

%post
chown :dip /etc/ppp/chap-secrets /etc/ppp/pap-secrets /etc/ppp/peers
chmod 660 /etc/ppp/chap-secrets /etc/ppp/pap-secrets
chmod 775 /etc/ppp/peers

chown :dip /usr/sbin/pppd
chmod 4754 /usr/sbin/pppd

%postun
if [ "$1" = "0" ] ; then # last instance of package being removed
	chown :root /usr/sbin/pppd
	chmod 555 /usr/sbin/pppd

	chown :root /etc/ppp/chap-secrets /etc/ppp/pap-secrets /etc/ppp/peers
	chmod 600 /etc/ppp/chap-secrets /etc/ppp/pap-secrets
	chmod 755 /etc/ppp/peers
fi

%changelog

