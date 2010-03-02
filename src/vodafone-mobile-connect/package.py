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

    import re

    def list_core_files(path, pattern):
        result = []
        def walk_callback(arg, directory, files):
            if '.svn' in files:
                files.remove('.svn')

            for file in files:
                if os.path.isdir(os.path.join(directory, file)):
                    continue
                m = re.search(pattern, file)
                if m:
                    result.append(os.path.join(directory, file))

        os.path.walk(path, walk_callback, None)
        return result

    def list_data_files(path):
        result = []
        def walk_callback(arg, directory, files):
            if '.svn' in files:
                files.remove('.svn')
            result.extend(os.path.join(directory, file) for file in files
                          if not os.path.isdir(os.path.join(directory, file)))

        os.path.walk(path, walk_callback, None)
        return result

    core_files = [
        (get_vmc_data_dir(), list_core_files('vmc','.+\.py\Z')),
    ]

    data_files = [

# Plugins
        (os.path.join(get_vmc_data_dir(), 'plugins', 'os'), list_data_files('plugins/os')),
        (os.path.join(get_vmc_data_dir(), 'plugins', 'devices'), list_data_files('plugins/devices')),
        (os.path.join(get_vmc_data_dir(), 'plugins', 'notifications'), list_data_files('plugins/notifications')),

# Resources
        (os.path.join(get_vmc_resources_dir(), 'extra'), list_data_files('resources/extra')),
        (os.path.join(get_vmc_resources_dir(), 'glade'), list_data_files('resources/glade')),
        (os.path.join(get_vmc_resources_dir(), 'templates'), list_data_files('resources/templates')),

# Data
        (get_vmc_data_dir(), ['gtk-tap.py']),

# Icon
        ('/usr/share/applications', ['resources/desktop/vmc.desktop']),
        ('/usr/share/pixmaps', ['resources/desktop/vodafone.png']),

# Doc
        (get_vmc_doc_dir(), ['debian/copyright', 'README', 'README-fr'] + glob('LICENSE*')),

# Bin
        (get_vmc_bin_dir(), glob('bin/*')),
    ]

# echo "%_unpackaged_files_terminate_build 0" >> /etc/rpm/macros

# Install core and data files
    for dst, src in core_files:
        sh("mkdir -p %s%s" % (root, dst))
        for file in src:
            (directory,a,b) = file.rpartition('/')

            dstdir="%s%s/%s" % (root, dst, directory)

            if not os.path.exists(dstdir):
                sh("mkdir -p %s" % dstdir)
            
            sh("cp -p %s %s/." % (file, dstdir))

    for dst, src in data_files:
        sh("mkdir -p %s%s" % (root, dst))
        for file in src:
            dstdir="%s%s" % ( root, dst )
            sh("cp -p %s %s/." % ( file, dstdir ))

# Splashscreen - apply version
    img_to_patch_path = "%s%s" % (root, os.path.join(get_vmc_resources_dir(), 'glade', 'splash.png'))
    paint_file(img_to_patch_path, '%s' % version)

# Remove developer overrides
    sh('rm -f %s/vmc/common/consts-dev.py' % root)

# Generate user doc
# Mandriva Free 2010 rpm package building fails to generate documentation so this two lines need to be commented.
    sh('tar -cf - doc/user | (cd %s && tar -xf -)' % tmp)
    sh('(cd %s/doc/user && make -f Makefile.pkg ROOT=../../%s-%s/%s/guide)' % (tmp, name, version,get_vmc_doc_dir())) 

# Apply platform specific overrides
    sh('(cd resources/platform/%s && tar -cf - . --exclude=./debian) | (cd %s && tar -xf -)' % (target, root))

# I18N
    sh('(cd resources && tar -cf - po glade) | (cd %s && tar -xf -)' % tmp)
    sh('(cd %s/po && make install ROOT=../%s-%s/ VERSION=%s)' % (tmp, name, version, version)) 

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

# if we have a platform/debian directory we must be building for a DEB based distro
    if os.path.exists('resources/platform/%s/debian' % target):
        # copy it
        sh('(cd resources/platform/%s && tar -cf - debian) | (cd %s && tar -xf -)' % (target, tmp))

    	changelog='%s/debian/changelog' % tmp
        sh("sed -i %s -e 's,name,%s,' -e 's,version,%s,' -e 's,release,%s,'" % (changelog,name,version,release))

    	control='%s/debian/control' % tmp
        sh("sed -i %s -e 's,Source.*$,Source: %s,' -e 's,Package.*$,Package: %s,'" % (control,name,name))

	# compile all of the python objects
	import compileall
	compileall.compile_dir('%s/' % root, ddir='/', force=True)

# so make can find out the root directory
    f = open('%s/builddir' % tmp,'w')
    f.write('%s-%s' % (name,version))
    f.close()

################################# 


if __name__ == '__main__':
    produce_tree()
