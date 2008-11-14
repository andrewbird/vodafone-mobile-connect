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
"""Unittests for the csv module"""

__version__ = "$Rev: 1172 $"

import os
from cStringIO import StringIO
from vmc.common.csvutils import CSVUnicodeWriter, CSVUnicodeReader
from twisted.trial import unittest

TMPFILE = 'test.csv'

CSVDATA = 'John,"+3532344333"\nPeter,"+345465454"\nLucy,"+4464576556"\n'

class TestCSVUtils(unittest.TestCase):
    """Test for csvutils functionality"""

    def test_get_rows(self):
        fobj = StringIO(CSVDATA)
        reader = CSVUnicodeReader(fobj)
        resp = reader.get_rows()
        self.assertEqual(resp, [[u'John', u'+3532344333'],
                                [u'Peter', u'+345465454'],
                                [u'Lucy', u'+4464576556']])
        fobj.close()
    
    def test_write_row(self):
        writer = CSVUnicodeWriter(open(TMPFILE, 'w'))
        row = [u'Pabl\0231', u'+345667781']
        writer.write_row(row)
        
        reader = CSVUnicodeReader(open(TMPFILE))
        resp = reader.get_rows()
        self.assertEqual(resp, [row])
        os.unlink(TMPFILE)
    
    def test_write_rows(self):
        writer = CSVUnicodeWriter(open(TMPFILE, 'w'))
        rows = [[u'Pablo', u'+345667781'],
                [u'Xabïé', u'+347327211'],
                [u'Raúls', u'+349494949'],
                [u'María', u'+312232111'],
                [u'André', u'+378544522']]
        
        writer.write_rows(rows)
        
        reader = CSVUnicodeReader(open(TMPFILE))
        resp = reader.get_rows()
        self.assertEqual(resp, rows)
        os.unlink(TMPFILE)
        
