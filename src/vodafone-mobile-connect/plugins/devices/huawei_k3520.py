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

__version__ = "$Rev$"

from vmc.common.hardware.huawei import HuaweiCustomizer, HuaweiDBusDevicePlugin

class HuaweiK3520(HuaweiDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Huawei's K3520"""
    name = "Huawei K3520"
    version = "0.1"
    author = u"Pablo Martí"
    custom = HuaweiCustomizer

    __remote_name__ = "K3520"

    __properties__ = {
        'usb_device.vendor_id': [0x12d1],
        'usb_device.product_id': [0x1001],
    }

