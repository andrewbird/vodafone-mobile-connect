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
"""
Common stuff for all ZTE's Icera based cards
"""

import re

from vmc.common.command import get_cmd_dict_copy, OK_REGEXP, ERROR_REGEXP
from vmc.common.hardware.base import Customizer
from vmc.common.sim import SIMBaseClass
from vmc.common.plugin import DBusDevicePlugin

ICERA_DICT = {
   'GPRSONLY': 'AT%IPSYS=0',
   '3GONLY': 'AT%IPSYS=1',
   'GPRSPREF': 'AT%IPSYS=2',
   '3GPREF': 'AT%IPSYS=3',
}

ICERA_CMD_DICT = get_cmd_dict_copy()

# \r\n+CPBR: (1-200),80,14,0,0,0\r\n\r\nOK\r\n'
ICERA_CMD_DICT['get_phonebook_size'] = dict(
    echo=None,
    end=OK_REGEXP,
    error=ERROR_REGEXP,
    extract=re.compile(r"""
        \r\n
        \+CPBR:\s
        \(\d+-(?P<size>\d+)\).*
        \r\n
    """, re.VERBOSE))

# \r\n
# +CMGL: 1,1,"616E64726577",23\r\n0791447758100650040C914497716247010
#             0009011503195310004D436390C\r\n'
# +CMGL: 2,1,"616E64726577",37\r\n0791447758100650040C914497716247010
#             0009011606113730014CA365CDD26B7EFEA705B1DBEABC3E47B9B0C\r\n'
ICERA_CMD_DICT['list_sms'] = dict(
    echo=None,
    end=OK_REGEXP,
    error=ERROR_REGEXP,
    extract=re.compile(r"""
        \r\n
        \+CMGL:\s
        (?P<id>\d+),
        (?P<where>\d),,\d+
        \r\n(?P<pdu>\w+)
    """, re.VERBOSE))

ICERA_CMD_DICT['get_network_mode'] = dict(
    echo=None,
    end=OK_REGEXP,
    error=ERROR_REGEXP,
    extract=re.compile(r"""
        %IPSYS:\s
        (?P<mode>\d+),
        (?P<domain>\d+)
    """, re.VERBOSE))


class IceraSIMClass(SIMBaseClass):
    """
    Icera based ZTE SIM Class
    """

    def __init__(self, sconn):
        super(IceraSIMClass, self).__init__(sconn)

    def initialize(self, set_encoding=True):
        d = super(IceraSIMClass, self).initialize(set_encoding=set_encoding)

        def init_callback(size):
            # Turn on the radio
            self.sconn.send_at('AT+CFUN=1')
            # make sure we are in 3g pref before registration
            self.sconn.send_at(ICERA_DICT['3GPREF'])
            # setup SIM storage defaults
            self.sconn.send_at('AT+CPMS="SM","SM","SM"')
            return size

        d.addCallback(init_callback)
        return d


class IceraDBusDevicePlugin(DBusDevicePlugin):
    """DBusDevicePlugin for Icera based ZTE devices"""
    simklass = IceraSIMClass

    def __init__(self):
        super(IceraDBusDevicePlugin, self).__init__()


class IceraCustomizer(Customizer):
    async_regexp = None
    conn_dict = ICERA_DICT
    cmd_dict = ICERA_CMD_DICT
