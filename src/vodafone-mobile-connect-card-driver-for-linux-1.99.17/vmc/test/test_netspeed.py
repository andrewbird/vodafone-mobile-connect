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
"""Unittests for vmc.common.netspeed"""

__version__ = "$Rev: 1172 $"

from twisted.trial import unittest

from vmc.common.netspeed import get_signal_level_from_rssi, bps_to_human

class TestNetSpeed(unittest.TestCase):
    """Tests for vmc.common.netspeed"""
    
    def test_bps_to_human(self):
        self.assertEqual(bps_to_human(1001, 1000), ('1.00 Kbps', '1.00 Kbps'))
        self.assertEqual(bps_to_human(1000001, 1000001), ('1.00 Mbps', '1.00 Mbps'))
        self.assertEqual(bps_to_human(100, 100), ('100.00 bps', '100.00 bps'))
    
    def test_get_signal_level_from_rssi(self):
        self.assertEqual(get_signal_level_from_rssi(31), 100)
        self.assertEqual(get_signal_level_from_rssi(23), 75)
        self.assertEqual(get_signal_level_from_rssi(18), 50)
        self.assertEqual(get_signal_level_from_rssi(12), 25)
        self.assertEqual(get_signal_level_from_rssi(99), 0)
        self.assertEqual(get_signal_level_from_rssi(1), 0)
    