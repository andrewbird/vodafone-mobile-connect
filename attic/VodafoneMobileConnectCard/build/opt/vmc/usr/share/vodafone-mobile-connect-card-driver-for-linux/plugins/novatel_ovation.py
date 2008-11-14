# -*- coding: utf-8 -*-
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

__version__ = "$Rev: 1093 $"

from twisted.python import log

import vmc.common.exceptions as ex
from vmc.common.plugin import DBusDevicePlugin
from vmc.common.exceptions import DeviceLacksExtractInfo
from vmc.common.hardware.novatel import NovatelCustomizer
from vmc.common.statem.networkreg import NetworkRegStateMachine

from vmc.contrib.epsilon.modal import mode


class OvationNetworkRegStateMachine(NetworkRegStateMachine):
    """
    NetworkRegStateMachine for NovatelWireless' Ovation
    
    The Ovation doesn't seems to report via +CREG its network registration
    status, so the vanilla NetworkRegStateMachine wont work. Instead we
    shortcut the process and move directly to obtain_netinfo
    """
    wait_to_register = NetworkRegStateMachine.wait_to_register
    obtain_netinfo = NetworkRegStateMachine.obtain_netinfo
    search_operators = NetworkRegStateMachine.search_operators
    international_roaming = NetworkRegStateMachine.international_roaming
    register_with_operator = NetworkRegStateMachine.register_with_operator
    registration_finished = NetworkRegStateMachine.registration_finished
    registration_failed = NetworkRegStateMachine.registration_failed
    
    class check_registered(mode):
        def __enter__(self):
            pass
        def __exit__(self):
            pass
        
        def do_next(self):
            log.msg("%s: NEW MODE: check_registered" % self)
            self.device.sconn.set_charset("IRA")
            self.device.sconn.set_network_info_format() # set it to numeric
            
            def get_netinfo_cb(netinfo):
                # Novatel Ovation doesn't reports +CREG notifications so we
                # have to modify its netreg process, we will query directly
                # the network is registered with
                log.msg("%s: NEW MODE: obtain_netinfo" % self)
                d = self.device.sconn.get_imsi()
                d.addCallback(lambda response: int(response[:5]))
                d.addCallback(self._process_imsi_cb)
            
            def get_netinfo_eb(failure):
                failure.trap(ex.NetworkTemporalyUnavailableError)
                d = self.device.sconn.get_netreg_status()
                d.addCallback(self._process_netreg_status)
                d.addErrback(log.err)
            
            d = self.device.sconn.get_network_info(process=False)
            d.addCallback(get_netinfo_cb)
            d.addErrback(get_netinfo_eb)

class NovatelOvationCustomizer(NovatelCustomizer):
    netrklass = OvationNetworkRegStateMachine


class NovatelOvation(DBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Novatel's Ovation"""
    name = "Novatel MC950D"
    version = "0.1"
    author = u"Pablo Martí"
    custom = NovatelOvationCustomizer

    __remote_name__ = "Ovation MC950D Card"

    __properties__ = {
        'usb_device.vendor_id' : [0x1410],
        'usb_device.product_id' : [0x4400],
    }

    def extract_info(self, children):
        # Ovation uses ttyUSB0 and ttyUSB1
        for device in children:
            try:
                if device['serial.port'] == 0: #data port
                    self.dport = device['serial.device'].encode('utf8')
            except KeyError:
                pass
        
        if not self.dport:
            raise DeviceLacksExtractInfo(self)

novatelovation = NovatelOvation()
