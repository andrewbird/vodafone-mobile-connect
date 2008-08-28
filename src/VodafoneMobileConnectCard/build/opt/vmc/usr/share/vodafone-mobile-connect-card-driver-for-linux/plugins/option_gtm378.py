# -*- coding: utf-8 -*-
# Copyright (C) 2006-2008  Vodafone España, S.A.
# Author:  Jaime Soriano
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

__version__ = "$Rev: 1056 $"

from vmc.common.hardware.option import (OptionDBusDevicePlugin,
                                        OptionCustomizer)

# Ulf Michel contributed this info:
# http://forge.vodafonebetavine.net/forum/message.php?msg_id=630
#
# OptionGTM378 integrated in Fuijitsu-Siemens Esprimo Mobile U Series
 
class OptionGTM378(OptionDBusDevicePlugin):
    """
    L{vmc.common.plugin.DBusDevicePlugin} for Option's GTM378
    """
    name = "Option GT M378"
    version = "0.1"
    author = "Ulf Michel"
    custom = OptionCustomizer
    
    __remote_name__ = 'GTM378'

    __properties__ = {
        'usb_device.vendor_id' : [0x0af0],
        'usb_device.product_id': [0x6901],
    }
    
optiongtm378 = OptionGTM378()
