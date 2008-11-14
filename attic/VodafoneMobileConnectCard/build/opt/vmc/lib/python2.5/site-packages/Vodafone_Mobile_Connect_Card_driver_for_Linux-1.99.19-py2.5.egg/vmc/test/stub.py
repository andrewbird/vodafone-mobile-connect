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
"""SerialPort stub"""

__version__ = "$Rev: 1172 $"

import time

from twisted.internet import reactor, defer

from vmc.common.protocol import SIMCardConnection

def test_protocol(device, stubklass, foo=None):
    if not foo:
        sconn = SIMCardConnection(device)
    else:
        sconn = foo(device)
    
    stub = stubklass(sconn)
    return stub

class SerialPortStub(object):
    def __init__(self, protocol):
        self.protocol = protocol
        self.pattern = None
        self.state = 'stop'

    def _iteration(self, d):
        try:
            how_much, what = self.pattern.next()
        except StopIteration, e:
            # give .1 seconds extra to finish everything
            reactor.callLater(.1, d.callback, True)
            return
        
        time.sleep(how_much)
        reactor.callLater(.0, self.protocol.dataReceived, what)
        self._iteration(d)

    def load_pattern(self, pattern):
        """
        Returns a Deferred call backed when pattern exhausts
        """
        # make it an iter
        self.pattern = iter(pattern)
        d = defer.Deferred()
        reactor.callLater(0.0, self._iteration, d)
        return d


class DeferredSuccess:
    """
    I'm a fake Deferred result
    """
    def __init__(self, expresp):
        self.expresp = expresp
        
    def __call__(self, *args, **kwds):
        return defer.succeed(self.expresp)

class DeferredFailure:
    """
    I'm a fake Deferred failure
    """
    def __init__(self, what):
        self.what = what
        
    def __call__(self, *args, **kwds):
        raise self.what


class DeferredNotification:
    """
    I am an action that will result in a notification after some delay
    """
    def __init__(self, immediate_response, notification, delay=1):
        self.immediate_response = immediate_response
        self.notification = notification
        self.delay = delay


class SconnStub(object):
    """
    
    """
    def __init__(self, patterns):
        self.responses = patterns
        self.fulfilled = []
        self.sm = None
    
    def __getattr__(self, name):
        if name in self.fulfilled:
            for i in map(str, range(2, 10)):
                method_name = name + i
                if method_name in self.responses:
                    return self.success_wrapper(method_name)
            
        if name in self.responses:
            return self.success_wrapper(name)
        
        msg = "Method %s not in %s"
        return DeferredFailure(AttributeError(msg % (name, self)))
    
    def success_wrapper(self, name):
        resp = self.responses.pop(name)
        self.fulfilled.append(name)
        if isinstance(resp, DeferredNotification):
            assert self.sm != None, "No associated state machine"
            reactor.callLater(resp.delay, self.sm.on_notification_received,
                              resp.notification)
            return DeferredSuccess(resp.immediate_response)
        
        return DeferredSuccess(resp)
        

class DeviceStub(object):
    def __init__(self, patterns):
        self.sconn = SconnStub(patterns)
    
    def set_sm(self, sm):
        self.sconn.sm = sm
        