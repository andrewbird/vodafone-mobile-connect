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

from vmc.common.hardware.zte import ZTECustomizer
from vmc.common.plugin import DBusDevicePlugin

class ZTEK3565(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for ZTE's version of Vodafone's K3565"""
    name = "Vodafone K3565-Z"
    version = "0.1"
    author = "Andrew Bird"
    custom = ZTECustomizer
    
    __remote_name__ = "K3565-Z"

    __properties__ = {
        'usb_device.vendor_id': [0x19d2],
        'usb_device.product_id': [0x0049, 0x0052], # depends on firmware version
    }
    
# K3565-Z uses ttyUSB2(data) and ttyUSB1(status)
# Leave this for reference, since new plugin layer might not 
# recognise that the data and control ports are not the usual way around

zte_k3520 = ZTEK3520()
