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

"""Unittests for the profiles module"""

__version__ = "$Rev: 1172 $"

import shutil
import os

from twisted.trial import unittest

from vmc.common.profiles import ProfileManager
from vmc.common.configbase import MobileProfile
from vmc.common.config import VMCConfig
from vmc.common.exceptions import ProfileInUseError

from vmc.utils.utilities import save_file

TMP_PATH = '/tmp/profiles.foo'

TEMPLATE = """
[profile]
name = profile-test
last_device =
updater =
"""

VMC_CFG = '/tmp/vmc.cfg'
save_file(VMC_CFG, TEMPLATE)

class TestProfileManager(unittest.TestCase):
    """Test for L{vmc.common.profiles.ProfileManager} functionality"""
    # XXX: We have 0 coverage on all operations that depend on a device
    # edit_profile, load_profile
    
    def setUpClass(self):
        os.mkdir(TMP_PATH)
        self.mana = ProfileManager(TMP_PATH)
        self.mana.config = VMCConfig(VMC_CFG)
    
    def tearDownClass(self):
        shutil.rmtree(TMP_PATH)
        self.mana = None
    
    def test_add_and_delete_profile_in_use(self):
        """
        Test that adding a profile works
        
        Test also that deleting the active profile raises an exception
        """
        profdict = dict(profile_name='profile-test',
                        username='vodafone',
                        password='vodafone',
                        connection='3GONLY',
                        apn='ac.vodafone.es',
                        dialer_profile='default',
                        staticdns=False,
                        dns1=None,
                        dns2=None)
        
        profile = self.mana.create_profile(profdict['profile_name'], profdict)
        self.mana.add_profile(profile)
        profiles = self.mana.get_profile_list()
        self.assertIn(profile, profiles)
        self.assertRaises(ProfileInUseError, self.mana.delete_profile, profile)
    
    def test_add_and_delete_profile_not_in_use(self):
        """
        Test that adding a profile works
        
        Test also that deleting a profile not active works
        """
        profdict = dict(profile_name='profile-test2',
                        username='vodafone',
                        password='vodafone',
                        connection='GPRSONLY',
                        apn='ac.vodafone.es',
                        dialer_profile='default',
                        staticdns=False,
                        dns1=None,
                        dns2=None)
        
        profile = self.mana.create_profile(profdict['profile_name'], profdict)
        self.mana.add_profile(profile)
        profiles = self.mana.get_profile_list()
        self.assertIn(profile, profiles)
        self.mana.delete_profile(profile)
        profiles2 = self.mana.get_profile_list()
        self.assertNotIn(profile, profiles2)
        