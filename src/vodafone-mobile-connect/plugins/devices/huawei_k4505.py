# -*- coding: utf-8 -*-
# Copyright (C) 2006-2009  Vodafone España, S.A.
# Author:  Andrew Bird
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

from vmc.common.hardware.huawei import HuaweiCustomizer, HuaweiDBusDevicePlugin

class HuaweiK4505(HuaweiDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's Vodafone K4505"""
    name = "Huawei K4505"
    version = "0.1"
    author = u"Andrew Bird"
    custom = HuaweiCustomizer

    __remote_name__ = "K4505"

    __properties__ = {
        'usb_device.vendor_id': [0x12d1],
        'usb_device.product_id': [0x1464],
    }

    hardcoded_ports = (0,4) # auto probing can hang

huaweik4505 = HuaweiK4505()

