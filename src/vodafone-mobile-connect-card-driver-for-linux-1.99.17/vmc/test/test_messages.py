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
Unittests for the SIM card

You need to be authenticated before running the test suite
"""

__version__ = "$Rev: 1141 $"

import os
import datetime

from twisted.trial.unittest import TestCase, SkipTest

import vmc.common.exceptions as ex
from vmc.common.hardware import HardwareRegistry
from vmc.common.startup import attach_serial_protocol
from vmc.common.configbase import VMCConfigBase
from vmc.common.statem.auth import AuthStateMachine
from vmc.common.sms import ShortMessage, ShortMessageSubmit
from vmc.common.persistent import DBShortMessage
from vmc.cli.collaborator import CLICollaboratorFactory
from vmc.common.messages import get_messages_obj


PATH = '/tmp/settings.conf'

if not os.path.exists(PATH):
    conf = None
else:
    conf = VMCConfigBase(PATH)
    

class TestMessages(TestCase):
    """Test for SIM card functionality"""
    
    def setUpClass(self):
        self.sconn = None
        self.serial = None
        self.device = None
        self.messages = None
        
        hw = HardwareRegistry()
        d = hw.get_devices()
        def get_devices_cb(devices):
            self.device = attach_serial_protocol(devices[0], test=False)
            self.sconn = self.device.sconn
            self.sport = self.device.sport
            d2 = self.device.preinit()
            d2.addCallback(self._authenticate)
            return d2
        
        d.addCallback(get_devices_cb)
        return d
    
    def tearDownClass(self):
        self.sconn.transport.unregisterProducer()
        self.sport.loseConnection("Bye bye")
        self.sport = None
        self.sconn = None
        self.device = None
    
    def _authenticate(self, ignored=None):
        if not conf:
            raise SkipTest("Not config")
        
        def post_configure_device(ignored):
            d = self.device.postinit()
            d.addCallback(lambda _: self.sconn.delete_all_sms())
            d.addCallback(lambda _: self.sconn.delete_all_contacts())
            self.messages = get_messages_obj(self.sconn)
            return d
        
        def check_pin_status(ignored):
            d = self.sconn.check_pin()
            #d.addCallback(lambda status: self.assertEqual(status, 'READY'))
            d.addCallback(post_configure_device)
            return d
        
        config = {'pin' : conf.get('test', 'pin')}
        authsm = AuthStateMachine(self.device, CLICollaboratorFactory, config)
        d = authsm.start_auth()
        d.addCallback(check_pin_status)
        return d
   
 
    def test_add_message_in_db(self):
        """
        Test that checks if a message is correctly added.
        """
        s = ShortMessage(u'+3456345435', u'how are you man',
                            _datetime=datetime.datetime.now())
        d = self.messages.add_message(s, 2)
        def add_message_cb(sms):
            d2 = self.messages.get_messages()
            d2.addCallback(lambda smslist: self.assertIn(sms, smslist))
            d2.addCallback(lambda _: self.messages.delete_messages([sms]))
            return d2

        d.addCallback(add_message_cb)            
        return d

    def test_add_messages_in_db_and_get_messages(self):
        """
        Test that checks if a list of messages is correctly added, and if
        get_messages works
        """       
        sms_list = [ShortMessage(u'+3456345435', u'how are you man',
                            _datetime=datetime.datetime.now()),
                    ShortMessage(u'+3400000000', u'how are you?',
                            _datetime=datetime.datetime.now())]
        
        responses = self.messages.add_messages(sms_list, 1)

        def check_messages(list):
            for sms in responses:
                self.assertIn(sms, list)
            self.messages.delete_messages(responses)

        d = self.messages.get_messages()        
        d.addCallback(check_messages)
        return d

    def test_delete_messages(self):
        """
        Test that checks the correct behaivour of messages deletion adding two
        messages, deleting one and checking that this one and only this one has
        been removed.
        """
        sms_list = [ShortMessage(u'+3456345435', u'how are you man',
                            _datetime=datetime.datetime.now()),
                    ShortMessage(u'+3400000000', u'how are you?',
                            _datetime=datetime.datetime.now())]
        
        responses = self.messages.add_messages(sms_list, 1)

        def check_messages(list):
            self.failIfIn(responses[0], list)
            self.failUnlessIn(responses[1], list)
            self.messages.delete_messages([responses[1]])

        def delete_one(list):
            self.messages.delete_messages([responses[0]])
            d2 = self.messages.get_messages()
            d2.addCallback(check_messages)
            return d2

        d = self.messages.get_messages()        
        d.addCallback(delete_one)        
        return d

    def test_get_message_from_sim(self):
        """
        Test that tries to recover a sms stored in sim.
        """
        raise SkipTest("ShortMessageSubmit reading is not yet supported")

        sms = ShortMessageSubmit('+3456345435', 'how are you man',
                                 conf.get('test', 'smsc'),
                                 _datetime=datetime.datetime.now())
       
        def check_message(stored_sms):
            self.failUnlessEqual(sms, stored_sms)
            return self.sconn.delete_sms(sms.index)

        def sms_stored(index):
            sms.index = index
            d2 = self.messages.get_message(sms)
            d2.addCallback(check_message)
            return d2

        d = self.sconn.add_sms(sms)
        d.addCallback(sms_stored)
        return d
