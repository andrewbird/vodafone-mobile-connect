#!/bin/sh

VID="$1"
PID="$2"

PATH=/usr/bin:/bin:/usr/sbin:/sbin

# Need to wait for the device to settle before sending the command
sleep 1

# Huawei recommended switch sequence
usb_modeswitch -v ${VID} -p ${PID} -M 55534243EE0000006000000000000611062000000000000000000000000000

