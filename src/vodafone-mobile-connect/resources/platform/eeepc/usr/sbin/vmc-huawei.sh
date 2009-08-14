#!/bin/bash

VID="$1"
PID="$2"
SWT="$3"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

if [ -d /sys/bus/usb-serial/drivers/option1/ttyUSB1 ] ; then
	# already switched and module loaded successfully
	exit 0
fi

# let the device settle
sleep 1

if [ "${SWT}" = "yes" ] ; then
    usb_modeswitch -v ${VID} -p ${PID} -H 1
fi

# unload the usb_storage driver, eeepc version incorrectly claims tty devs
modprobe -r option
modprobe -r usb_storage
modprobe -a option
echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id

