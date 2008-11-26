#!/bin/bash

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

modprobe -r option
modprobe -r pl2303
modprobe -r usbserial
usb_modeswitch -v ${VID} -p ${PID} \
               -m 0x05 -M 55534243123456780000000000000601000000000000000000000000000000

sleep 5

# we have to assume that the device is known to the driver or hardcode it here
modprobe -a option
echo "0x0af0 0x6600" > /sys/bus/usb-serial/drivers/option1/new_id

