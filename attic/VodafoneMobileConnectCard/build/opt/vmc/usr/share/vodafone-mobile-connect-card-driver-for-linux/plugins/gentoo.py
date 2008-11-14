# -*- coding: utf-8 -*-
# Copyright (C) 2008  Vodafone España, S.A.
# Author:  Rafael Treviño
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
Gentoo OSPlugin
"""

__version__ = "$Rev: 1172 $"

import re

from vmc.common.oses import LinuxPlugin

gentoo_customization = {
    'WVDIAL_CONN_SWITCH' : '--config',
    'gksudo_name' : 'gksu',
}

class GentooBasedDistro(LinuxPlugin):
    os_name = re.compile('Gentoo')
    os_version = None
    customization = gentoo_customization

gentoo = GentooBasedDistro()
