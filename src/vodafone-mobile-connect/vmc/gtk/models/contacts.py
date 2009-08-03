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
"""Contacts-related models"""

__version__ = "$Rev: 1172 $"

import gtk
from gobject import TYPE_STRING, TYPE_PYOBJECT, TYPE_BOOLEAN

from vmc.gtk import ListStoreModel
from vmc.common.phonebook import is_db_contact, is_evl_contact
from vmc.gtk.images import MOBILE_IMG, COMPUTER_IMG, EVOLUTION_IMG

class ContactsStoreModel(ListStoreModel):
    """Store Model for Contacts treeviews"""
    def __init__(self):
        super(ContactsStoreModel, self).__init__(gtk.gdk.Pixbuf,
                TYPE_STRING, TYPE_STRING, TYPE_PYOBJECT, TYPE_BOOLEAN)

    def add_contacts(self, contacts):
        """Adds C{contacts} to the store"""
        for contact in contacts:
            self.add_contact(contact)

    def add_contact(self, contact):
        """Adds C{contact} to the store"""
        if is_db_contact(contact):
            img = COMPUTER_IMG
        elif is_evl_contact(contact):
            img = EVOLUTION_IMG
        else:
            img = MOBILE_IMG
        self.append([img, contact.name, contact.number, contact, contact.writable])

