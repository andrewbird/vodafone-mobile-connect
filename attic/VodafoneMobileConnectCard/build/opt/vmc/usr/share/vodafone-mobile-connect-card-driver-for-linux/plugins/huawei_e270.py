# -*- coding: utf-8 -*-
# Copyright (C) 2006-2008  Vodafone España, S.A.
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

__version__ = "$Rev: 1203 $"

from vmc.common.exceptions import DeviceLacksExtractInfo
from vmc.common.hardware.huawei import HuaweiE2XXCustomizer
from vmc.common.plugin import DBusDevicePlugin

class HuaweiE270(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's E270"""
    name = "Huawei E270"
    version = "0.1"
    author = u"Pablo Martí"
    custom = HuaweiE2XXCustomizer
    
    __remote_name__ = "E270"

    __properties__ = {
        'usb_device.vendor_id': [0x12d1],
        'usb_device.product_id': [0x1003],
    }
    
    def extract_info(self, children):
        # HW 270 uses ttyUSB0 and ttyUSB1
        for device in children:
            try:
                if device['serial.port'] == 1: # control port
                    self.cport = device['serial.device'].encode('utf8')
                elif device['serial.port'] == 0: # data port
                    self.dport = device['serial.device'].encode('utf8')
            except KeyError:
                pass
        
        if not self.cport or not self.dport:
            raise DeviceLacksExtractInfo(self)

huaweiE270 = HuaweiE270()
