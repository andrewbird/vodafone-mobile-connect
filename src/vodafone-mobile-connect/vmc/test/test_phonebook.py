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
Tests for the phonebook module
"""

__version__ = "$Rev: 1172 $"

import os

from twisted.trial.unittest import TestCase, SkipTest

import vmc.common.exceptions as ex
from vmc.common.hardware import HardwareRegistry
from vmc.common.startup import attach_serial_protocol
from vmc.common.configbase import VMCConfigBase
from vmc.common.statem.auth import AuthStateMachine
from vmc.common.persistent import Contact
from vmc.cli.collaborator import CLICollaboratorFactory
from vmc.common.phonebook import get_phonebook


PATH = '/tmp/settings.conf'

if not os.path.exists(PATH):
    conf = None
else:
    conf = VMCConfigBase(PATH)
    

class TestPhoneBook(TestCase):
    """Test for the phonebook module"""
    
    def setUpClass(self):
        self.sconn = None
        self.serial = None
        self.device = None
        self.phonebook = None
        
        hw = HardwareRegistry()
        d = hw.get_devices()
        def get_devices_cb(devices):
            self.device = attach_serial_protocol(devices[0], test=False)
            self.sconn = self.device.sconn
            self.sport = self.device.sport
            return self._authenticate()
        
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
            d = self.device.initialize()
            d.addCallback(lambda _: self.sconn.delete_all_sms())
            d.addCallback(lambda _: self.sconn.delete_all_contacts())
            self.phonebook = get_phonebook(self.sconn)
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
    
    def test_add_contact_in_sim(self):
        c = Contact("Peter", "+34673434321")
        def process_contact(contact):
            d2 = self.phonebook.get_contacts()
            d2.addCallback(lambda contacts: self.assertIn(contact, contacts))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=True)
        d.addCallback(process_contact)
        return d
    
    def test_add_contact_in_db(self):
        c = Contact("Paul", "+34673435676")
        def process_contact(contact):
            d2 = self.phonebook.get_contacts()
            d2.addCallback(lambda contacts: self.assertIn(contact, contacts))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=False)
        d.addCallback(process_contact)
        return d
    
    def test_edit_contact(self):
        c = Contact("James", "+34673434222")
        def process_contact(contact):
            contact.name = 'John'
            d2 = self.phonebook.edit_contact(contact)
            d2.addCallback(lambda contactback:
                           self.assertEqual(contactback.name, 'John'))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=True)
        d.addCallback(process_contact)
        return d
    
    def test_find_contact_in_db_by_name(self):
        c = Contact("Aitor", "+34673232322")
        def process_contact(contact):
            d2 = self.phonebook.find_contact("Ai")
            d2.addCallback(lambda contacts: self.assertIn(contact, contacts))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=False)
        d.addCallback(process_contact)
        return d
    
    def test_find_contact_in_db_by_number(self):
        c = Contact("Jaume", "+34633223422")
        def process_contact(contact):
            d2 = self.phonebook.find_contact(number='+34633223422')
            d2.addCallback(lambda contacts: self.assertIn(contact, contacts))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=False)
        d.addCallback(process_contact)
        return d
    
    def test_find_contact_in_sim_by_name(self):
        c = Contact("Peter", "+34673434321")
        def process_contact(contact):
            d2 = self.phonebook.find_contact("Pet")
            d2.addCallback(lambda contacts: self.assertIn(contact, contacts))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=True)
        d.addCallback(process_contact)
        return d
    
    def test_find_contact_in_sim_by_number(self):
        c = Contact("Lucy", "+34673432239")
        def process_contact(contact):
            d2 = self.phonebook.find_contact(number="+34673432239")
            d2.addCallback(lambda contacts: self.assertIn(contact, contacts))
            d2.addCallback(lambda _: self.phonebook.delete_contact(contact))
            return d2
        
        d = self.phonebook.add_contact(c, sim=True)
        d.addCallback(process_contact)
        return d
    
        
