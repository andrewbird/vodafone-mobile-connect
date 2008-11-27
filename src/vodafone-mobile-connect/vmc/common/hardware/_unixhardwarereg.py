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
The hardware module manages device discovery via dbus/hal on Unix/Linux
"""
__version__ = "$Rev: 1172 $"

import serial

from twisted.internet import defer

from vmc.common.hardware._dbus import DbusComponent
from vmc.common.hardware.base import identify_device
from vmc.utils.utilities import extract_lsb_info, natsort

def probe_port(port):
    """
    Returns C{True} if C{port} works, otherwise returns C{False}
    """
    try:
        ser = serial.Serial(port, timeout=1)
        ser.write('AT+CGMR\r\n')
        if not ser.readlines():
            # Huawei E620 with driver option registers three serial
            # ports and the middle one wont raise any exception while
            # opening it even thou its a dummy port.
            return False

        return True
    except serial.SerialException:
        return False
    finally:
        ser.close()

def probe_ports(ports):
    """
    Returns a tuple of (data port, control port) out of C{ports}
    """
    dport = cport = None
    while ports:
        port = ports.pop(0)
        if probe_port(port):
            if not dport:
                # data port tends to the be the first one
                dport = port
            elif not cport:
                # control port the next one
                cport = port
                break

    return dport, cport

def extract_info(props):
    info = {}
    if 'usb.vendor_id' in props:
        info['usb_device.vendor_id'] = props['usb.vendor_id']
        info['usb_device.product_id'] = props['usb.product_id']
    elif 'usb_device.vendor_id' in props:
        info['usb_device.vendor_id'] = props['usb_device.vendor_id']
        info['usb_device.product_id'] = props['usb_device.product_id']
    elif 'pcmia.manf_id' in props:
        info['pcmcia.manf_id'] = props['pcmcia.manf_id']
        info['pcmcia.card_id'] = props['pcmcia.card_id']
    elif 'pci.vendor_id' in props:
        info['pci.vendor_id'] = props['pci.vendor_id']
        info['pci.product_id'] = props['pci.product_id']
    else:
        raise RuntimeError("Unknown bus for device %s" % props['info.udi'])

    return info


class HardwareRegistry(DbusComponent):
    """
    I find and configure devices on Linux

    I am resilient to ports assigned in unusual locations
    and devices sharing ids.
    """

    def __init__(self):
        super(HardwareRegistry, self).__init__()
        self.call_id = None
        self.os_info = extract_lsb_info()

    def get_devices(self):
        """
        Returns a list with all the devices present in the system

        List of deferreds of course
        """
        parent_udis = self._get_parent_udis()
        d = self._get_devices_from_udis(parent_udis)
        return d

    def _get_device_from_udi(self, udi):
        """
        Returns a device built out of the info extracted from C{udi}
        """
        info = self._get_info_from_udi(udi)
        ports = self._get_ports_from_udi(udi)
        device = self._get_device_from_info_and_ports(info, udi, ports)
        return device

    def _get_devices_from_udis(self, udis):
        """
        Returns a list of devices built out of the info extracted from C{udis}
        """
        unknown_devs = map(self._get_device_from_udi, udis)
        deferreds = map(identify_device, unknown_devs)
        return defer.gatherResults(deferreds)

    def _get_parent_udis(self):
        """
        Returns the root udi of all the devices with modem capabilities
        """
        return set(map(self._get_parent_udi,
                       self.manager.FindDeviceByCapability("modem")))

    def _get_parent_udi(self, udi):
        """
        Returns the absolute parent udi of C{udi}
        """
        ORIG = 'serial.originating_device'
        def get_parent(props):
            if ORIG in props:
                return props[ORIG]
            return props['info.parent']

        current_udi = udi
        while True:
            props = self.get_properties_from_udi(current_udi)
            try:
                info = extract_info(props)
                break
            except RuntimeError:
                current_udi = get_parent(props)

        # now that we have an id to lookup for, lets repeat the process till we
        # get another RuntimeError
        def find_out_if_contained(_info, props):
            """
            Returns C{True} if C{_info} values are contained in C{props}

            As hal likes to swap between usb.vendor_id and usb_device.vendor_id
            I have got a special case where I will retry
            """
            def compare_dicts(d1, d2):
                for key in d1:
                    try:
                        return d1[key] == d2[key]
                    except KeyError:
                        return False

            if compare_dicts(_info, props):
                # we got a straight map
                return True
            # hal likes to swap between usb_device.vendor_id and usb.vendor_id
            if 'usb_device.vendor_id' in _info:
                # our last chance, perhaps its swapped
                newinfo = {'usb.vendor_id' : _info['usb_device.vendor_id'],
                           'usb.product_id' : _info['usb_device.product_id']}
                return compare_dicts(newinfo, props)

            # the original compare_dicts failed, so return False
            return False

        last_udi = current_udi
        while True:
            props = self.get_properties_from_udi(current_udi)
            if not find_out_if_contained(info, props):
                break
            last_udi, current_udi = current_udi, get_parent(props)

        return last_udi

    def _get_info_from_udi(self, udi):
        # log.msg("Obtaining info from udi %s" % udi)
        return extract_info(self.get_properties_from_udi(udi))

    def _get_child_udis_from_udi(self, udi):
        """
        Returns the paths of C{udi} childs and the properties used
        """
        device_props = self.get_devices_properties()
        dev_udis = sorted(device_props.keys(), key=len)
        dev_udis2 = dev_udis[:]
        childs = []
        while dev_udis:
            _udi = dev_udis.pop()
            if _udi != udi and 'info.parent' in device_props[_udi]:
                par_udi = device_props[_udi]['info.parent']

                if par_udi == udi or par_udi in childs:
                    childs.append(_udi)

        while dev_udis2:
            _udi = dev_udis2.pop()
            if _udi != udi and 'info.parent' in device_props[_udi]:
                par_udi = device_props[_udi]['info.parent']

                if par_udi == udi or (par_udi in childs and
                                            _udi not in childs):
                    childs.append(_udi)

        return childs, device_props

    def _get_ports_from_udi(self, udi):
        """
        Returns all the ports that C{udi} has registered
        """
        childs, dp = self._get_child_udis_from_udi(udi)
        if not childs:
            raise RuntimeError("Couldn't find any child of device %s" % udi)

        ports = map(str, [dp[_udi]['serial.device']
                        for _udi in childs if 'serial.device' in dp[_udi]])
        natsort(ports)
        return ports

    def _get_device_from_info_and_ports(self, info, udi, ports):
        """
        Returns a C{DevicePlugin} out of C{info} and C{dport} and {cport}
        """
        from vmc.common.plugin import PluginManager
        plugin = PluginManager.get_plugin_by_vendor_product_id(*info.values())

        if plugin:
            # set its udi
            plugin.udi = udi
            dport, cport = probe_ports(ports)

            if not dport and not cport:
                # this shouldn't happen
                raise RuntimeError("No data port and no control port")

            plugin.cport, plugin.dport = cport, dport
            return plugin

        raise RuntimeError("Couldn't find a plugin with info %s" % info)

    def get_plugin_for_remote_dev(self, speed, dport, cport):
        from vmc.common.plugin import UnknownDevicePlugin
        from vmc.common.hardware.base import Customizer
        dev = UnknownDevicePlugin()
        dev.custom = Customizer()
        dev.dport, dev.cport, dev.baudrate = dport, cport, speed
        port = cport and cport or dport
        return identify_device(port)

