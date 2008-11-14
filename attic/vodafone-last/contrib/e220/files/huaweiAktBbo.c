/* HUAWEI E220 3G HSDPA modem - Aktivator modemu = aktivuje ttyUSB0 tty USB1 
   bobovsky 11.12.2006
   dalej sa uz pouzije usbserial a usb-storage
   cc huaweiAktBbo.c -lusb  (resp -I. -L.)
   armeb-linux-gcc huaweiAktBbo.c -L. -I. -lusb
*/
/* This file is generated with usbsnoop2libusb.pl from a usbsnoop log file. */
/* Latest version of the script should be in http://iki.fi/lindi/usb/usbsnoop2libusb.pl */

/* Modified by Pablo Martí Gamboa pmarti@warp.es  20 Jun 2007
 * log: commented stuff removed
 *
 * Modified by Pablo Martí Gamboa pmarti@warp.es  13 Jul 2007
 * log: unused stuff removed
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
    ret = usb_release_interface(devh, 0);
    if (!ret)
	printf("failed to release interface: %d\n", ret);
    usb_close(devh);
    if (!ret)
	printf("failed to close interface: %d\n", ret);
    exit(1);
}

struct usb_device *find_device(int vendor, int product) {
    struct usb_bus *bus;
    
    for (bus = usb_get_busses(); bus; bus = bus->next) {
	struct usb_device *dev;
	
	for (dev = bus->devices; dev; dev = dev->next) {
	    if (dev->descriptor.idVendor == vendor
		&& dev->descriptor.idProduct == product)
		return dev;
	}
    }
    return NULL;
}

int main(int argc, char **argv) {
    int ret, vendor, product;
    struct usb_device *dev;
    char buf[65535], *endptr;

    usb_init();
    usb_find_busses();
    usb_find_devices();
    
    printf("Hladam HUAWEI E220 a prepnem na modem - bbo 06\n");
    vendor = 0x12d1;
    product = 0x1003;
    dev = find_device(vendor, product);
    if (dev == NULL) {
        dev = find_device(vendor, 0x1001);
    }
    assert(dev);

    devh = usb_open(dev);
    assert(devh);
    
    signal(SIGTERM, release_usb_device);

    // BBO typ 1 = DEVICE
    ret = usb_get_descriptor(devh, 0x0000001, 0x0000000, buf, 0x0000012);
    usleep(1*1000);
    // BBO typ 2 = CONFIGURATION
    ret = usb_get_descriptor(devh, 0x0000002, 0x0000000, buf, 0x0000009);
    usleep(1*1000);
    // BBO typ 2 = CONFIGURATION
    ret = usb_get_descriptor(devh, 0x0000002, 0x0000000, buf, 0x0000020);
    usleep(1*1000);
    ret = usb_control_msg(devh, USB_TYPE_STANDARD + USB_RECIP_DEVICE, USB_REQ_SET_FEATURE, 00000001, 0, buf, 0, 1000);
    printf("4 set feature request returned %d\n", ret);
    ret = usb_close(devh);
    assert(ret == 0);
    printf("Prepnute-OK, Mas ttyUSB0 ttyUSB1 (cez usbserial vendor=0x12d1 product=0x1003)\n");
    printf("pozri /proc/bus/usb/devices\n");
    return 0;
}
