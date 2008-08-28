# -*- coding: utf-8 -*-
# Author:  Adam King - heavily based on Pablo Marti's U630 plugin
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

from vmc.common.plugin import DBusDevicePlugin
from vmc.common.exceptions import DeviceLacksExtractInfo

from vmc.common.hardware.novatel import NovatelCustomizer

class NovatelU740(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Novatel's U740"""
    name = "Novatel U740"
    version = "0.1"
    author = "Adam King"
    custom = NovatelCustomizer

    __remote_name__ = "Merlin U740 (HW REV [0:33])"

    __properties__ = {
        'usb_device.vendor_id' : [0x1410],
        'usb_device.product_id' : [0x1400, 0x1410]
    }

    def extract_info(self, children):
        # U740 uses ttyUSB0
        for device in children:
            try:
                if device['serial.port'] == 0: #data port
                    self.dport = device['serial.device'].encode('utf8')
            except KeyError:
                pass

        if not self.dport:
            raise DeviceLacksExtractInfo(self)

novatelu740 = NovatelU740()
