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
"""Linpus OSPlugin"""
__version__ = "$Rev: 1172 $"

import re

from vmc.common.oses import LinuxPlugin

DEFAULT_TEMPLATE = """
debug
noauth
name wvdial
# no replacedefaultroute on Fedora / Linpus use ip-up instead
ipparam vmc
noipdefault
nomagic
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



class LinpusBasedDistro(LinuxPlugin):
    os_name = re.compile('Linpus')
    os_version = None

    def get_config_template(self, dialer_profile):
	return TEMPLATES_DICT[dialer_profile]


linpus = LinpusBasedDistro()
