#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009  Vodafone España, S.A.
# Author:  Vicente Hernando
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
Command line program that adds one or some users to necessary groups 
so they can execute vodafone-mobile-connect program
"""

import sys
import os   
import shutil

sys.path.insert(1,'/usr/share/vodafone-mobile-connect')

from twisted.python import log   # will show log messages.
from twisted.python import usage # parses command line options.
from twisted.python.procutils import which

from vmc.common.startup import create_skeleton_and_do_initial_setup

from vmc.common.exceptions import OSNotRegisteredError
from vmc.common.consts import APP_LONG_NAME
import vmc.common.consts as consts

from vmc.common.plugin import PluginManager
from vmc.common.interfaces import IOSPlugin
from vmc.utils.utilities import extract_lsb_info  # Obtains distribution info

# Obtains current distribution name and version.
os_info = extract_lsb_info()

LOCK = os.path.join(consts.VMC_HOME, '.setup-done')

def get_groups():
    for osplugin in PluginManager.get_plugins(IOSPlugin):
        try:
            if osplugin.os_name.match(os_info['os_name']):
                if osplugin.os_version:
                    if osplugin.os_version.match(os_info['os_version']):
                        log.msg('osplugin: %s' % (osplugin.__class__))
                        return osplugin.os_groups
                    else:
                        # Version doesn't match.
                        pass
                else:
                    # No version specified.
                    log.msg('osplugin: %s' % (osplugin.__class__))
                    return osplugin.os_groups
            else:
                # Distro name doesn't match.
                pass
        except KeyError:
            pass

    # No matching os plugin found.
    message = 'OS/Distro not registered'
    details = """
The OS/Distro under which you are running %s
is not registered in the OS database. Check the common.oal module for what
you can do in order to support your OS/Distro
""" % APP_LONG_NAME
    #    dialogs.open_warning_dialog(message, details)
    log.msg('%s %s' % (message, details))
    raise OSNotRegisteredError


class Options(usage.Options):
    """
    Parsing command line options.
    """
    def __init__(self):
        usage.Options.__init__(self)
        self['user_list'] = []

    optParameters = [["user", "u", None, "The user name"]]

    def opt_user(self, symbol):
        self['user_list'].append(symbol)

    opt_u = opt_user



def initial_setup():
    
    if os.path.exists(LOCK):
        return
    
    try:
        shutil.rmtree(consts.VMC_HOME, True)
        os.mkdir(consts.VMC_HOME)
    except OSError, e:
        pass
    
    # copy plugins to plugins dir
    shutil.copytree(consts.PLUGINS_DIR, consts.PLUGINS_HOME)


def final_setup():

    if os.path.exists(LOCK):
        return

    try:
        shutil.rmtree(consts.VMC_HOME, True)
    except OSError, e:
        pass

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg('Log started')

    # Obtains user id and checks for root privileges.
    uid = os.getuid()
    log.msg('getuid: %s' % uid)
    if uid != 0:
        log.msg('Sorry you need root privileges to execute this program.')
        sys.exit()

    # Parses command line.
    config = Options()
    try:
        config.parseOptions() # When given no argument, parses sys.argv[1:]
    except usage.UsageError, errortext:
        print '%s: %s' % (sys.argv[0], errortext)
        print '%s: Try --help for usage details.' % (sys.argv[0])
        sys.exit(1)

 
    # Hacked version of create_skeleton_and_do_initial_setup()
    initial_setup()

    distro_groups = get_groups()
    log.msg('distro_groups: %s' % distro_groups)
    if distro_groups == None:
        log.msg('There are no groups selected for this distro')
        sys.exit()


    # Obtain a list with users to be added to groups.
    if config['user_list'] == [] :
        log.msg("There are no users to be added")
        log.msg('%s: Try --help for usage details.' % (sys.argv[0]))
        sys.exit(0)
    else:
        log.msg('Users to be added %s' % config['user_list'])
        
    # Parsing user_list for real users.
    import pwd
    parsed_user_list = []
    for username in config['user_list']:
        try:
            pwd.getpwnam(username)
            parsed_user_list.append(username)
        except KeyError:
            log.msg('Warning: %s is not a correct user' % username)

    useradd_command = which('usermod')
    if useradd_command == []:
        log.msg('Error: there is no usermod system command available')
        sys.exit(1)

    import grp
    for username in parsed_user_list:
        for group in distro_groups:
            group_info = grp.getgrnam(group)
            if username not in group_info.gr_mem:
                log.msg('Adding user: %s to group: %s' % (username, group))
                cmd = '%s -a -G %s %s' % (useradd_command[0], group, username)
                print 'cmd: %s' % cmd
                os.system(cmd)
            else:
                log.msg('user %s already in group %s' % (username, group))

    # Hacked version of create_skeleton_and_do_initial_setup()
    final_setup()

    log.msg('')
    log.msg('##################################################')
    log.msg('###############    IMPORTANT    ##################')
    log.msg('')
    log.msg('REMEMBER TO LOGIN AGAIN SO CHANGES WILL BE APPLIED')
    log.msg('##################################################')
