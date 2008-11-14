#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2006-2008  Vodafone España, S.A.
# Author:  Rafael Treviño
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import signal
import time
import usb
import sys

def release_usb_device(dummy):
    return devh.releaseInterface()

def find_device(vendor, product):
    for bus in usb.busses():
        for device in bus.devices:
            if device.idVendor == vendor \
                    and device.idProduct == product:
                        return device
    return None

def usb_open(dev):
    devh = dev.open()
    devh.detachKernelDriver(0) # Should this be iface.interfaceNumber?
    conf = dev.configurations[0]
    iface = conf.interfaces[0][0]
    devh.setConfiguration(conf)
    devh.claimInterface(iface)
    devh.setAltInterface(iface)
    devh.reset()
    return devh

if __name__ == '__main__':
    print 'Hladam HUAWEI E220 a prepnem na modem - bbo 06'
    vendor  = 0x12d1
    product = 0x1003

    dev = find_device(vendor, product)
    if dev == None:
        product = 0x1001
        dev = find_device(vendor, 0x1001)
    assert dev

    devh = usb_open(dev)
    # devh = dev.open()
    assert devh

    signal.signal(signal.SIGTERM, release_usb_device)

    # BBO typ 1 = DEVICE
    ret = devh.getDescriptor(0x00000001, 0x00000000, 0x00000012)
    time.sleep(0.001)
    # BBO typ 2 = CONFIGURATION
    ret = devh.getDescriptor(0x00000002, 0x00000000, 0x00000009)
    time.sleep(0.001)
    # BBO typ 2 = CONFIGURATION
    ret = devh.getDescriptor(0x00000002, 0x00000000, 0x00000020)
    time.sleep(0.001)
    reqBuffer = [0] * 8
    ret = devh.controlMsg(usb.TYPE_STANDARD + usb.RECIP_DEVICE, usb.REQ_SET_FEATURE, reqBuffer, value=00000001, index=0, timeout=1000)
    print '4 set feature request returned %d' % ret
    # ret = release_usb_device(0)
    # assert ret == 0
    print 'Prepnute-OK, Mas ttyUSB0 ttyUSB1 (cez usbserial vendor=0x12d1 product=%x)' % product
    print 'pozri /proc/bus/usb/devices'
    sys.exit(0)
