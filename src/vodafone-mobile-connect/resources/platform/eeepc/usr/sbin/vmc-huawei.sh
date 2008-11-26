#!/bin/bash

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

if [ -e /dev/ttyUSB1 ] ; then 
   # switched already :-)
   exit 0
fi

usb_modeswitch -v ${VID} -p ${PID} -H 1

# it may not use this driver if the product id is already 
# compiled into another driver
# best to blacklist pl2303
modprobe -a option
echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id

