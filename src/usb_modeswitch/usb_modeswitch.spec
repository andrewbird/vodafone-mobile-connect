Name:		usb_modeswitch
Version:	0.9.4
Release:	1%{?dist}
Summary:	Generic tool for switching modes of USB devices	
Packager:	Andrew Bird <ajb@spheresystems.co.uk>

Group:		System Environment/Base	
License:	GPL	
URL:		http://www.draisberghof.de/usb_modeswitch/
Source0:	usb_modeswitch-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libusb-devel
Requires:	libusb

%description
USB_ModeSwitch is (surprise!) a mode switching tool for controlling "flip flop" (multiple device) USB gear. Several new USB devices (especially high-speed wireless WAN stuff, they're expensive anyway) have their MS Windows drivers onboard; when plugged in for the first time they act like a flash storage and start installing the driver from there. After that (and on every consecutive plugging) this driver switches the mode internally, the storage device vanishes (in most cases), and a new device (like an USB modem) shows up. The WWAN gear maker Option calls that feature "ZeroCD (TM)".

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
/usr/sbin/usb_modeswitch
%config(noreplace) %attr(0644,root,root) /etc/usb_modeswitch.conf
%doc



%changelog

