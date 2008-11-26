#!/bin/bash

# for Ovation device
/sbin/modprobe -r option
eject /dev/novatel-storage

/sbin/modprobe -a option
echo "0x1410 0x4400" > /sys/bus/usb-serial/drivers/option1/new_id

