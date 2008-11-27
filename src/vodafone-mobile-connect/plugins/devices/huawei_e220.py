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

__version__ = "$Rev: 1172 $"

from vmc.common.sim import SIMBaseClass
from vmc.common.plugin import DBusDevicePlugin
from vmc.common.hardware.huawei import HuaweiE2XXCustomizer

class HuaweiE220SIMClass(SIMBaseClass):
    """Huawei E220 SIM Class"""
    def __init__(self, sconn):
        super(HuaweiE220SIMClass, self).__init__(sconn)
    
    def postinit(self):
        d = super(HuaweiE220SIMClass, self).postinit(set_encoding=False)
        def postinit_cb(size):
            self.sconn.get_smsc()
            # before switching to UCS2, we need to get once the SMSC number
            # otherwise as soon as we send a SMS, the device would reset
            # as if it had been unplugged and replugged to the system
            def process_charset(charset):
                """
                Do not set charset to UCS2 if is not necessary, returns size
                """
                if charset == "UCS2":
                    self.set_charset(charset)
                    return size
                else:
                    d = self.sconn.set_charset("UCS2")
                    d.addCallback(lambda ignored: size)
                    return d
            
            d2 = self.sconn.get_charset()
            d2.addCallback(process_charset)
            return d2

        d.addCallback(postinit_cb)
        return d


class HuaweiE220(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's E220"""
    name = "Huawei E220"
    version = "0.1"
    author = u"Pablo Martí"
    custom = HuaweiE2XXCustomizer
    simklass = HuaweiE220SIMClass
    
    __remote_name__ = "E220"

    __properties__ = {
        'usb_device.vendor_id': [0x12d1],
        'usb_device.product_id': [0x1003, 0x1004],
    }

