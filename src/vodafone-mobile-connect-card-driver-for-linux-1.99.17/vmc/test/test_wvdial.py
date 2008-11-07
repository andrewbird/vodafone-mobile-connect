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
tests for the wvdial dialer
"""
__version__ = "$Rev: 1172 $"

import os
import shutil

from twisted.trial import unittest

from vmc.common.dialers.wvdial import (get_wvdial_conf_file,
                                       append_entry_to_secrets)
from vmc.common.dialer import DialerConf
from vmc.utils.utilities import get_file_data, touch

class TestWvdialDialer(unittest.TestCase):
    
    def test_append_entry_to_secrets(self):
        pap_path = '/tmp/pap-secrets'
        chap_path = '/tmp/chap-secrets'
        touch(pap_path)
        touch(chap_path)
        
        append_entry_to_secrets('vodafone', 'vodafone', pap_path, chap_path)
        pap_data = get_file_data(pap_path)
        chap_data = get_file_data(chap_path)
        
        self.assertEqual(pap_data, '"vodafone"\t*\t"vodafone"\n')
        self.assertEqual(pap_data, chap_data)
        
        os.unlink(pap_path)
        os.unlink(chap_path)
    
    def test_get_wvdial_conf_file(self):
        conf = dict(apn='ac.vodafone.es',
                    username='vodafone',
                    password='vodafone',
                    dialer_profile='default',
                    staticdns=False,
                    dns=None)
        expected = \
"""# wvdial template for VMC

[Dialer Defaults]

Phone = *99***1#
Username = vodafone
Password = vodafone
Stupid Mode = 1
Dial Command = ATDT
Check Def Route = on
Dial Attempts = 3

[Dialer connect]

Modem = /dev/ttyUSB0
Baud = 460800
Init2 = ATZ
Init3 = ATQ0 V1 E0 S0=0 &C1 &D2 +FCLASS=0
Init4 = AT+CGDCONT=1,"IP","ac.vodafone.es"
ISDN = 0
Modem Type = Analog Modem
"""
        
        dialerconf = DialerConf.from_config_dict(conf)
        path = get_wvdial_conf_file(dialerconf, '/dev/ttyUSB0')
        data = get_file_data(path)
        self.assertEqual(data, expected)
        
        shutil.rmtree(os.path.dirname(path))
    