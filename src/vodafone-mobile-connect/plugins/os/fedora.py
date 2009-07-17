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
"""Fedora OSPlugin"""
__version__ = "$Rev: 1179 $"

import re

from twisted.python.procutils import which

from vmc.common.oses import LinuxPlugin
from vmc.utils.utilities import get_file_data

fedora_customization = {
    'WVDIAL_CONN_SWITCH' : '--config',
    'gksudo_name' : 'gksu',
}

class FedoraBasedDistro(LinuxPlugin):
    """
    OSPlugin for Fedora-based distros
    """
    os_name = re.compile("Fedora")
    os_version = None    #FEDORA_GENERAL
    os_version = re.compile("11")     #FEDORA_11
    customization = fedora_customization
    os_groups = ['dip', 'uucp', 'lock']    #FEDORA_GENERAL
    os_groups = ['dialout', 'lock']        #FEDORA_11

    #XXX: Almost duplicated code with Suse plugin
    def get_timezone(self):
        timezone_re = re.compile('ZONE="(?P<tzname>[\w/]+)"')
        sysconf_clock_file = get_file_data('/etc/sysconfig/clock')
        search_dict = timezone_re.search(sysconf_clock_file).groupdict()
        return search_dict['tzname']
 
    def get_connection_args(self, dialer):
        assert dialer.binary == 'wvdial'
        
        if not self.privileges_needed:
            return [dialer.bin_path, self.abstraction['WVDIAL_CONN_SWITCH'],
                    dialer.conf_path, 'connect']
        
        gksudo_name = self.abstraction['gksudo_name']
        gksudo_path = which(gksudo_name)[0]
        args = [dialer.bin_path, self.abstraction['WVDIAL_CONN_SWITCH'],
                dialer.conf_path, 'connect']
        return [gksudo_path, '-g', " ".join(args)]
    
    def get_disconnection_args(self, dialer):
        assert dialer.binary == 'wvdial'
        
        killall_path = which('killall')[0]
        if not self.privileges_needed:
            return [killall_path, 'pppd', 'wvdial']
        
        gksudo_name = self.abstraction['gksudo_name']
        gksudo_path = which(gksudo_name)[0]
        args = " ".join([killall_path, 'pppd', 'wvdial'])
        return [gksudo_path, '-g', args]

class YellowDogLinuxDistro(LinuxPlugin):
    """
    OSPlugin for YDL
    """
    os_name = re.compile("YellowDog")

fedora = FedoraBasedDistro()
yellowdog = YellowDogLinuxDistro()
