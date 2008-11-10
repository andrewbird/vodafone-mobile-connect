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

__version__ = "$Rev$"

from vmc.common.hardware.sonyericsson import SonyEricssonCustomizer
from vmc.common.plugin import RemoteDevicePlugin, DBusDevicePlugin

from vmc.common.middleware import SIMCardConnAdapter
from vmc.common.exceptions import DeviceLacksExtractInfo

class K610iSIMCardConnAdapter(SIMCardConnAdapter):
    def set_charset(self, charset):
        """
        Some actions fail with UCS2
        """
        if charset == 'UCS2':
            d = super(K610iSIMCardConnAdapter, self).set_charset('IRA')
        else:
            d = super(K610iSIMCardConnAdapter, self).set_charset(charset)
        d.addCallback(lambda ignord: self.device.sim.set_charset(charset))
        return d

class SonyEricssonK610iCustomizer(SonyEricssonCustomizer):
    adapter = K610iSIMCardConnAdapter

class SonyEricssonK610iBT(RemoteDevicePlugin):
    """L{vmc.common.plugin.RemoteDevicePlugin} for SonyEricsson's K610i"""
    name = "SonyEricsson K610i"
    version = "0.1"
    author = u"Pablo Martí"
    custom = SonyEricssonK610iCustomizer

    __remote_name__ = "AAD-3022041-BV"

class SonyEricssonK610iUSB(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Sony Ericsson k610i"""
    name = "Sony Ericsson K610i"
    version = "0.1"
    author = u"Jaime Soriano"
    custom = SonyEricssonK610iCustomizer

    __remote_name__ = "AAD-3022041-BV"

    __properties__ = {
        'usb_device.vendor_id': [0x0fce],
        'usb_device.product_id': [0xd046],
    }

    def extract_info(self, children):
        for device in children:
            try:
                if device['serial.port'] == 0: #data port
                    self.dport = device['serial.device'].encode('utf8')
            except KeyError:
                pass
        
        if not self.dport:
            raise DeviceLacksExtractInfo(self)

sonyericsson_k610iBT = SonyEricssonK610iBT()
sonyericsson_k610iUSB = SonyEricssonK610iUSB()
