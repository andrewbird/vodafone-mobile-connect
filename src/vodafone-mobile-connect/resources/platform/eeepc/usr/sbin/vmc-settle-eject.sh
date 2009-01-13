#!/bin/bash

# Some devices will switch straight away, others like ZTE K3565-Z need to
# settle for a while before the eject will flip the device

DEVICE="$1"
WAIT="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

( 
	for i in `seq ${WAIT}` ; do
		eject ${DEVICE}

	   	sleep 1

		if [ -d /sys/bus/usb-serial/drivers/option1/ttyUSB1 ] ; then
			exit 0
		fi
	done

) < /dev/null > /dev/null 2>&1 &


