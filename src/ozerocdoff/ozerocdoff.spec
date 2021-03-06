Name:		ozerocdoff
Version:	0.4
Release:	1%{?dist}
Summary:	Tool for switching modes of Option USB devices
Packager:	Andrew Bird <ajb@spheresystems.co.uk>

Group:		System Environment/Base
License:	GPL
URL:		http://www.pharscape.org/ozerocdoff.html
Source0:	ozerocdoff-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%define su111 %(if [ "%{suse_version}" = "1110" ]; then echo 1; else echo 0; fi)

%if 0%{?su111} || 0%{?su112}
Requires:       libusb-0_1-4
%else
Requires:       libusb
%endif

BuildRequires:	libusb-devel


%description
Ozerocdoff - an improved ZeroCD switching utility
This is the improved Option software for temporarily disabling ZeroCD and allowing the modem to be a modem. It has replaced rezero.

%prep
%setup -q


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBNAME=%{_lib}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/sbin/ozerocdoff
/usr/sbin/osetsuspend

/etc/udev/rules.d/51-hso-udev.rules

/usr/%{_lib}/hal/scripts/hal-serial-hsotype
/usr/share/hal/fdi/preprobe/20thirdparty/10-wwan-hso-preprobe.fdi
/usr/share/hal/fdi/information/20thirdparty/10-wwan-quirk.fdi

%config(noreplace) %attr(0644,root,root) /etc/hso-suspend.conf

%doc

%changelog

