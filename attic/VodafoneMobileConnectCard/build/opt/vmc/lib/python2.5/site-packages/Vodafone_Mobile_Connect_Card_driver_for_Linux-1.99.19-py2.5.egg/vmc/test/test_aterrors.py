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
"""Unittests for the aterrors module"""

__version__ = "$Rev: 1172 $"

from twisted.trial import unittest
import vmc.common.exceptions as ex
from vmc.common.aterrors import extract_error

class TestATErrors(unittest.TestCase):
    """Tests for vmc.common.aterrors"""

    def test_cme_errors(self):
        raw = '\r\n+CME ERROR: SIM interface not started\r\n'
        self.assertEqual(extract_error(raw)[0], ex.CMEErrorSIMNotStarted)
        raw2 = 'AT+CPIN=1330\r\n\r\n+CME ERROR: operation not allowed\r\n'
        self.assertEqual(extract_error(raw2)[0], ex.CMEErrorOperationNotAllowed)
        raw3 = '\r\n+CME ERROR: SIM busy\r\n'
        self.assertEqual(extract_error(raw3)[0], ex.CMEErrorSIMBusy)

    def test_cms_errors(self):
        raw = '\r\n+CMS ERROR: 500\r\n'
        self.assertEqual(extract_error(raw)[0], ex.CMSError500)
        raw2 = '\r\n+CMS ERROR: 301\r\n'
        self.assertEqual(extract_error(raw2)[0], ex.CMSError301)
    
