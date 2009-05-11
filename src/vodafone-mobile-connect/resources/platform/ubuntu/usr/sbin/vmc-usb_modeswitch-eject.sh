#!/bin/sh

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

# Need to wait for the device to settle before sending the command
sleep 1

# Standard SCSI eject 
usb_modeswitch -v ${VID} -p ${PID} -M 5553424312345678000000000000061b000000020000000000000000000000 -R 1 

# Storage passthrough
#usb_modeswitch -v ${VID} -p ${PID} -M 55534243123456782400000080000C85000000240000000000000000000000 -R 1

