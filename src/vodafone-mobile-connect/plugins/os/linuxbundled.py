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
"""Bundled OSPlugin"""

__version__ = "$Rev: 1172 $"

from twisted.python.procutils import which

from vmc.common.oses import LinuxPlugin
from vmc.common.runtime import app_is_frozen

from vmc.common.plugin import PluginManager
from vmc.common.interfaces import IOSPlugin
from vmc.common.hardware import hw_reg

bundled_customization = {
    'WVDIAL_CONN_SWITCH' : '--config',
}

class BundledDistro(LinuxPlugin):
    os_name = None
    os_version = None
    
    customization = bundled_customization

    def initialize(self):
        super(BundledDistro, self).initialize()
        for plugin in PluginManager.get_plugins(IOSPlugin):
            if (plugin.is_valid() and plugin.__class__ != self.__class__):
                self.__class__.__bases__ = (plugin.__class__,)
                return

    def is_valid(self):
        return app_is_frozen()
    
    def get_connection_args(self, dialer):
        assert dialer.binary == 'wvdial'
        
        if not self.privileges_needed:
            return [dialer.bin_path, self.abstraction['WVDIAL_CONN_SWITCH'],
                    dialer.conf_path, 'connect']
        else:
            gksudo_name = self.abstraction['gksudo_name']
            gksudo_path = which(gksudo_name)[0]
            return [gksudo_path, dialer.bin_path,
                    self.abstraction['WVDIAL_CONN_SWITCH'],
                    dialer.conf_path, 'connect']
    
    def get_disconnection_args(self, dialer):
        assert dialer.binary == 'wvdial'
        
        killall_path = which('killall')[0]
        if not self.privileges_needed:
            return [killall_path, 'pppd', 'wvdial']
        else:
            gksudo_name = self.abstraction['gksudo_name']
            gksudo_path = which(gksudo_name)[0]
            return [gksudo_path, killall_path, 'pppd', 'wvdial']

bundle = BundledDistro()
