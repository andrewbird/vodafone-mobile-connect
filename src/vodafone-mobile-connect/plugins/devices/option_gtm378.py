# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007  Vodafone España, S.A.
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

from vmc.common.hardware.option import (OptionDBusDevicePlugin,
                                        OptionCustomizer)

# Ulf Michel contributed this info:
# http://forge.vodafonebetavine.net/forum/message.php?msg_id=630
# https://forge.betavine.net/forum/forum.php?thread_id=680&forum_id=20
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
        'usb_device.vendor_id': [0x0af0],
        'usb_device.product_id': [0x6901, 0x6911],
    }

    def preprobe_init(self, ports, info):
        # It would be really cool to use HAL to figure out the port assignment
        # using the 'info.hsotype' provided by ozerocdoff fdi files, but for
        # now just hardcode :-(
        # 0 == 'Diagnostic'
        # 1 == 'Application'
        # 2 == 'Control'
        # 3 == 'Modem'
        if info['usb_device.product_id'] == 0x6911:
            self.hardcoded_ports = (3, 1) # NDIS version
        else:
            pass                          # Original, just probe

optiongtm378 = OptionGTM378()
