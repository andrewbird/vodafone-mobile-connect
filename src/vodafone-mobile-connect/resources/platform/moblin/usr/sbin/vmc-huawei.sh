#!/bin/bash

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

modprobe -r option
modprobe -r pl2303
modprobe -r usbserial
usb_modeswitch -v ${VID} -p ${PID} -H 1

# may not use this driver if the product id is already compiled into another driver
modprobe -a option
echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id

