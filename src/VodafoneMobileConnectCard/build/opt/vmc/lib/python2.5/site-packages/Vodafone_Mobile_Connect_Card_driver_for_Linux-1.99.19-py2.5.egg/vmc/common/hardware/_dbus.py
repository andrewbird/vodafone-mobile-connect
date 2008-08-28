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
        return [self.get_properties_from_udi(udi)
                    for udi in self.manager.GetAllDevices()]


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

class Node(object):
    def __init__(self, devinfo, parent=None):
        self.devinfo = devinfo
        self.parent = parent
        self.children = []
    
    def __repr__(self):
        return '<Node udi=%s>' % str(self.devinfo['info.udi'])

    def __getitem__(self, key):
        try:
            return self.devinfo[key]
        except:
            raise

    def search(self, properties):
        def search_in_children():
            found = []
            for child in self.children:
                found += child.search(properties)
            return found
        for key, property in properties:
            if self.devinfo[key] != property:
                return search_in_children()
        return [self]

class DBusTree(object):
    def __init__(self, root, devices):
        self.root = root
        self.devices = devices
    
    def __repr__(self):
        def print_node(node, padding=0):
            rep = (' ' * padding) + node.__repr__() + '\n'
            for child in node.children:
                rep += print_node(child, padding + 1)
            return rep
        return print_node(self.root)

    def __get_item__(self, key):
        return self.devices[key]

    def search_nodes(self, properties):
        self.root.search(properties)

class DBusHardwareRegistry(DbusComponent):
    #implements(IHardwareRegistry)

    def __init__(self):
        super(DBusHardwareRegistry, self).__init__()
        self.dirty = True
        self._register_handlers()

    def get_devices(self):
        if self.dirty:
            self._update_registry()
        #XXX: get devices from registry that have a plugin to manage them and
        # cached plugins

    def _register_handlers(self):
        print "REGISTER_HANDLERS"
        self.manager.connect_to_signal('DeviceAdded', self._hardware_changed)
        self.manager.connect_to_signal('DeviceRemoved', self._hardware_changed)

    def _hardware_changed(self, udi):
        print "DIRTY"
        self.dirty = True

    def _update_registry(self):
        self.registry = self._get_dbus_tree()
        self.dirty = False

    def _get_dbus_tree(self):
        def get_properties_from_udi(udi):
            """Returns all the properties from C{udi}"""
            obj = self.bus.get_object('org.freedesktop.Hal', udi)
            dev = dbus.Interface(obj, 'org.freedesktop.Hal.Device')
            return dev.GetAllProperties()

        def get_devices_properties():
            """Returns all the properties from all devices registed in HAL"""
            return [get_properties_from_udi(udi)
                        for udi in self.manager.GetAllDevices()]

        devices = {}
        for properties in get_devices_properties():
            devices[str(properties['info.udi'])] = Node(properties)

        for udi in devices:
            node = devices[udi]
            if 'info.parent' in node.devinfo:
                node.parent = devices[str(node['info.parent'])]
                node.parent.children.append(node)
            else:
                parent_node = node

        return DBusTree(parent_node, devices)

#XXX: hardware_registry = DBusHardwareRegistry()
