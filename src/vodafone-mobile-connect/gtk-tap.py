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
Starts Vodafone Mobile Connect driver for Linux

execute it with:  twistd -r gtk2 -noy gtk-tap.py
"""

import locale
import signal
import sys

sys.path.insert(1,'/usr/share/vodafone-mobile-connect')

from twisted.application.service import Application, IProcess

__version__ = "$Rev: 1172 $"

# i10n stuff
locale.setlocale(locale.LC_ALL, '')

from vmc.common.startup import (create_skeleton_and_do_initial_setup,
                                ensure_have_config)

# it will just return if its not necessary
create_skeleton_and_do_initial_setup()

# make sure we always have a config
ensure_have_config()

# we delays this imports as they depend on modules that in turn depend on
# stuff that depend on plugins. If we dont delay this imports after the
# initial setup is complete we would get a messy traceback
from vmc.gtk.startup import check_dependencies, GTKSerialService
from vmc.common import shell
from vmc.common.consts import APP_LONG_NAME, APP_SHORT_NAME, SSH_PORT
from vmc.gtk import dialogs
from vmc.common.encoding import _

probs = check_dependencies()
if probs:
    message = _('Missing dependencies')
    probtext = '\n'.join(probs)
    msg = _('The following dependencies are not satisfied:\n%s') % probtext
    dialogs.open_warning_dialog(message, msg)
    raise SystemExit()

# access osobj singleton
from vmc.common.exceptions import OSNotRegisteredError
try:
    from vmc.common.oal import osobj
except OSNotRegisteredError:
    message = _('OS/Distro not registered')
    details = """
The OS/Distro under which you are running %s
is not registered in the OS database. Check the common.oal module for what
you can do in order to support your OS/Distro
""" % APP_LONG_NAME
    dialogs.open_warning_dialog(message, details)
    raise SystemExit()

if osobj.manage_secrets:
    probs = osobj.check_permissions()
    if probs:
        message = _('Permissions problems')
        probtext = '\n'.join(probs)
        details = """
%s needs the following files and dirs with some specific permissions
in order to work properly:\n%s""" % (APP_LONG_NAME, probtext)
        dialogs.open_warning_dialog(message, details)
        raise SystemExit()

from vmc.common.shutdown import shutdown_core
signal.signal(signal.SIGINT, shutdown_core)

service = GTKSerialService()
application = Application(APP_SHORT_NAME)

# Enable only for debugging
#from twisted.application import strports
#factory = shell.getManholeFactory(globals(), admin='admin')
#strports.service(SSH_PORT, factory).setServiceParent(application)

# Causes reinitialisation and consequently double probing
# Disabling saves 2 secs on 2.2Ghz laptop and 8 secs on EeePC-701
#IProcess(application).processName = APP_SHORT_NAME

service.setServiceParent(application)
