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
tests for the utilities module
"""
__version__ = "$Rev: 1172 $"

import os

from twisted.trial import unittest

from vmc.utils.utilities import (get_file_data, save_file,
                                 generate_vmc_dns_lock)

class TestUtilities(unittest.TestCase):
    
    def test_get_file_data(self):
        text = os.urandom(2000)
        path = '/tmp/file.foo'
        fobj = open(path, 'w')
        fobj.write(text)
        fobj.close()
        
        self.assertEqual(text, get_file_data(path))
        os.unlink(path)
    
    def test_save_file(self):
        text = os.urandom(2000)
        path = '/tmp/file.foo'
        
        save_file(path, text)
        
        fobj = open(path, 'r')
        data = fobj.read()
        fobj.close()
        
        self.assertEqual(text, data)
        os.unlink(path)
    
    def test_generate_vmc_dns_lock(self):
        dns1 = '212.33.21.1'
        dns2 = '212.33.21.2'
        
        path = '/tmp/test-vmc.lock'
        expected = 'DNS1=212.33.21.1\nDNS2=212.33.21.2\n'
        
        generate_vmc_dns_lock(dns1, dns2, path)
        self.assertEqual(get_file_data(path), expected)
        
        os.unlink(path)
    
