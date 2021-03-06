# -*- coding: utf-8 -*-
# Copyright (C) 2006-2009  Vodafone España, S.A.
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

from vmc.common.hardware.huawei import HuaweiDBusDevicePlugin

from vmc.common.plugins.huawei_e160b import HuaweiE160B
from vmc.common.plugins.huawei_e172 import HuaweiE172
from vmc.common.plugins.huawei_e220 import HuaweiE220
from vmc.common.plugins.huawei_e270 import HuaweiE270
from vmc.common.plugins.huawei_e272 import HuaweiE272
from vmc.common.plugins.huawei_e510 import HuaweiE510
from vmc.common.plugins.huawei_e620 import HuaweiE620
from vmc.common.plugins.huawei_e660 import HuaweiE660
from vmc.common.plugins.huawei_e660a import HuaweiE660A
from vmc.common.plugins.huawei_e870 import HuaweiE870
from vmc.common.plugins.huawei_e3735 import HuaweiE3735

from vmc.common.plugins.huawei_k2540 import HuaweiK2540
from vmc.common.plugins.huawei_k3520 import HuaweiK3520
from vmc.common.plugins.huawei_k3565 import HuaweiK3565
from vmc.common.plugins.huawei_k3715 import HuaweiK3715

from vmc.common.plugins.huawei_em730v import HuaweiEM730V
from vmc.common.plugins.huawei_em770 import HuaweiEM770

from vmc.common.plugins.huawei_b970 import HuaweiB970


class HuaweiEXXX1003(HuaweiDBusDevicePlugin):
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
            'E870': HuaweiE870,      # Expresscards

            'E160B': HuaweiE160B,     # USB Sticks
            'E17X': HuaweiE172,
            'E220': HuaweiE220,
            'E270': HuaweiE270,
            'E272': HuaweiE272,
            'K3565': HuaweiK3565,

            'B970': HuaweiB970,      # Routers

            'default': HuaweiE220,
        }


class HuaweiEXXX1001(HuaweiDBusDevicePlugin):
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
            'E510': HuaweiE510,     # Cardbus
            'E620': HuaweiE620,
            'E660': HuaweiE660,
            'E660A': HuaweiE660A,

            'E3735': HuaweiE3735,   # Expresscards

            'K2540': HuaweiK2540,    # USB Sticks
            'K3520': HuaweiK3520,
            'K3565': HuaweiK3565,
            'K3715': HuaweiK3715,

            'EM730V': HuaweiEM730V,  # Embedded Modules
            'EM770': HuaweiEM770,

            'default': HuaweiE660,
        }


huaweiexxx1003 = HuaweiEXXX1003()
huaweiexxx1001 = HuaweiEXXX1001()
