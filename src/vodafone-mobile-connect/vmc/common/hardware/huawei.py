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
"""
Common stuff for all Huawei's cards
"""

__version__ = "$Rev: 1190 $"

import re

from vmc.common.hardware.base import Customizer
from vmc.common.netspeed import bps_to_human
from vmc.common.middleware import SIMCardConnAdapter
import vmc.common.notifications as notifications
from vmc.common.sim import SIMBaseClass

from vmc.common.command import get_cmd_dict_copy, OK_REGEXP, ERROR_REGEXP
from twisted.python import log
from vmc.common.command import ATCmd

HUAWEI_DICT = {
   'GPRSONLY' : 'AT^SYSCFG=13,1,3FFFFFFF,2,4',
   '3GONLY'   : 'AT^SYSCFG=14,2,3FFFFFFF,2,4',
   'GPRSPREF' : 'AT^SYSCFG=2,1,3FFFFFFF,2,4',
   '3GPREF'   : 'AT^SYSCFG=2,2,3FFFFFFF,2,4',
}

def huawei_new_conn_mode(args):
    """Translates C{arg} to VMC's language"""
    mode_args_dict = {
        '0,0' : notifications.NO_SIGNAL,
        '3,2' : notifications.GPRS_SIGNAL,
        '3,3' : notifications.GPRS_SIGNAL,
        '5,4' : notifications.UMTS_SIGNAL,
        '5,5' : notifications.HSDPA_SIGNAL,
        '5,6' : notifications.HSUPA_SIGNAL,
        '5,7' : notifications.HSPA_SIGNAL, # doc says HSDPA + HSUPA ain't that
                                           # just HSPA?
    }
    return mode_args_dict[args]

def huawei_radio_switch(args):
    state_args_dict = {
        '0,0' : notifications.RADIO_OFF,
        '0,1' : notifications.RADIO_OFF,
        '1,0' : notifications.RADIO_OFF,
        '1,1' : notifications.RADIO_ON,
    }
    return state_args_dict[args]

def huawei_new_speed_link(args):
    converted_args = map(lambda hexstr: int(hexstr, 16), args.split(','))
    time, tx, rx, tx_flow, rx_flow, tx_rate, rx_rate = converted_args
    return bps_to_human(tx * 8, rx * 8)


class HuaweiCustomizer(Customizer):
    """
    Base Customizer class for Huawei cards
    """
    async_regexp = re.compile('\r\n(?P<signal>\^[A-Z]{3,9}):(?P<args>.*)\r\n')
    conn_dict = HUAWEI_DICT
    device_capabilities = [notifications.SIG_NEW_CONN_MODE,
                           notifications.SIG_RSSI,
                           notifications.SIG_SPEED,
                           notifications.SIG_RFSWITCH]

    cmd_dict = get_cmd_dict_copy()

    cmd_dict['get_card_model'] = dict(echo=None,
                    end=OK_REGEXP,
                    error=ERROR_REGEXP,
                    extract=re.compile('\s*(?P<model>\S*)\r\n'))

    cmd_dict['get_radio'] = dict(echo=None,
                    end=OK_REGEXP,
                    error=ERROR_REGEXP,
                    extract=re.compile('\s*\^RFSWITCH:(?P<switch>\S*)\r\n'))
    
    signal_translations = {
        '^MODE' : (notifications.SIG_NEW_CONN_MODE, huawei_new_conn_mode),
        '^RSSI' : (notifications.SIG_RSSI, lambda i: int(i)),
        '^DSFLOWRPT' : (notifications.SIG_SPEED, huawei_new_speed_link),
        '^RFSWITCH' : (notifications.SIG_RFSWITCH, huawei_radio_switch),
    }

class HuaweiE2XXAdapter(SIMCardConnAdapter):
    """
    Adapter for all Huawei E2XX cards
    """
    def __init__(self, device):
        super(HuaweiE2XXAdapter, self).__init__(device)
    
    def set_smsc(self, smsc):
        """
        Sets the SIM's smsc to C{smsc}
        
        We wrap the operation with set_charset('IRA') and set_charset('UCS2')
        """
        # XXX: The return value of this method is actually the return value
        # of the set_charset("UCS2") operation
        d = self.set_charset('IRA')
        d.addCallback(lambda _: super(HuaweiE2XXAdapter, self).set_smsc(smsc))
        d.addCallback(lambda _: self.set_charset('UCS2'))
        return d

class HuaweiE2XXCustomizer(HuaweiCustomizer):
    """
    Customizer for all Huawei E2XX cards
    """
    adapter = HuaweiE2XXAdapter

##############################################
# Modules have RFSWITCH
    
class HuaweiEMXXAdapter(HuaweiE2XXAdapter):
    """
    Adapter for all Huawei E2XX cards
    """
    def __init__(self, device):
        super(HuaweiEMXXAdapter, self).__init__(device)
    
    def get_signal_level(self):
        """
        Returns the signal level
            @rtype: C{Deferred}
            Overloaded to poll the RFSWITCH status
        """

        cmd = ATCmd('AT^RFSWITCH?',name='get_radio')
        d = self.queue_at_cmd(cmd)
        d.addCallback(lambda _: super(HuaweiEMXXAdapter, self).get_signal_level())
        return d

class HuaweiEMXXCustomizer(HuaweiCustomizer):
    """
    Customizer for all Huawei E2XX cards
    """
    adapter = HuaweiEMXXAdapter

