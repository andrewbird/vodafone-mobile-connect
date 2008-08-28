# -*- coding: utf-8 -*-
# Copyright (C) 2006-2008  Vodafone España, S.A.
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

__version__ = "$Rev$"

from vmc.common.plugin import RemoteDevicePlugin
from vmc.common.hardware.nokia import NokiaCustomizer, NokiaSIMBaseClass

class Nokia6230(RemoteDevicePlugin):
    """L{vmc.common.plugin.RemoteDevicePlugin} for Nokia's 6230"""
    name = "Nokia 6230"
    version = "0.1"
    author = u"Pablo Martí"
    custom = NokiaCustomizer
    simklass = NokiaSIMBaseClass

    __remote_name__ = "Nokia 6230"

nokia6230 = Nokia6230()
