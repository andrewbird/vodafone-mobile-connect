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
"""Unittests for the encoding module"""

__version__ = "$Rev: 1172 $"

from twisted.trial import unittest

from vmc.common.encoding import (pack_7bit_bytes, pack_8bit_bytes,
                                 pack_ucs2_bytes, unpack_ucs2_bytes,
                                 check_if_ucs2)

class TestEncoding(unittest.TestCase):
    """Test for csvutils functionality"""
    
    def test_check_if_ucs2(self):
        self.assertEqual(check_if_ucs2('00'), False)
        self.assertEqual(check_if_ucs2('mañico'), False)
        self.assertEqual(check_if_ucs2('0056006F006400610066006F006E0065'),
                         True)
        self.assertEqual(check_if_ucs2('1234'), False)
    
    def test_pack_7bit_bytes(self):
        # 07911356131313F311000A9260214365870000AA04E8373B0C
        self.assertEqual(pack_7bit_bytes('hola'), 'E8373B0C')
    
    def test_pack_8bit_bytes(self):
        # 07911356131313F311000A9260214365870004AA04686F6C61
        self.assertEqual(pack_8bit_bytes('hola'), '686F6C61')
        # from Nokia's Smart Messaging FAQ
        expected_resp = '424547494E3A5643415244'
        self.assertEqual(pack_8bit_bytes('BEGIN:VCARD'), expected_resp)
    
    def test_pack_ucs2_bytes(self):
        # 07911356131313F311000A9260214365870008AA080068006F006C0061
        self.assertEqual(pack_ucs2_bytes('hola'), '0068006F006C0061')
        # 07911356131313F311000A9260214365870008AA0A0068006F006C00610073
        self.assertEqual(pack_ucs2_bytes('holas'), '0068006F006C00610073')
    
    def test_unpack_ucs2_bytes(self):
        self.assertEqual(unpack_ucs2_bytes('0068006F006C0061'), 'hola')
        resp = 'holas'
        self.assertEqual(unpack_ucs2_bytes('0068006F006C00610073'), resp)
    
    
