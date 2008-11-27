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
"""Plugin system for VMCCdfL2"""

__version__ = "$Rev: 1172 $"

import os
from os.path import join
import stat

from pytz import timezone

from zope.interface import implements

from twisted.python import log, procutils
from twisted.plugin import IPlugin, getPlugins

from vmc.common.consts import WVDIAL_AUTH_CONF, TOP_DIR
import vmc.common.exceptions as ex
import vmc.common.interfaces as interfaces
from vmc.common.runtime import app_is_frozen
from vmc.common.sim import SIMBaseClass

VERSION = 2

BASE_PATH_DICT = {
      'WVDIAL_AUTH_CONF': WVDIAL_AUTH_CONF,
      'WVDIAL_CONN_SWITCH' : '-C',
      'gksudo_name' : 'gksudo',
      'CFG_TEMPLATE' : 'vmc.cfg.tpl',
}

DEFAULT_TEMPLATE = """
debug
noauth
name wvdial
ipparam vmc
noipdefault
nomagic
usepeerdns
ipcp-accept-local
ipcp-accept-remote
nomp
noccp
nopredictor1
novj
novjccomp
nobsdcomp"""

PAP_TEMPLATE = DEFAULT_TEMPLATE + """
refuse-chap
refuse-mschap
refuse-mschap-v2
refuse-eap
"""

CHAP_TEMPLATE = DEFAULT_TEMPLATE + """
refuse-pap
"""

TEMPLATES_DICT = {
    'default' : DEFAULT_TEMPLATE,
    'PAP' : PAP_TEMPLATE,
    'CHAP' : CHAP_TEMPLATE,
}

def flatten_list(x):
    """
    Flattens C{x} into a single list
    """
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten_list(el))
        else:
            result.append(el)
    return result


class DevicePlugin(object):
    """Base class of all DevicePlugins"""
    
    implements(IPlugin, interfaces.IDevicePlugin)
    # at what speed should we talk with this device?
    baudrate = 115200
    # control port
    cport = None
    # data port
    dport = None
    # instance of a custom adapter class if device needs customization
    custom = None
    # serial connection reference
    sconn = None
    # SerialPort reference
    sport = None
    # Class that will initialize the SIM, by default SIMBaseClass
    simklass = SIMBaseClass
    # Response of AT+CGMM
    __remote_name__ = ""
    
    def __init__(self):
        super(DevicePlugin, self).__init__()
        # control port
        self.cport = None
        # data port
        self.dport = None
        # sim instance
        self.sim = None

    def initialize(self):
        """
        Post-initializes the SIM

        @rtype: L{twisted.internet.defer.Deferred}
        @return: SIM phonebook size
        """
        self.sim = self.simklass(self.sconn)
        return self.sim.initialize()

    def has_two_ports(self):
        try:
            return self.cport != None
        except AttributeError:
            return False

    def patch(self, other):
        """
        Patch myself in-place with the settings of another plugin
        """
        if not isinstance(other, DevicePlugin):
            raise ValueError("Cannot patch myself with a %s" % type(other))

        self.cport = other.cport
        self.dport = other.dport
        self.baudrate = other.baudrate


class DBusDevicePlugin(DevicePlugin):
    """
    Base class from which all the DBusDevicePlugins should inherit from
    """
    implements(IPlugin, interfaces.IDBusDevicePlugin)
    
    __properties__ = {}
    
    def __init__(self):
        super(DBusDevicePlugin, self).__init__()
        self.udi = None
        self.parent_udi = None
    
    def __eq__(self, other):
        # I can be compared against a DBusDevicePlugin
        if isinstance(other, DBusDevicePlugin):
            for k in self.__properties__:
                if k not in other.__properties__:
                    # not the same plugin for sure!
                    return False
                
                self_pvalues = self.__properties__[k]
                other_pvalues = other.__properties__[k]
                if not len(set(self_pvalues) & set(other_pvalues)):
                    # selfp_values is a list of ints (valid product/device ids
                    # to consider that this plugin exists in the system).
                    # If the result of the AND of the set of selfvalues and
                    # othervalues is 0 means that they don't share any id
                    return False
            
            # Now that we know they share ids, its time to compare ports
            return self.cport == other.cport and self.dport == other.dport
        
        # I can be compared against a DevicePlugin
        if isinstance(other, DevicePlugin):
            return (self.__remote_name__ == other.__remote_name__ and
                    self.cport == other.cport and self.dport == other.dport)
        
        # And I can also be compared against a dict (dbus)
        if not isinstance(other, dict):
            raise ValueError("Cannot reliably compare me with %s" % other)
        
        for k, v in self.__properties__.iteritems():
            try:
                if other[k] not in v:
                    return False
            except KeyError:
                return False
        
        # if we've arrived here means that all the __properties__ pairs are
        # satisfied, thus we've found the device. We are going to store its
        # udi and the parent's udi. The device's udi is going to be used to
        # get its children. The tipical 3G device will have 1-3 children
        # (one for each serial port). The parent's udi is also stored because
        # in some systems with python-dbus >= 0.8 the parent of an Option
        # GlobeTrotter 3G+ EMEA's children will be the cardbus driver udi
        # instead of the udi of the pci device itself.
        self.udi = other['info.udi']
        self.parent_udi = other['info.parent']
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def _get_my_children(self, device_props):
        children = []
        for device in device_props:
            try:
                if (device['info.parent'].startswith(self.udi) or
                        device['info.parent'].startswith(self.parent_udi)):
                    children.append(device)
            except KeyError:
                pass
        
        return children

    def patch(self, other):
        super(DBusDevicePlugin, self).patch(other)
        self.udi = other.udi


