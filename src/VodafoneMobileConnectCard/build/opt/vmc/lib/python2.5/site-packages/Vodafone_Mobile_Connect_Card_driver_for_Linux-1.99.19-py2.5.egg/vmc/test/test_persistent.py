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

"""Unittests for the persistent module"""

__version__ = "$Rev: 1172 $"

import datetime
import shutil

from twisted.trial import unittest

from vmc.common.encoding import pack_ucs2_bytes as pack
from vmc.common.sms import ShortMessage
from vmc.common.persistent import (Contact, ContactsManager,
                                   SMSManager, NetworkOperatorManager,
                                   UsageManager)

from vmc.contrib.epsilon.extime import Time

TMPFILE = '/tmp/foo.db'

class TestContactsManager(unittest.TestCase):
    """Test for L{vmc.common.persistent.ContactsManager} functionality"""

    def setUpClass(self):
        self.mana = ContactsManager(TMPFILE)
    
    def tearDownClass(self):
        self.mana.close()
        shutil.rmtree(TMPFILE)
    
    def test_add_contact(self):
        contact = Contact('Peter', '+3453453452')
        c1 = self.mana.add_contact(contact)
        self.assertEqual(contact, self.mana.get_contact_by_id(c1.get_index()))
        contact2 = Contact('John', '+45364563345')
        c2  = self.mana.add_contact(contact2)
        self.assertEqual(contact2,
                         self.mana.get_contact_by_id(c2.get_index()))
    
    def test_find_contact(self):
        contact = Contact('Pepito', '+3453423423423')
        c1 = self.mana.add_contact(contact)
        resp = list(self.mana.find_contacts('Pe'))
        self.failUnlessIn(c1, resp)
    
    def test_delete_contact(self):
        contact = Contact(pack('Paul'), '+45364563345')
        c1 = self.mana.add_contact(contact)
        self.mana.delete_contact_by_id(c1.get_index())
        self.assertRaises(KeyError, self.mana.get_contact_by_id,
                                    c1.get_index())


class TestSMSManager(unittest.TestCase):
    """Test for L{vmc.common.persistent.SMSManager} functionality"""

    def setUpClass(self):
        self.mana = SMSManager(TMPFILE)
        self.now = datetime.datetime.now()
    
    def tearDownClass(self):
        self.mana.close()
        shutil.rmtree(TMPFILE)
    
    def test_add_messages(self):
        now = datetime.datetime.now()
        _sms1 = ShortMessage(u'+4554354333', u'how are ya', self.now)
        _sms2 = ShortMessage(u'+3546564564', u'hola!', self.now)
        _sms3 = ShortMessage(u'+4354534534', u'adios', self.now)
        
        _list = [_sms1, _sms2, _sms3]
        responses = self.mana.add_messages(_list, where=2)
        
        for _sms in [_sms1, _sms2, _sms3]:
            self.failUnlessIn(_sms, responses)
    
    def test_delete_messages(self):
        smslist = [
            ShortMessage(u'+455438983', u'hey man', self.now),
            ShortMessage(u'+4554354333', u'how are ya', self.now),
            ShortMessage(u'+3546564564', u'hola!', self.now),
            ShortMessage(u'+4354534534', u'adios', self.now),
        ]
        
        responses = self.mana.add_messages(smslist, where=2)
        exp = responses.pop(0)
        
        for _sms in responses:
            self.mana.delete_message_by_id(_sms.get_index())

        messages = list(self.mana.get_messages())
        self.failUnlessIn(exp, messages)


class TestNetworksManager(unittest.TestCase):
    """
    Tests for the NetworksManager
    """
    def setUpClass(self):
        self.mana = NetworkOperatorManager(TMPFILE)
        networks = __import__('resources/extra/networks')
        instances = [getattr(networks, item)() for item in dir(networks)
            if (not item.startswith('__') and item != 'NetworkOperator')]
        return self.mana.populate_networks(instances)
    
    def tearDownClass(self):
        self.mana.close()
        shutil.rmtree(TMPFILE)
    
    def test_lookup_network(self):
        """
        Test that looking up a known netid (21401) works
        """
        network = self.mana.get_network_by_id(21401)
        self.assertEqual(network.name, 'Vodafone')
        self.assertEqual(network.country, 'Spain')
    
    def test_lookup_inexistent_network(self):
        """
        Test that looking up an unknown netid (6002 atm) returns None
        """
        network = self.mana.get_network_by_id(6002)
        self.assertEqual(network, None)


class TestUsageManager(unittest.TestCase):
    """
    Tests for the UsageManager
    """
    def setUpClass(self):
        self.mana = UsageManager(TMPFILE)
    
    def tearDownClass(self):
        self.mana.close()
        shutil.rmtree(TMPFILE)
    
    def test_append_item(self):
        """
        Test that appending a couple of usage items works
        """
        args = [True, Time.fromDatetime(datetime.datetime.now()),
                Time.fromDatetime(datetime.datetime.now() + datetime.timedelta(minutes=59)),
                112100, 121222]
        args2 = [False, Time.fromDatetime(datetime.datetime.now() - datetime.timedelta(minutes=43)),
                Time.fromDatetime(datetime.datetime.now() + datetime.timedelta(minutes=50)),
                11244443, 12243453]
        
        item1 = self.mana.add_usage_item(*args)
        item2 = self.mana.add_usage_item(*args2)
        
        self.assertEquals(self.mana.store.getItemByID(item1.storeID), item1)
        self.assertEquals(self.mana.store.getItemByID(item2.storeID), item2)
        
        item1.deleteFromStore()
        item2.deleteFromStore()
    
    def test_get_usage_for_day(self):
        """
        Append 2 3G sessions that occurred 21/11/07 and get usage for that day
        """
        # 16:20 PM  21 Nov 2007
        now = datetime.datetime(2007, 11, 21, 16, 20)
        
        args = [True, Time.fromDatetime(now), # from now to now + 60m (60min)
                Time.fromDatetime(now + datetime.timedelta(minutes=45)),
                11212100, 12321222]
        
        args2 = [True, # from now + 80m to now + 120m  (40min)
                 Time.fromDatetime(now + datetime.timedelta(minutes=80)),
                 Time.fromDatetime(now + datetime.timedelta(minutes=120)),
                 112128, 1232121]
        
        item1 = self.mana.add_usage_item(*args)
        item2 = self.mana.add_usage_item(*args2)
        
        resp = self.mana.get_usage_for_day(now.date())
        
        self.failUnlessIn(item1, resp)
        self.failUnlessIn(item2, resp)
    
    def test_get_usage_for_month(self):
        # 16:20 PM  21 Nov 2006
        now = datetime.datetime(2006, 11, 21, 16, 20)
        
        args = [True, # from now + 180m to now + 210m  (30min)
                Time.fromDatetime(now + datetime.timedelta(minutes=180)),
                Time.fromDatetime(now + datetime.timedelta(minutes=210)),
                112128, 1232121]
        
        item3 = self.mana.add_usage_item(*args)
        
        resp = list(self.mana.get_usage_for_month(now.date()))
        self.failUnless(len(resp) == 1)
        self.failUnlessIn(item3, resp)
        
