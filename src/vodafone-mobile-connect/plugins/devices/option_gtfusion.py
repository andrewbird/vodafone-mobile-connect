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

from vmc.common.hardware.option import (OptionDBusDevicePlugin,
                                        OptionCustomizer)

# Stefano Rivera contributed this info through email on 20 Sept 2007
 
class OptionGTFusion(OptionDBusDevicePlugin):
    """
    L{vmc.common.plugin.DBusDevicePlugin} for Option's GT Fusion
    """
    name = "Option GlobeTrotter Fusion"
    version = "0.1"
    author = "Stefano Rivera"
    custom = OptionCustomizer
    
    __remote_name__ = 'GlobeTrotter Fusion'

    __properties__ = {
        'usb_device.vendor_id' : [0x0af0],
        'usb_device.product_id': [0x6000],
    }
    
optiongtfusion = OptionGTFusion()
