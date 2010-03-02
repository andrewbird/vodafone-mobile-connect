#!/bin/bash

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

# it may not use this driver if the product id is already 
# compiled into another driver, it's best to blacklist pl2303 and onda
[ -f /sys/bus/usb-serial/drivers/option1/new_id ] || modprobe -a option
echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id

