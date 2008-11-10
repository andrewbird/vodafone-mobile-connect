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

class OptionNozomi(OptionDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Option's Nozomi"""
    name = "Option GlobeTrotter 3G+"
    version = "0.1"
    author = u"Pablo Martí"
    custom = OptionCustomizer
    
    __remote_name__ = "GlobeTrotter 3G+"
    
    __properties__ = {
        'pci.vendor_id' : [0x1931],
        'pci.product_id' : [0xc],
    }

option_nozomi = OptionNozomi()
