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

"""
DevicePlugin for the Sierra Wireless 8775 datacard
"""

__version__ = "$Rev: 1203 $"

from vmc.common.exceptions import DeviceLacksExtractInfo
from vmc.common.plugin import DBusDevicePlugin

from vmc.common.hardware.sierra import SierraWirelessCustomizer

class SierraWireless8775(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for SierraWireless 875"""
    name = "SierraWireless 8775"
    version = "0.1"
    author = "Rafael Treviño"
    custom = SierraWirelessCustomizer
    
    __remote_name__ = "MC8775V"   #response from AT+CGMM

    __properties__ = {
        'usb_device.vendor_id' : [0x1199],
        'usb_device.product_id': [0x6813, 0x6812],
    }
    
    def extract_info(self, children):
        # Sierra MC8775 uses ttyUSB0 and ttyUSB2
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

sierrawireless8775 = SierraWireless8775()
