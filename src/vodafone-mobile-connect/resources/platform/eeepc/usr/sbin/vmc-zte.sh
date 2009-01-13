#!/bin/bash

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

# load the driver if necessary
[ -f /sys/bus/usb-serial/drivers/option1/new_id ] || modprobe -a option
echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id

