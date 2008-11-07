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
"""Unittests for stub"""

__version__ = "$Rev: 1172 $"

import sys

from twisted.trial import unittest
from twisted.python import log

from stub import DeviceStub

class TestStub(unittest.TestCase):
    """Tests for vmc.test.stub.DeviceStub"""

    def test_pattern_without_repetitions(self):
        pattern = {
            'get_network_info': (21401, "3G"),
            'get_signal_level': 27,
        }
        device = DeviceStub(pattern)
        d = device.sconn.get_network_info()
        d.addCallback(lambda resp: self.assertEqual(resp, (21401, "3G")))
        return d
    
    def test_pattern_with_repetitions(self):
        pattern = {
            'get_network_info': (21401, "3G"),
            'get_network_info2': (21403, "GPRS"),
            'get_network_info3': (21402, "3G"),
        }
        device = DeviceStub(pattern)
        device.sconn.get_network_info().addCallback(
                lambda info: self.assertEqual(info, (21401, "3G")))
        
        device.sconn.get_network_info().addCallback(
                lambda info: self.assertEqual(info, (21403, "GPRS")))
        
        d = device.sconn.get_network_info()
        d.addCallback(lambda info: self.assertEqual(info, (21402, "3G")))
        return d
    
    def test_pattern_noexistent(self):
        pattern = {
            'get_network_info': (21401, "3G"),
        }
        device = DeviceStub(pattern)
        self.assertRaises(AttributeError, device.sconn.get_all_contacts)
