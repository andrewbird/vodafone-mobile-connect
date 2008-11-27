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
"""Unittests for buffering"""

__version__ = "$Rev: 1172 $"

from twisted.trial import unittest

import vmc.common.notifications as N
from vmc.common.protocol import BufferingStateMachine
from vmc.common.plugin import PluginManager
from stub import SerialPortStub, test_protocol

class TestBuffering(unittest.TestCase):
    """Tests for vmc.common.protocol."""
    
    def setUpClass(self):
        # uncomment me to see whats going on
        huawei = PluginManager.get_plugin_by_name('Huawei E220')
        stub = test_protocol(huawei, SerialPortStub, BufferingStateMachine)
        self.stub = stub

    def test_notifications_at_idle_state(self):
        pattern = [
            (.0, "\r\n^RSSI:27\r\n"),
            (.5, "\r\n^RSSI:26\r\n"),
            (.3, "\r\n^RSSI:12\r\n"),
        ]
        
        expected = [
            N.UnsolicitedNotification(N.SIG_RSSI, 27),
            N.UnsolicitedNotification(N.SIG_RSSI, 26),
            N.UnsolicitedNotification(N.SIG_RSSI, 12),
        ]

        def load_pattern_cb(ignored):
            resp = []
            
            while self.stub.protocol.notifications.pending:
                d = self.stub.protocol.notifications.get()
                d.addCallback(lambda noti: resp.append(noti))
            
            self.assertEqual(expected, resp)

        d = self.stub.load_pattern(pattern)
        d.addCallback(load_pattern_cb)
        return d
        
