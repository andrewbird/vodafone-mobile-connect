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
from vmc.common.hardware.zte import ZTECustomizer, ZTEDBusDevicePlugin

class ZTEK3520(ZTEDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for ZTE's version of Vodafone's K3520"""
    name = "ZTE K3520-Z"
    version = "0.1"
    author = "Andrew Bird"
    custom = ZTECustomizer

    __remote_name__ = "K3520-Z"

    __properties__ = {
        'usb_device.vendor_id': [0x19d2],
        'usb_device.product_id': [0x0025, 0x0055], # depends on firmware revision
    }

    # K3520-Z uses ttyUSB1(data) and ttyUSB3(status)
    hardcoded_ports = (1, 3)

zte_k3520 = ZTEK3520()

