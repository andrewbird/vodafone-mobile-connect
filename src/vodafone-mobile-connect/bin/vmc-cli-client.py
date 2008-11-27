#!/usr/bin/env python
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
CLI client for VMCCdfL
"""

__version__ = "$Rev: 1109 $"

import sys

from twisted.python import usage, log
from twisted.internet import glib2reactor
glib2reactor.install()

from twisted.internet import reactor

from vmc.common.startup import create_skeleton_and_do_initial_setup

# it will just return if its not necessary
create_skeleton_and_do_initial_setup()

import vmc.common.exceptions as ex
from vmc.common.dialer import DialerConf
from vmc.common.hardware import hw_reg

class Options(usage.Options):
    optFlags = [
        ["connect", "c", "Connect to Internet"],
        ["staticdns", "s", "Use static DNS?"],
    ]
    optParameters = [
        ["apn", "a", "ac.vodafone.es", "The APN host we're connecting to"],
        ["password", "p", "vodafone", "Password to use with wvdial"],
        ["pin", "n", None, "The SIM's PIN"],
        ["username", "u", "vodafone", "Username to use with wvdial"],
        ["dns", "d", None, "DNS"],
        ["dialer_profile", "i", 'default', "Dialer profile to use"],
    ]


def start_cli_client():
    config = Options()
    try:
        config.parseOptions()
    except usage.UsageError, e:
        log.msg('%s: %s' % (sys.argv[0], e))
        log.msg('%s: Try --help for usage details.' % (sys.argv[0]))
        reactor.stop()
    
    def get_devices_cb(devices):
        device = devices[0]
        cli = VMCClient(device, config)
        cli.start_it()
    
    def device_not_found_eb(failure):
        failure.trap(ex.DeviceNotFoundError)
        log.msg("I couldn't find a device to use through DBus")
        reactor.stop()
    
    def device_lacks_extractinfo_eb(failure):
        failure.trap(ex.DeviceLacksExtractInfo)
        log.msg("Your card has been properly recognized but I couldn't infer")
        log.msg("from DBus what ports should use to communicate with device")
        reactor.stop()
    
    d = hw_reg.get_devices()
    d.addCallback(get_devices_cb)
    d.addErrback(device_not_found_eb)
    d.addErrback(device_lacks_extractinfo_eb)


class VMCClient(object):
    def __init__(self, device, config):
        self.device = device
        self.config = config
        self.wrapper = None
        self.connsm = None
    
    def start_it(self):
        if self.config['connect']:
            statemachine_callbacks = {
                'ImDoneEnter' : self.connect_to_internet,
            }
        else:
            # we just wanna run standalone ok?
            statemachine_callbacks = {}
        
        statemachine_errbacks = {
            'AlreadyConnecting' : None,
            'AlreadyConnected' : None,
            'IllegalOperationError' : None,
        }
        
        from vmc.cli.wrapper import CLIWrapper
        self.wrapper = CLIWrapper(self.device, {},
                                   statemachine_callbacks,
                                   statemachine_errbacks)
        # we pass the config so CLICollaborator can send PIN if needed
        self.wrapper.start_behaviour(self.config)
    
    def connect_to_internet(self):
        reactor.callLater(1, self.__connect_to_internet)

    def __connect_to_internet(self):
        self.connsm = self.wrapper.behaviour.current_sm
        # generate the configuration
        dialconf = DialerConf.from_config_dict(self.config)
        # configure dialer
        self.connsm.dialer.configure(dialconf, self.wrapper.device)
        # connect to Internet
        d = self.connsm.connect()
        
        def connect_eb(failure):
            log.err(failure)
            reactor.stop()
        
        d.addCallback(lambda _: log.msg("Connected to Internet!"))
        d.addErrback(connect_eb)


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    reactor.callWhenRunning(start_cli_client)
    reactor.run()
    
