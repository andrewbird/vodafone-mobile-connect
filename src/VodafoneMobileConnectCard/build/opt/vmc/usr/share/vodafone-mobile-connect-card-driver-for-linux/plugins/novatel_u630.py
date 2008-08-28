# -*- coding: utf-8 -*-
# Copyright (C) 2006-2008  Vodafone España, S.A.
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

__version__ = "$Rev: 1203 $"

from vmc.common.plugin import DBusDevicePlugin
from vmc.common.exceptions import DeviceLacksExtractInfo

from vmc.common.hardware.novatel import NovatelCustomizer

class NovatelU630(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Novatel's U630"""
    name = "Novatel U630"
    version = "0.1"
    author = u"Pablo Martí"
    custom = NovatelCustomizer

    __properties__ = {
        'pcmcia.manf_id': [0xa4],
        'pcmcia.card_id': [0x276],
    }
    
    def extract_info(self, children):
        # U630 sports just one serial port
        for device in children:
            try:
                self.dport = device['serial.device'].encode('utf8')
            except KeyError:
                pass
        
        if not self.dport:
            raise DeviceLacksExtractInfo(self)

novatelu630 = NovatelU630()
