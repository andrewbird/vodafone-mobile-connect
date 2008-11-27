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
"""dbus stuff"""

import dbus

if getattr(dbus, 'version', (0, 0, 0)) >= (0, 41, 0):
    # otherwise wont work
    import dbus.glib

from twisted.internet import reactor
from twisted.python import log

from vmc.contrib import louie
from vmc.common.interfaces import IDBusDevicePlugin, IRemoteDevicePlugin
import vmc.common.notifications as notifications


class DbusComponent(object):
    """I provide a couple of useful methods to deal with DBus"""
    
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.obj = self.bus.get_object('org.freedesktop.Hal',
                                  '/org/freedesktop/Hal/Manager')
        self.manager = dbus.Interface(self.obj, 'org.freedesktop.Hal.Manager')

    def get_properties_from_udi(self, udi):
        """Returns all the properties from C{udi}"""
        obj = self.bus.get_object('org.freedesktop.Hal', udi)
        dev = dbus.Interface(obj, 'org.freedesktop.Hal.Device')
        return dev.GetAllProperties()
    
    def get_devices_properties(self):
        """Returns all the properties from all devices registed in HAL"""
        props = {}
        for udi in self.manager.GetAllDevices():
            props[udi] = self.get_properties_from_udi(udi)

        return props


class DeviceListener(DbusComponent):
    """
    I listen for Device{Added,Removed} signals
    
    If a new device is added and I don't have a registered device, I will send
    a L{vmc.common.notifications.SIG_DEVICE_ADDED} so the upper parts of the
    system will do whatever they want to do with the device. If the device in
    use is removed, I will notify the upper parts of the system and they will
    act accordingly
    """
    def __init__(self, device):
        DbusComponent.__init__(self)
        self.device = device
        self.register_handlers()
    
    def register_handlers(self):
        self.manager.connect_to_signal('DeviceAdded', self.device_added)
        self.manager.connect_to_signal('DeviceRemoved', self.device_removed)
    
    def device_added(self, udi):
        """Called when a device has been added"""
        if self.device:
            # if we already have an active device, ignore the new device
            return
        
        # leave it alone four seconds so the device can settle and register
        # itself with the kernel properly
        reactor.callLater(4, self.process_device_added)
    
    def process_device_added(self):
        from vmc.common.plugin import PluginManager
        properties = self.get_devices_properties()
        for plugin in PluginManager.get_plugins(IDBusDevicePlugin):
            if plugin in properties:
                plugin.setup(properties)
                louie.send(notifications.SIG_DEVICE_ADDED, None, plugin)
                self.device = plugin
    
    def device_removed(self, udi):
        """Called when a device has been removed"""
        if not self.device:
            return
        
        if IRemoteDevicePlugin.providedBy(self.device):
            log.msg("DEVICE %s REMOVED" % udi)
            return
        
        if self.device.udi == udi:
            louie.send(notifications.SIG_DEVICE_REMOVED, None)
            self.device = None

