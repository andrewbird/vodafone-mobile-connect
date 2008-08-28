# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007  Vodafone España, S.A.
# Author:  Pablo Martí
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

__version__ = "$Rev: 1209 $"

from vmc.common.exceptions import DeviceLacksExtractInfo
from vmc.common.hardware.zte import ZTECustomizer
from vmc.common.plugin import DBusDevicePlugin

class ZTEMF620(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's E272"""
    name = "ZTE MF620"
    version = "0.1"
    author = "Zhao Ming"
    custom = ZTECustomizer
    
    __remote_name__ = "MF620"

    __properties__ = {
        'usb_device.vendor_id': [0x19d2],
        'usb_device.product_id': [0x0001],
    }
    
    def extract_info(self, children):
        # MF620 uses ttyUSB0 and ttyUSB2
        for device in children:
            try:
                if device['serial.port'] == 2: # control port
                    self.cport = device['serial.device'].encode('utf8')
                elif device['serial.port'] == 0: # data port
                    self.dport = device['serial.device'].encode('utf8')
            except KeyError:
                pass
        
        if not self.cport or not self.dport:
            raise DeviceLacksExtractInfo(self)

zte_mf620= ZTEMF620()

