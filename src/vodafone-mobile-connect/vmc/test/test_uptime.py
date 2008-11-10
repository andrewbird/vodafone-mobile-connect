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
Tests for the uptime module
"""
__version__ = "$Rev: 1172 $"

from twisted.trial import unittest

from vmc.common.uptime import get_time_dict, get_uptime_string

class TestUptime(unittest.TestCase):
    """Tests for uptime module"""
    
    def test_get_time_dict_with_two_minutes(self):
        self.assertEqual(get_time_dict(120), {'minute': 2})

    def test_get_time_dict_with_more_than_a_day(self):
        self.assertEqual(get_time_dict(86460), {'day': 1, 'minute': 1})
    
    def test_get_uptime_string_with_two_minutes(self):
        self.assertEqual(get_uptime_string(120), "0:02")

    def test_get_uptime_string_with_more_than_a_day(self):
        self.assertEqual(get_uptime_string(86460), "1 day, 0:01")
        
