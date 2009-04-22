# -*- coding: utf-8 -*-
# Copyright (C) 2009  Vodafone España, S.A.
# Author:  Andrew Bird
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

from vmc.common.exceptions import DeviceLacksExtractInfo
from vmc.common.hardware.zte import ZTECustomizer, ZTEDBusDevicePlugin

import re

from vmc.common.command import get_cmd_dict_copy, OK_REGEXP, ERROR_REGEXP
from vmc.common.hardware.base import Customizer


ZTE2525_CMD_DICT = get_cmd_dict_copy()

ZTE2525_CMD_DICT['get_netreg_status'] = dict(echo=None,
                end=OK_REGEXP,
                error=ERROR_REGEXP,
                extract=re.compile(r"""
                \r\n
                \+CREG:\s
                (?P<mode>\d),(?P<status>\d+)(,[0-9a-fA-F]*,[0-9a-fA-F]*)?
                \r\n
                """, re.VERBOSE))

ZTE2525_CMD_DICT['get_network_info'] = dict(echo=None,
                end=OK_REGEXP,
                error=ERROR_REGEXP,
                extract=re.compile(r"""
                \r\n
                \+COPS:\s+
                (
                (?P<error>\d) |
                \d,\d,             # or followed by num,num,str ( fixed bearer )
                "(?P<netname>[\w\S ]*)"
                )                  # end of group
                \r\n
                """, re.VERBOSE))

ZTE2525_CMD_DICT['get_sms_by_index'] = dict(echo=None,
                end=OK_REGEXP,
                error=ERROR_REGEXP,
                extract=re.compile(r"""
                \r\n
                \+CMGR:\s
                (?P<storedat>\d),
                (?P<contact>.*),
                \d+\r\n
                (?P<pdu>\w+)
                \r\n""", re.VERBOSE))

ZTE2525_CMD_DICT['get_sms'] = dict(echo=None,
                end=re.compile('(\r\n)?\r\n(OK)\r\n'),
                error=ERROR_REGEXP,
                extract=re.compile(r"""
                \r\n
                \+CMGL:\s
                (?P<id>\d+),
                (?P<storedat>\d),
                (?P<contact>.*),
                \d+\r\n
                (?P<pdu>\w+)
                """, re.VERBOSE))


class ZTE2525Customizer(Customizer):
    async_regexp = None
    conn_dict = {
        'GPRSONLY' : None,
        '3GONLY'   : None,
        'GPRSPREF' : None,
        '3GPREF'   : None,
    }
    cmd_dict = ZTE2525_CMD_DICT


class ZTEK2525(ZTEDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for ZTE's version of Vodafone's K2525"""
    name = "ZTE K2525"
    version = "0.1"
    author = "Andrew Bird"
    custom = ZTE2525Customizer

    __remote_name__ = "K2525"

    __properties__ = {
        'usb_device.vendor_id': [0x19d2],
        'usb_device.product_id': [0x0022],
    }

zte_k2525 = ZTEK2525()

