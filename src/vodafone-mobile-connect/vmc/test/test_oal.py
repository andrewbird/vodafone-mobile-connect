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
Unit tests for the Operating System Abstraction Layer
"""

__version__ = "$Rev$"

from os.path import join

from pytz import timezone

from twisted.trial.unittest import TestCase, SkipTest
from twisted.internet.utils import getProcessValue
from twisted.python import procutils

from vmc.common.consts import TOP_DIR
from vmc.common.oal import osobj
from vmc.common.runtime import app_is_frozen
from vmc.common.plugin import PluginManager
from vmc.common.hardware.hardwarereg import hw_reg
from vmc.common.plugins.linuxbundled import BundledDistro
from vmc.common.interfaces import IOSPlugin

class TestOAL(TestCase):
    
    def setUpClass(self):
        try:
            self.os = osobj
            self.frozen = app_is_frozen()
        except :
            self.os = None

    def check_os_registered(self):
        if not self.os:
            raise SkipTest("No valid OS found")

    def check_frozen(self):
        if not self.frozen:
            raise SkipTest("Test for frozen distribution")

    def get_os_by_lsb(self, lsb):
        for plugin in PluginManager.get_plugins(IOSPlugin):
            if plugin.is_valid() and not isinstance(osplugin, BundledDistro):
                return plugin

    def test_bundle_mixin(self):
        self.check_frozen()
        if hw_reg.os_info:
            os = self.get_os_by_lsb(hw_reg.os_info)
            if not os:
                raise SkipTest("I couldn't find a suitable OS plugin")
            self.failUnlessEqual(self.os.__class__.__bases__, (os.__class__,))

    def test_get_iface_stats(self):
        """
        Test that checks if interface stats can be obtained.
        """
        def get_stats_cb(stats):
            self.failUnless(isinstance(stats, list))
            self.failUnless(len(stats) == 2)
            #XXX:self.failUnless(isinstance(stats[0], int), msg=stats[0])
            #XXX:self.failUnless(isinstance(stats[1], int), msg=stats[1])
        d = self.os.get_iface_stats()
        d.addCallback(get_stats_cb)
        return d

    def test_get_timezone(self):
        """
        Test that checks if the OS object can get a timezone that pytz can
        understand.
        """
        self.check_os_registered()
        zone = self.os.get_timezone()
        if zone == None:
            raise SkipTest("Timezone is None")
        timezone(zone)

    def test_os_validations(self):
        """
        Test that looks for a suitable plugin for any supported OS.
        """
        lsb = {
            'debian':   dict(os_name = "Debian", os_version=""),
            'fedora':   dict(os_name = "Fedora", os_version=""),
            #XXX: 'freebsd':  dict(os_name = "", os_version=700000),
            'suse':     dict(os_name = "SUSE LINUX", os_version=""),
            'ubuntu':   dict(os_name = "Ubuntu", os_version="")
        }
        failed = []
        for os_name, os_lsb in lsb.iteritems():
            if not self.get_os_by_lsb(os_lsb): failed.append(os_name)

        self.failIf(failed, msg="Failed validations: " + str(failed))

    def test_privileges_needed(self):
        """
        The cases where we don't need special privileges are:
        - When running from a bundled installation.
        - When running as root user.
        - When pppd is not setuided.

        It runs pppd and check if it returns the expected value.
        """
        self.check_os_registered()

        def run_pppd():
            try:
                pppd_path = procutils.which('pppd')[0]
            except IndexError:
                pppd_path = join(TOP_DIR, 'usr', 'sbin', 'pppd')
            return getProcessValue(pppd_path, args=("/dev/null",))

        if self.os.are_privileges_needed():
            d = run_pppd()
            d.addCallback(lambda code : self.failUnlessEqual(code, 3))
        else:
            d = run_pppd()
            d.addCallback(lambda code : self.failIfEqual(code, 3))
        return d

    def test_registered_os(self):
        self.failUnless(self.os)
