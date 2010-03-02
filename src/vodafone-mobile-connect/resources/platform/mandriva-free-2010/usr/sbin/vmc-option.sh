#!/bin/bash

VID="$1"
PID="$2"
OP="$3"

PATH=/usr/bin:/bin:/usr/sbin:/sbin


case "${OP}" in
	flip)	# special case for flipping ZeroCD to modem mode
		modprobe -r option
		modprobe -r pl2303
		modprobe -r usbserial
		usb_modeswitch -v ${VID} -p ${PID} \
			-m 0x05 -M 55534243123456780000000000000601000000000000000000000000000000
		;;

	*)	# default action is to load option driver with supplied IDs
		modprobe -a option
		echo "0x${VID} 0x${PID}" > /sys/bus/usb-serial/drivers/option1/new_id
		;;
esac


