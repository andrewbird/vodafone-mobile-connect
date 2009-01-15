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

from vmc.common.plugin import DBusDevicePlugin

from vmc.common.plugins.huawei_e172 import HuaweiE172
from vmc.common.plugins.huawei_e220 import HuaweiE220
from vmc.common.plugins.huawei_e270 import HuaweiE270
from vmc.common.plugins.huawei_e272 import HuaweiE272
from vmc.common.plugins.huawei_e620 import HuaweiE620
from vmc.common.plugins.huawei_e660 import HuaweiE660
from vmc.common.plugins.huawei_e660a import HuaweiE660A
from vmc.common.plugins.huawei_k3520 import HuaweiK3520
from vmc.common.plugins.huawei_k3715 import HuaweiK3715
from vmc.common.plugins.huawei_em730v import HuaweiEM730V


class HuaweiEXXX1003(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's 1003 family"""
    name = "Huawei EXXX"
    version = "0.1"
    author = u"Pablo Martí"
    
    __remote_name__ = "EXXX"

    __properties__ = {
        'usb_device.vendor_id': [0x12d1],
        'usb_device.product_id': [0x1003, 0x1004],
    }

    def __init__(self):
        super(HuaweiEXXX1003, self).__init__()

        self.mapping = {
            'E17X' : HuaweiE172,
            'E220' : HuaweiE220,
            'E270' : HuaweiE270,
            'E272' : HuaweiE272,
            'K3565' : HuaweiK3565,

            'default' : HuaweiE220,
        }

class HuaweiEXXX1001(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's 1001 family"""
    name = "Huawei EXXX"
    version = "0.1"
    author = u"Pablo Martí"

    __remote_name__ = None

    __properties__ = {
        'usb_device.vendor_id': [0x12d1],
        'usb_device.product_id': [0x1001],
    }

    def __init__(self):
        super(HuaweiEXXX1001, self).__init__()

        self.mapping = {
            'E660'  : HuaweiE660,
            'E660A' : HuaweiE660A,
            'E620'  : HuaweiE620,
            'K3520' : HuaweiK3520,
            'K3715' : HuaweiK3715,
            'EM730V' : HuaweiEM730V,

            'default' : HuaweiE660,
        }

huaweiexxx1003 = HuaweiEXXX1003()
huaweiexxx1001 = HuaweiEXXX1001()
