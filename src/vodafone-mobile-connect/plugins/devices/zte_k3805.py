# -*- coding: utf-8 -*-
# Copyright (C) 2009  Vodafone España, S.A.
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

from vmc.common.exceptions import DeviceLacksExtractInfo
from vmc.common.hardware.icera import IceraCustomizer, IceraDBusDevicePlugin


class ZTEK3805(IceraDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for ZTE's K3805-Z"""
    name = "ZTE K3805-Z"
    version = "0.1"
    author = "Andrew Bird"
    custom = IceraCustomizer

    __remote_name__ = "K3805-z"

    __properties__ = {
        'usb_device.vendor_id': [0x19d2],
        'usb_device.product_id': [0x1003],
    }

    hardcoded_ports = (0, 1)

zte_k3805 = ZTEK3805()
