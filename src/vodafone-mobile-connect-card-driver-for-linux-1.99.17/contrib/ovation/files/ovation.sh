#! /bin/bash
/sbin/modprobe -r usbserial
eject /dev/novatel-storage
/sbin/modprobe usbserial vendor=0x1410 product=0x4400
