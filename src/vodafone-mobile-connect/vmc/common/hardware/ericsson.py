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
Common stuff for all Ericsson's cards
"""

__version__ = "$Rev: 1190 $"

import re

from vmc.common.hardware.base import Customizer
from vmc.common.netspeed import bps_to_human
from vmc.common.middleware import SIMCardConnAdapter
import vmc.common.notifications as notifications
from vmc.common.sim import SIMBaseClass

from vmc.common.plugin import DBusDevicePlugin

from vmc.common.encoding import pack_ucs2_bytes

from vmc.common.command import get_cmd_dict_copy, OK_REGEXP, ERROR_REGEXP
from twisted.python import log
from vmc.common.command import ATCmd

ERICSSON_DICT = {
   'GPRSONLY' : 'AT+CFUN=5',
   '3GONLY'   : 'AT+CFUN=6',
   'GPRSPREF' : None,
   '3GPREF'   : 'AT+CFUN=1',
}

class EricssonSIMClass(SIMBaseClass):
    """
    Ericsson SIM Class
    """
    def __init__(self, sconn):
        super(EricssonSIMClass, self).__init__(sconn)

    def initialize(self, set_encoding=True):

        self.sconn.reset_settings()
        self.sconn.disable_echo()
        self.sconn.send_at('AT+CFUN=1') # Turn on the radio

        d = super(EricssonSIMClass, self).initialize(set_encoding=set_encoding)
        def init_callback(size):
            # setup SIM storage defaults
            self.sconn.send_at('AT+CPMS="SM","SM","SM"')
            return size

        d.addCallback(init_callback)
        return d

class EricssonDBusDevicePlugin(DBusDevicePlugin):
    """DBusDevicePlugin for Ericsson"""
    simklass = EricssonSIMClass

    def __init__(self):
        super(EricssonDBusDevicePlugin, self).__init__()


class EricssonAdapter(SIMCardConnAdapter):
    """
    Adapter for all Ericsson cards
    """
    def __init__(self, device):
        log.msg("called EricssonAdapter::__init__")
        super(EricssonAdapter, self).__init__(device)

    def reset_settings(self):
        """
        Resets the settings to factory settings

        @rtype: C{Deferred}
        """
        cmd = ATCmd('AT&F', name='reset_settings')
        return self.queue_at_cmd(cmd)

    def get_signal_level(self):
        """
        On Ericsson, AT+CSQ only returns valid data in GPRS mode

        So we need to override and provide an alternative. +CIND
        returns an indication between 0-5 so let's just multiply
        that by 5 to get a very rough rssi

        @rtype: C{Deferred}
        """

        cmd = ATCmd('AT+CIND?',name='get_signal_indication')
        d = self.queue_at_cmd(cmd)
        d.addCallback(lambda response: int(response[0].group('sig'))*5)
        return d

    def set_charset(self, charset):
        """
        Sets the character set used on the SIM

        The oddity here is that the set command needs to have its charset value
        encoded in the current character set
        """
        if (self.device.sim.charset == 'UCS2'):
            charset = pack_ucs2_bytes(charset)

        d = super(EricssonAdapter, self).set_charset(charset)
        return d

    def get_pin_status(self):
        """
        Returns 1 if PIN auth is active and 0 if its not
        
        @rtype: C{Deferred}
        """
        def ericsson_get_pin_status(facility):
            """
            Checks whether the pin is enabled or disabled
            """
            cmd = ATCmd('AT+CLCK="%s",2' % facility, name='get_pin_status')
            return self.queue_at_cmd(cmd)

        def pinreq_errback(failure):
            failure.trap(ex.CMEErrorSIMPINRequired)
            return 1
        
        def aterror_eb(failure):
            failure.trap(ex.ATError)
            # return the failure or wont work
            return failure
        
        facility = (self.device.sim.charset == 'UCS2') and pack_ucs2_bytes('SC') or 'SC'

        d = ericsson_get_pin_status(facility)                    # call the local one
        d.addCallback(lambda response: int(response[0].group('status')))
        d.addErrback(pinreq_errback)
        d.addErrback(aterror_eb)
        return d
 

class EricssonCustomizer(Customizer):
    """
    Base Customizer class for Ericsson cards
    """

    adapter = EricssonAdapter

    # Multiline so we catch and remove the ESTKSMENU
#    async_regexp = re.compile(r"""\r\n(?P<signal>\*[A-Z]{3,}):(?P<args>.*)\r\n""",
#                        re.MULTILINE)

    ignore_regexp = [ re.compile(r"""\r\n(?P<ignore>\*ESTKSMENU:.*)\r\n""", re.MULTILINE|re.DOTALL),
                      re.compile(r"""\r\n(?P<ignore>\*EMWI.*)\r\n"""),
                      re.compile(r"""\r\n(?P<ignore>\+PACSP0.*)\r\n"""),
                    ]

    conn_dict = ERICSSON_DICT

    cmd_dict = get_cmd_dict_copy()

    cmd_dict['get_card_model'] = dict(echo=None,
                    end=OK_REGEXP,
                    error=ERROR_REGEXP,
                    extract=re.compile('\s*(?P<model>\S*)\r\n'))

    cmd_dict['get_signal_indication'] = dict(echo=None,
                    end=OK_REGEXP,
                    error=ERROR_REGEXP,
                    extract=re.compile('\s*\+CIND:\s+[0-9]*,(?P<sig>[0-9]*),.*')) # +CIND: 5,5,0,0,1,0,1,0,1,1,0,0

    cmd_dict['get_network_info'] = dict(echo=None,
                 end=OK_REGEXP,
                 error=ERROR_REGEXP,
                 extract=re.compile(r"""
                          \r\n
                          \+COPS:\s+
                          (
                          (?P<error>\d) |
                          \d,\d,             # or followed by num,num,str,num
                          "(?P<netname>[\w\S ]*)",
                          (?P<status>\d)
                          )                  # end of group
                          \s*
                          \r\n
                          """, re.VERBOSE))


