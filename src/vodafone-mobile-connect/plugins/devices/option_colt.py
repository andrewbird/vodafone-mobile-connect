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
DevicePlugin for Option Colt

(end of life reached)
"""
__version__ = "$Rev: 1172 $"

from twisted.python import log

from vmc.common.hardware.option import (OptionDBusDevicePlugin,
                                        OptionCustomizer)
from vmc.common.sim import SIMBaseClass
from vmc.common.statem.auth import AuthStateMachine
from vmc.contrib.epsilon.modal import mode
    
class OptionColtAuthStateMachine(AuthStateMachine):
    """
    Custom AuthStateMachine for Option Colt
    
    This device has a rather buggy firmware that yields all sort of
    weird errors. For example, if PIN authentication is disabled on the SIM
    and you issue an AT+CPIN? command, it will reply with a +CPIN: SIM PUK2
    """
    pin_needed_status = AuthStateMachine.pin_needed_status
    puk_needed_status = AuthStateMachine.puk_needed_status
    puk2_needed_status = AuthStateMachine.puk2_needed_status
    
    class get_pin_status(mode):
        """
        Ask the PIN what's the PIN status
            
        The SIM can be in one of the following states:
        - SIM is ready (already authenticated, or PIN disabled)
             - PIN is needed
             - PIN2 is needed (not handled)
             - PUK is needed
             - PUK2 is needed
             - SIM is not inserted
             - SIM's firmware error
        """
        def __enter__(self):
            pass
        def __exit__(self):
            pass
            
        def do_next(self):
            log.msg("Instantiating get_pin_status mode....")
            d = self.device.sconn.get_pin_status()
            d.addCallback(self.get_pin_status_cb)
            d.addErrback(self.sim_failure_eb)
            d.addErrback(self.sim_busy_eb)
            d.addErrback(self.sim_no_present_eb)
            d.addErrback(log.err)


class OptionColtSIMClass(SIMBaseClass):
    """Huawei E220 SIM Class"""
    def __init__(self, sconn):
        super(OptionColtSIMClass, self).__init__(sconn)
    
    def postinit(self):
        self.charset = 'IRA'
        d = super(OptionColtSIMClass, self).postinit(set_encoding=False)
        d.addCallback(lambda size: self.set_size(size))
        return d

class OptionColtCustomizer(OptionCustomizer):
    """L{vmc.common.hardware.Customizer} for Option Colt"""
    authklass = OptionColtAuthStateMachine


class OptionColt(OptionDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Option Colt"""
    name = "Option Colt"
    version = "0.1"
    author = u"Pablo Martí"
    custom = OptionColtCustomizer
    simklass = OptionColtSIMClass
    
    __remote_name__ = "129"
    
    __properties__ = {
        'usb_device.vendor_id' : [0x0af0],
        'usb_device.product_id' : [0x5000],
    }


optioncolt = OptionColt()
