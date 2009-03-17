# -*- coding: utf-8 -*-
# Copyright (C) 2009 Vodafone España, S.A.
# Author: Andrew Bird
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

# Note: For this device to be identified by the OS the following two prerequisties
# must be statisfied:
# Kernel module 'hso' must be installed
# Option storage flipping and HAL configuration package 'ozerocdoff' must be installed

class OptionK3760(OptionDBusDevicePlugin):
    """
    L{vmc.common.plugin.DBusDevicePlugin} for Option's version of Vodafone K3760
    """
    name = "Option K3760"
    version = "0.1"
    author = "Andrew Bird"
    custom = OptionCustomizer
    
    __remote_name__ = 'GlobeTrotter HSUPA Modem'

    __properties__ = {
        'usb_device.vendor_id' : [0x0af0],
        'usb_device.product_id': [0x7501],
    }

    def preprobe_init(self, ports, info):
        # It would be really cool to use HAL to figure out the port assignment
        # using the 'info.hsotype' provided by ozerocdoff fdi files, but for now
        # just hardcode :-(
        # 0 == 'Diagnostic'
        # 1 == 'Application'
        # 2 == 'Control'
        # 3 == 'Modem'
        self.hardcoded_ports = (3,1)
    
optionk3760 = OptionK3760()
