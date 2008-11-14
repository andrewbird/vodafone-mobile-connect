/*
  Mode switcher for Option Icon 3G+ USB box

  Copyright (C) 2006  Josua Dietze  (digidietze nospam t-online spamno de)

  Triggers the switching of the box from storage device mode
  to modem (serial) device mode.

  Created with help from usbsnoop2libusb.pl (http://iki.fi/lindi/usb/usbsnoop2libusb.pl)

  Version 0.2, 2006/09/25
    Code cleaning, more messages
  Version 0.1, 2006/09/24
    Just very basic functionality ...


  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details:

  http://www.gnu.org/licenses/gpl.txt

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <signal.h>
#include <ctype.h>
#include <usb.h>

struct usb_dev_handle *devh;

void release_usb_device(int dummy) {
    int ret;
    printf("Program cancelled by system. Bye\n\n");
    ret = usb_release_interface(devh, 0);
    if (!ret)
	printf(" Oops, failed to release interface: %d\n", ret);
    usb_close(devh);
    if (!ret)
	printf(" Oops, failed to close interface: %d\n", ret);
    printf("\n");
    exit(1);
}

struct usb_device *find_device(int vendor, int product) {
    struct usb_bus *bus;
    struct usb_device *right_dev;
    right_dev = NULL;
    
    printf("Looking for Option Icon USB 3G+ box ...\n");
    for (bus = usb_get_busses(); bus; bus = bus->next) {
	struct usb_device *dev;
	
	for (dev = bus->devices; dev; dev = dev->next) {
	    if (dev->descriptor.idVendor == vendor && dev->descriptor.idProduct == product) {
		right_dev = dev;
	    }
	    if (dev->descriptor.idVendor == 0x0af0 && dev->descriptor.idProduct == 0x6600) {
	        printf("Found box in modem mode. Switching not necessary. Bye\n\n");
		exit(0);
	    }
	}
    }
    if (right_dev != NULL)
	printf("Found box in storage mode. Preparing for switching ...\n");
    else {
	printf("No Option Icon box found. Is it connected? Bye\n\n");
	exit(0);
    }
    return right_dev;
}

int main(int argc, char **argv) {
    int ret;
    int vendor = 0x05c6;
    int product = 0x1000;

    struct usb_device *dev;
    char buf[65535];

    printf("\n * icon_switch: tool for changing USB mode of Option Icon 3G+ box\n");
    printf(" * (C) Josua Dietze 2006\n");
    printf(" * Works with libusb 0.1.12 and probably other versions\n\n");

    usb_init();
    usb_find_busses();
    usb_find_devices();

    dev = find_device(vendor, product);
    assert(dev);

    devh = usb_open(dev);
    assert(devh);
    
    signal(SIGTERM, release_usb_device);

    printf("Looking for active storage driver ...\n");
    ret = usb_get_driver_np(devh, 0, buf, sizeof(buf));
    if (ret == 0) {
	printf(" OK, driver found (\"%s\"), attempting to detach it ...\n", buf);
	ret = usb_detach_kernel_driver_np(devh, 0);
	if (ret == 0)
    	    printf(" OK, driver \"%s\" successfully detached\n", buf);
	else
    	    printf(" Oops, driver \"%s\" detach failed with error %d. Trying to continue ...\n", buf, ret);
    } else {
        printf("No driver found. Box was not initialized. Can't communicate. Bye\n\n");
	exit(1);
    }
    ret = usb_claim_interface(devh, 0);
    if (ret != 0) {
	printf("Could not claim interface (error %d). Can't communicate. Bye\n\n", ret);
	exit(1);
    }
    
    ret = usb_set_altinterface(devh, 0);
    assert(ret >= 0);
 
 
    memcpy(buf, "\x55\x53\x42\x43\x70\x6e\xde\x86\x00\x00\x00\x00\x00\x00\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 0x000001f);
    ret = usb_bulk_write(devh, 0x00000005, buf, 0x000001f, 1000);
    if (ret >= 0 )
	printf("Device change command successfully sent. Box probably switched.\nLook at /var/log/syslog for result ... Bye\n\n");
    else
	printf("Device change command returned error %d", ret);
 
    ret = usb_release_interface(devh, 0);
    assert(ret == 0);

    ret = usb_close(devh);
    assert(ret == 0);

    return 0;
}
