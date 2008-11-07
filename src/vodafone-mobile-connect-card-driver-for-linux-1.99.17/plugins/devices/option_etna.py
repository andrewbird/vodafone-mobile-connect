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

__version__ = "$Rev: 1190 $"

from vmc.common.hardware.option import (OptionDBusDevicePlugin,
                                        OptionCustomizer)
from vmc.common.middleware import SIMCardConnAdapter

class OptionEtnaSIMCardConnAdapter(SIMCardConnAdapter):
    def get_roaming_ids(self):
        # FW 2.8.0Hd while panik if AT+CPOL is sent while in UCS2, we will
        # switch to IRA, perform the operation and switch back to UCS2
        self.set_charset("IRA")
        d = super(OptionEtnaSIMCardConnAdapter, self).get_roaming_ids()
        def get_roaming_ids_cb(rids):
            d2 = self.set_charset("UCS2")
            d2.addCallback(lambda _: rids)
            return d2
        
        d.addCallback(get_roaming_ids_cb)
        return d
    
    def find_contacts(self, pattern):
        """Returns a list of C{Contact} whose name matches pattern"""
        # ETNA's AT+CPBF function is broken, it always raises a
        # CME ERROR: Not Found (at least with the following firmware rev:
        # FW 2.8.0Hd (Date: Oct 11 2007, Time: 10:20:29))
        # we have no option but to use this little hack and emulate AT+CPBF
        # getting all contacts and returning those whose name match pattern
        # this will be slower than AT+CPBF with many contacts but at least
        # works
        d = super(OptionEtnaSIMCardConnAdapter, self).get_contacts()
        d.addCallback(lambda contacts: [c for c in contacts
                                        if c.get_name().startswith(pattern)])
        return d


class OptionEtnaCustomizer(OptionCustomizer):
    adapter = OptionEtnaSIMCardConnAdapter


class OptionEtna(OptionDBusDevicePlugin):
    """L{vmc.common.plugin.DBusDevicePlugin} for Options's Etna"""
    name = "Option Etna"
    version = "0.1"
    author = u"Pablo Martí"
    custom = OptionEtnaCustomizer
    
    __remote_name__ = "GlobeTrotter HSUPA Modem"
    
    __properties__ = {
          'usb_device.vendor_id' : [0x0af0],
          'usb_device.product_id': [0x7001],
    }

optionetna = OptionEtna()
