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
Base classes for the hardware module
"""
__version__ = "$Rev: 1172 $"

from serial.serialutil import SerialException

from twisted.internet import defer, reactor, serialport
from twisted.python import log

from vmc.common.command import get_cmd_dict_copy
from vmc.common.middleware import SIMCardConnAdapter
from vmc.common.statem.auth import AuthStateMachine
from vmc.common.statem.connection import ConnectStateMachine
from vmc.common.statem.networkreg import NetworkRegStateMachine

class Customizer(object):
    """
    I contain all the custom classes and metadata that a device needs
    
    @cvar adapter: Adapter for the device
    @type adapter: L{SIMCardConnAdapter} child.
    @cvar async_regexp: regexp to parse asynchronous notifications emited
    by the device.
    @cvar conn_dict: Dictionary with the AT strings necessary to change
    between the different connection modes
    @cvar cmd_dict: Dictionary with commands info
    @cvar device_capabilities: List with the unsolicited notifications that
    this device supports
    @cvar authklass: Class that will handle the authentication for this device
    @cvar connklass: Class that will handle the connection for this device
    @cvar netrklass: Class that will handle the network registration for this
    device
    """
    adapter = SIMCardConnAdapter
    async_regexp = None
    conn_dict = {}
    cmd_dict = get_cmd_dict_copy()
    device_capabilities = []
    signal_translations = {}
    authklass = AuthStateMachine
    connklass = ConnectStateMachine
    netrklass = NetworkRegStateMachine


class DeviceResolver(object):
    """
    I identify unkown devices attached to the serial port
    """
    def __init__(self):
        super(DeviceResolver, self).__init__()
    
    @classmethod
    def identify_device(cls, dev):
        sconn = SIMCardConnAdapter(dev)
        try:
            dport, speed = dev.dport, dev.baudrate
            _sp = serialport.SerialPort(sconn, dport, reactor, baudrate=speed)
        except SerialException, e:
            return defer.fail(e)
        
        deferred = defer.Deferred()
        def get_model_no():
            def get_model_cb(name):
                _sp.loseConnection('Bye bye!')
                deferred.callback(name)
            
            d = sconn.get_card_model()
            d.addCallback(get_model_cb)
            d.addErrback(log.err)
        
        reactor.callLater(1, get_model_no)
        return deferred
