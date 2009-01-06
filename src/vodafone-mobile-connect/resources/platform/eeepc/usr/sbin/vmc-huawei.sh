#!/bin/bash

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

if [ -d /sys/bus/usb-serial/drivers/option1/ttyUSB1 ] ; then
	# already switched and module loaded successfully
	exit 0
fi

# let the device settle
sleep 1

# seems to be switched already on some devices, not sure why
usb_modeswitch -v ${VID} -p ${PID} -H 1


# load the driver if necessary
[ -f /sys/bus/usb-serial/drivers/option1/new_id ] || modprobe -a option
echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id