class RemoteDevicePlugin(DevicePlugin):
    """
    Base class from which all the RemoteDevicePlugins should inherit from
    """
    implements(IPlugin, interfaces.IRemoteDevicePlugin)


class UnknownDevicePlugin(DevicePlugin):
    """
    UnknownDevicePlugin
    """
    implements(IPlugin, interfaces.IRemoteDevicePlugin)


def get_unknown_device_plugin(dataport, controlport=None, baudrate=115200,
        name='Unknown Device', cached_id=None):
    """
    Returns a C{UnknownDevicePlugin} instance configured with the given params
    """
    from vmc.common.hardware.base import Customizer
    plugin = UnknownDevicePlugin()
    plugin.custom = Customizer()
    plugin.dport = dataport
    plugin.cport = controlport
    plugin.baudrate = baudrate
    plugin.name = name
    plugin.cached_id = cached_id
    def identify_device_cb(model):
        plugin.__remote_name__ = model
        return plugin

    from vmc.common.hardware.base import identify_device
    d = identify_device(plugin)
    d.addCallback(identify_device_cb)
    return d

class OSPlugin(object):
    """Base class from which all the OSPlugins should inherit from"""
    implements(IPlugin, interfaces.IOSPlugin)
    abstraction = BASE_PATH_DICT
    customization = None
    dialer = None
    os_name = None
    os_version = None
    manage_secrets = True
    privileges_needed = None
    
    def __init__(self):
        super(OSPlugin, self).__init__()
    
    def are_privileges_needed(self):
        """
        Sets C{self.privileges_needed} to True if pppd is suid
        
        This should take into account SELinux stuff
        """
        if app_is_frozen() or not os.geteuid():
            # if we're running the bundled version or we are root
            return False
        
        try:
            pppd_path = procutils.which('pppd')[0]
        except IndexError:
            pppd_path = join(TOP_DIR, 'usr', 'sbin', 'pppd')
        
        smode = os.stat(pppd_path)[stat.ST_MODE]
        mode = str(stat.S_IMODE(smode))
        return len(mode) != 4
    
    def get_timezone(self):
        raise NotImplementedError()
    
    def get_tzinfo(self):
        zone = self.get_timezone()
        try:
            return timezone(zone)
        except:
            # we're not catching this exception because some dated pytz
            # do not include UnknownTimeZoneError, if get_tzinfo doesn't works
            # we just return None as its a valid tzinfo and we can't do more
            return None
    
    def get_iface_stats(self, iface):
        raise NotImplementedError()
    
    def is_valid(self):
        raise NotImplementedError()

    def get_config_template(self, dialer_profile):
        return TEMPLATES_DICT[dialer_profile]
    
    def initialize(self):
        self.privileges_needed = self.are_privileges_needed()
        if self.customization:
            self.abstraction.update(self.customization)


class NotificationPlugin(object):
    """Base class from which all NotificationPlugins should inherit from"""
    implements(IPlugin, interfaces.INotificationPlugin)
    klass = None # reference to the class that we are interested in
    
    def __init__(self):
        super(NotificationPlugin, self).__init__()
    
    def on_notification_received(self, wrapper, notification):
        raise NotImplementedError()


import vmc.common.plugins
class PluginManager(object):
    """I manage VMCCdfL's plugins"""
    
    @classmethod
    def get_plugins(cls, interface=IPlugin, package=vmc.common.plugins):
        return getPlugins(interface, package)
    
    @classmethod
    def regenerate_cache(cls):
        log.msg("PluginManager: Regenerating plugin cache...")
        list(getPlugins(IPlugin, package=vmc.common.plugins))
    
    @classmethod
    def get_plugin_by_name(cls, name, interface=IPlugin):
        """Get a plugin by its name"""
        for plugin in cls.get_plugins(interface, vmc.common.plugins):
            try:
                if plugin.name == name:
                    return plugin
            
            except AttributeError:
                pass
        
        return None
    
    @classmethod
    def get_plugin_by_remote_name(cls, name,
                                  interface=interfaces.IDevicePlugin):
        """
        Get a plugin by its remote name
        
        @raise ex.UnknownPluginNameError: When we don't know about the plugin
        """
        for plugin in cls.get_plugins(interface, vmc.common.plugins):
            try:
                log.msg("PluginManager: trying plugin %s" % plugin.__remote_name__)
                if plugin.__remote_name__ == name:
                    log.msg("PluginManager: matched plugin %s with %s" % (plugin.__remote_name__ , name) )
                    return plugin
            
            except AttributeError:
                # if Plugin.__class__ != DevicePlugin, __remote_name__ not def
                pass
        
        raise ex.UnknownPluginNameError(name)

    @classmethod
    def get_plugin_by_vendor_product_id(cls, product_id, vendor_id):
        log.msg("get_plugin_by_id called with 0x%X and 0x%X" % (product_id,
                                                            vendor_id))
        for plugin in cls.get_plugins(interfaces.IDBusDevicePlugin):
            props = flatten_list(plugin.__properties__.values())
            if int(product_id) in props and int(vendor_id) in props:
                if not plugin.mapping:
                    # regular plugin
                    return plugin

                # device has multiple personalities...
                # this will just return the default plugin for
                # the mapping, we keep a reference to the mapping
                # once the device is properly identified by
                # vmc.common.hardware.base::identify_device
                _plugin = plugin.mapping['default']()
                _plugin.mapping = plugin.mapping
                return _plugin

        return None
