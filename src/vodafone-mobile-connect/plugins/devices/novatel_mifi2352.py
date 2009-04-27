# -*- coding: utf-8 -*-
# Copyright (C) 2009  Vodafone España, S.A.
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

__version__ = "$Rev: 1172 $"

from vmc.common.hardware.novatel import NovatelCustomizer
from vmc.common.sim import SIMBaseClass
from vmc.common.plugin import DBusDevicePlugin
import serial


class NovatelMiFiSIMClass(SIMBaseClass):
    """
    Novatel MiFi SIM Class
    """
    def __init__(self, sconn):
        super(NovatelMiFiSIMClass, self).__init__(sconn)

    def initialize(self, set_encoding=True):
        d = super(NovatelMiFiSIMClass, self).initialize(set_encoding=set_encoding)
        def init_callback(size):
            # setup SIM storage defaults
            self.sconn.send_at('AT+CPMS="SM","SM","SM"')
            return size

        d.addCallback(init_callback)
        return d


class NovatelMiFiDBusDevicePlugin(DBusDevicePlugin):
    """DBusDevicePlugin for Novatel MiFi"""
    simklass = NovatelMiFiSIMClass

    def __init__(self):
        super(NovatelMiFiDBusDevicePlugin, self).__init__()


class NovatelMiFi2352(NovatelMiFiDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Novatel's MiFi 2352"""
    name = "Novatel MiFi2352"
    version = "0.1"
    author = u"Andrew Bird"
    custom = NovatelCustomizer

    __remote_name__ = "MiFi2352 "

    __properties__ = {
        'usb_device.vendor_id' : [0x1410],
        'usb_device.product_id' : [0x7001],
    }

    def preprobe_init(self, ports, info):
        # Novatel secondary port needs to be flipped from DM to AT mode
        # before it will answer our AT queries. So the primary port
        # needs this string first or auto detection of ctrl port fails.
        # Note: Early models/firmware were DM only
        ser = serial.Serial(ports[0], timeout=1)
        ser.write('AT$NWDMAT=1\r\n')
        ser.close()


novatelmifi2352 = NovatelMiFi2352()
