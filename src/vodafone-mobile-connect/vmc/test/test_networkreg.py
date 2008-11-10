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

from vmc.common.middleware import BasicNetworkOperator
from vmc.common.statem.networkreg import NetworkRegStateMachine
from vmc.common.notifications import NetworkRegNotification
from stub import DeviceStub, DeferredNotification

class TestNetworkRegistrationSM(unittest.TestCase):
    """Tests for vmc.test.stub.DeviceStub"""
    def setUpClass(self):
        import sys
        # uncomment me to see whats going on
        #log.startLogging(sys.stdout)

    def test_already_connected(self):
        """
        Test when we are already connected to our operator
        """
        pattern = {
            'get_imsi' : '21401122121212',
            'get_netreg_status' : (0, 1),
            'get_network_info' : (21401, "3G"),
            'set_charset' : 'OK',
            'set_charset2' : 'OK',
            'set_network_info_format' : 'OK',
        }
        
        device = DeviceStub(pattern)
        sm = NetworkRegStateMachine(device)
        d = sm.start_netreg()
        d.addCallback(lambda resp: self.assertEqual(resp, (21401, "3G")))
        return d
    
    def test_sim_insists_on_replying_in_alphanumeric_format(self):
        """
        Test when the SIM insists on replying in alphanumeric format
        
        Affected devices: Option Nozomi.
        """
        pattern = {
            'get_imsi' : '21401122121212',
            'get_imsi2' : '21401122121212',
            'get_netreg_status' : (0, 1),
            'get_network_info' : ("Vodafone ES", "3G"),
            'set_network_info_format': 'OK',
            'set_charset' : 'OK',
            'set_charset2' : 'OK',
            'set_network_info_format' : 'OK',
            # register with network succeeds
            'register_with_network' : 'OK',
        }
        
        device = DeviceStub(pattern)
        sm = NetworkRegStateMachine(device)
        d = sm.start_netreg()
        d.addCallback(lambda resp: self.assertEqual(resp, ("Vodafone ES", "3G")))
        return d
    
    def test_not_registered_and_not_searching(self):
        """
        Test when we are not registered and the SIM doesn't tries to register
        """
        pattern = {
            # our IMSI is a vodafone one
            'get_imsi' : '21401122121212',
            # first time we're connected it will return we're connected to
            # Amena
            'get_network_info' : (21403, "3G"),
            # second time we're connected it will say we're connected to
            # vodafone
            'get_network_info2' : (21401, "3G"),
            'get_netreg_status' : DeferredNotification(
                                                    (0, 0),
                                                    NetworkRegNotification(1),
                                                    delay=1),
            'set_netreg_notification' : 'OK',
            'set_charset' : 'OK',
            'set_charset2' : 'OK',
            'set_network_info_format' : 'OK',
            # Vodafone, Amena and Telefónica are around
            'get_network_names' : [BasicNetworkOperator(21403),
                                   BasicNetworkOperator(21401),
                                   BasicNetworkOperator(21407)],
            # register with network succeeds
            'register_with_network' : 'OK',
        }
        
        device = DeviceStub(pattern)
        sm = NetworkRegStateMachine(device)
        device.set_sm(sm)
        d = sm.start_netreg()
        d.addCallback(lambda resp: self.assertEqual(resp, (21401, "3G")))
        return d
    
    def test_connected_to_other_operator_abroad(self):
        """
        Test when we are connected to other operator abroad and our operator
        list is available
        """
        raise unittest.SkipTest("Not Ready")
        pattern = {
            # our IMSI is a vodafone one
            'get_imsi' : '21401122121212',
            # first time we're connected it will return we're connected to
            # TIM BRAZIL
            'get_network_info' : (72403, "GPRS"),
            'get_netreg_status' : (0, 0),
            # second time we're connected it will say we're connected to
            # Claro
            'get_network_info2' : (72405, "GPRS"),
            'set_charset' : 'OK',
            'set_charset2' : 'OK',
            'set_network_info_format' : 'OK',
            'set_netreg_notification' : 'OK',
            # TIM Brazil and Claro are around
            'get_network_names' : [BasicNetworkOperator(72403),
                                   BasicNetworkOperator(72405)],
            # AT+CPOL response, we've got agreements with Claro Brazil
            # and some other networks
            'get_roaming_ids' : [BasicNetworkOperator(12367),
                                 BasicNetworkOperator(33412),
                                 BasicNetworkOperator(55673),
                                 BasicNetworkOperator(72405), # Claro
                                 BasicNetworkOperator(74201),],
            # register with network succeeds
            'register_with_network' : 'OK',
        }
        
        device = DeviceStub(pattern)
        sm = NetworkRegStateMachine(device)
        d = sm.start_netreg()
        # assert we're connected to Claro GPRS
        d.addCallback(lambda resp: self.assertEqual(resp, (72405, "GPRS")))
        return d
