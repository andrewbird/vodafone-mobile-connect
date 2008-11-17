# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007  Vodafone España, S.A.
# Author:  Pablo Martí
#          Andrew Bird
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
This module generates Vodafone Mobile Connect's .deb and rpm 
"""
__version__ = "$Rev: 1189 $"

###################
# it is meant to be executed at the root of the package
# python package.py
##################

import os
from glob import glob

from twisted.python.release import sh

def get_svn_revision():
    stdout = os.popen2("svn info | grep Revision | awk '{print $2}'")[1]
    result = stdout.read().strip('\n')
    stdout.close()
    return result

def get_vmc_name():
    from vmc.common.consts import APP_SLUG_NAME
    return APP_SLUG_NAME

def get_vmc_version():
    from vmc.common.consts import APP_VERSION
    return APP_VERSION

def get_vmc_bin_dir():
    from vmc.common.consts_prefix import TOP_DIR
    return os.path.join(TOP_DIR, 'usr', 'bin')

def get_vmc_data_dir():
    from vmc.common.consts import DATA_DIR
    return DATA_DIR

def get_vmc_resources_dir():
    from vmc.common.consts import RESOURCES_DIR
    return RESOURCES_DIR

def get_vmc_doc_dir():
    from vmc.common.consts_prefix import TOP_DIR
    return os.path.join(TOP_DIR, 'usr', 'share', 'doc', get_vmc_name())

def paint_file(path, text):
    print path
    from PIL import Image, ImageFont, ImageDraw
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("resources/tools/FreeSans.ttf", 12)
    draw.text((300, 0), text, font=font)
    im.save(path)
    
def produce_devel_doc(basepath, guidepath):
    TPL_PATH = os.path.join(basepath, 'doc', 'devel', 'template.tpl')
    DOC_DIR = os.path.join(basepath, 'doc', 'devel')
    IMAGES_DIR = os.path.join(basepath, 'doc', 'user', 'images')
    sh("lore --config template=%(tpl_path)s "
       "--config baseurl=api/%%s.html "
       "%(doc_dir)s/*.xhtml" % dict(doc_dir=DOC_DIR, tpl_path=TPL_PATH)
       )
    sh("cp %s/*.html doc/devel/*.css %s" % (DOC_DIR, guidepath))
    sh("cp -R %s %s/images" % (IMAGES_DIR, guidepath))

def produce_api_doc(path):
    os.system("pydoctor --system-class=%(sysclass)s "
       "--project-name=%(projname)s "
       "--html-output=%(path)s/api "
       "--make-html "
       "--add-package vmc" % \
               {'sysclass' : 'pydoctor.twistedmodel.TwistedSystem',
                # XXX: otherwise we'll just get "Vodafone"
                'projname' : get_app_name(),
                'path' : path}
       )

def produce_tree():
    name = get_vmc_name()
    version = get_vmc_version()

    target=os.getenv("TARGET")
    if target == None:
        target = "generic"

    release=os.getenv("RELEASE")
    if release == None:
        release = "1"

    tmp = "./tmp"
    nvr_triplet="%s-%s-%s" % (name,version,release)

    root = "%s/%s-%s" % (tmp, name, version)

    from setuptools import setup, find_packages

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

# Plugins
        (os.path.join(get_vmc_data_dir(), 'plugins', 'os'), list_files('plugins/os')),
        (os.path.join(get_vmc_data_dir(), 'plugins', 'devices'), list_files('plugins/devices')),
        (os.path.join(get_vmc_data_dir(), 'plugins', 'notifications'), list_files('plugins/notifications')),

# Resources
        (os.path.join(get_vmc_resources_dir(), 'extra'), list_files('resources/extra')),
        (os.path.join(get_vmc_resources_dir(), 'glade'), list_files('resources/glade')),
        (os.path.join(get_vmc_resources_dir(), 'templates'), list_files('resources/templates')),

# Data
        (get_vmc_data_dir(), ['gtk-tap.py']),

# Icon
        ('share/applications', ['resources/desktop/vmc.desktop']),
        ('share/pixmaps', ['resources/desktop/vodafone.png']),

# Doc
        (get_vmc_doc_dir(), ['debian/copyright', 'INSTALL', 'LICENSE', 'LICENSE.bsd', 'README']),

# Bin
        (get_vmc_bin_dir(), glob('bin/*')),
    ]

# echo "%_unpackaged_files_terminate_build 0" >> /etc/rpm/macros

    from sys import argv
    argv.append('--root=%s' % root)

    setup(name=name,
          version=version,
          packages=find_packages(),
          data_files=data_files,
          )

# Bin - patch paths
    sh("sed -i %s/usr/bin/vodafone-mobile-connect-card-driver-for-linux -e 's,vodafone-mobile-connect-card-driver-for-linux,%s,g'" % \
        (root, name) )
    sh("sed -i %s/usr/bin/vodafone-mobile-connect-card-driver-for-linux-debug -e 's,vodafone-mobile-connect-card-driver-for-linux,%s,g'" % \
        (root, name) )

# Splashscreen - apply version
    img_to_patch_path = "%s%s" % (root, os.path.join(get_vmc_resources_dir(), 'glade', 'splash.png'))
    paint_file(img_to_patch_path, '%s' % version)

# Remove developer overrides
    sh('rm -rf %s/vmc/common/consts-dev.py' % root)

# Generate devel doc
    #guide_path = os.path.join(root, 'doc', 'guide', 'devel')
    #produce_devel_doc(root, guide_path)
    #produce_api_doc(guide_path)

# Generate user doc
#    sh('make -C %s/doc/install html' % root)
#    sh('make -C %s/doc/user html' % root)

# Apply platform specific overrides
    sh('(cd resources/platform/%s && tar -cf - . --exclude=./debian) | (cd %s && tar -xf -)' % (target, root))
    sh('(cd resources/platform/%s && tar -cf - debian) | (cd %s && tar -xf -)' % (target, tmp))

# I18N
    sh('(cd resources && tar -cf - po) | (cd %s && tar -xf -)' % tmp)
    sh('(cd %s/po && make -f Makefile.pkg ROOT=../%s-%s/)' % (tmp, name, version)) 

# Remove any svn info in copy
    sh('find %s -name ".svn" | xargs rm -rf' % root)

# if we have an RPM spec file we must be building a bundle for an RPM based distro
    try:
    	specfile='%s/vmc.spec' % root
        os.stat(specfile)
        sh("sed -i %s -e 's,Name:.*$,Name:           %s,'" % (specfile,name))
        sh("sed -i %s -e 's,Version:.*$,Version:        %s,'" % (specfile,version))
        sh("sed -i %s -e 's,Release:.*$,Release:        %s,'" % (specfile,release))
        sh("sed -i %s -e 's,Source0:.*$,Source0:        %s.tar.bz2,'" % (specfile,nvr_triplet))

# remove any precompiled objects - rpm's smart enough to build them
        sh('find %s -name "*.pyc" | xargs rm -rf' % root)
        sh('find %s -name "*.pyo" | xargs rm -rf' % root)

        sh('(cd %s && tar -jcvf %s.tar.bz2 %s-%s)' % (tmp,nvr_triplet,name,version))
    except:
        pass

# if we have a debian changelog we must be building for a DEB based distro
    try:
    	changelog='%s/debian/changelog' % tmp
        os.stat(changelog)
        sh("sed -i %s -e 's,name,%s,' -e 's,version,%s,' -e 's,release,%s,'" % (changelog,name,version,release))

    	control='%s/debian/control' % tmp
        os.stat(control)
        sh("sed -i %s -e 's,Source.*$,Source: %s,' -e 's,Package.*$,Package: %s,'" % (control,name,name))

# so make can find out the root directory
	f = open('%s/builddir' % tmp,'w')
	f.write('%s-%s' % (name,version))
	f.close()
    except:
        pass
    


################################# 


if __name__ == '__main__':
    produce_tree()