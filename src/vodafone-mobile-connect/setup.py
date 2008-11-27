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
setuptools file for Vodafone Mobile Connect Card driver for Linux
"""

from glob import glob
import os

from ez_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages

from vmc.common.consts import (APP_VERSION, APP_LONG_NAME,
                               TOP_DIR, APP_SLUG_NAME)

BIN_DIR = os.path.join(TOP_DIR, 'usr', 'bin')
DATA_DIR = os.path.join(TOP_DIR, 'usr', 'share', '%s' % APP_SLUG_NAME)
RESOURCES = os.path.join(DATA_DIR, 'resources')

def list_files(path):
    result = []
    def walk_callback(arg, directory, files):
        if '.svn' in files:
            files.remove('.svn')
        result.extend(os.path.join(directory, file) for file in files
                      if not os.path.isdir(os.path.join(directory, file)))

    os.path.walk(path, walk_callback, None)
    return result

data_files = [
   (os.path.join(RESOURCES, 'glade'), list_files('resources/glade')),
   (os.path.join(RESOURCES, 'extra'), list_files('resources/extra')),
   (os.path.join(RESOURCES, 'templates'), list_files('resources/templates')),
   (os.path.join(DATA_DIR, 'plugins'), list_files('plugins')),
   ('share/applications', ['resources/desktop/vmc.desktop']),
   ('share/pixmaps', ['resources/desktop/vodafone.png']),
   (DATA_DIR, ['gtk-tap.py']),
   (BIN_DIR, glob('bin/*')),
]

setup(name=APP_LONG_NAME,
      version=APP_VERSION,
      description='3G device manager for Linux',
      download_url="http://www.betavine.net/web/linux_drivers",
      author='Pablo Martí Gamboa',
      author_email='pmarti@warp.es',
      license='GPL',
      packages=find_packages(),
      data_files=data_files,
      zip_safe=False,
      test_suite='vmc.test',
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Communications :: Telephony',
        ]
)
