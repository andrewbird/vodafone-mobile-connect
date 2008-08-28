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
This module generates Vodafone Mobile Connect Card driver for Linux's .deb
"""
__version__ = "$Rev: 1189 $"

###################
# it is meant to be executed at the root of the package
# python admin/produce_deb.py [ubuntu | fedora | opensuse]
##################

import os
import sys

from twisted.python.release import sh

def get_temp_dir():
    import tempfile
    return tempfile.mkdtemp('', 'VMC', '/tmp')

def get_svn_revision():
    stdout = os.popen2("svn info | grep Revision | awk '{print $2}'")[1]
    result = stdout.read().strip('\n')
    stdout.close()
    return result

def get_vmc_version():
    cmd = "grep APP_VERSION vmc/common/consts.py | awk '{print $3}'"
    stdout = os.popen2(cmd)[1]
    result = stdout.read().strip('\n').strip("'")
    stdout.close()
    return result

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
                'projname' : 'vodafone-mobile-connect-card-driver-for-linux',
                'path' : path}
       )

def produce_source(arch):
    tmp_dir = get_temp_dir()
    version = get_vmc_version()
    pkg_name = "vodafone-mobile-connect-card-driver-for-linux-%s" % version
    final_path = os.path.join(tmp_dir, pkg_name)
    sh("cp -RL %s %s" % (os.getcwd(), final_path))
    sh("cp -R %s/po %s/resources/" % (os.getcwd(), final_path))
    sh("cp -R %s/desktop %s/resources/" % (os.getcwd(), final_path))
    sh("cp %s/consts_prefix.py %s/vmc/common/" % (os.getcwd(), final_path))

    sh('find %s -name ".svn" | xargs rm -rf' % final_path)
    sh('find %s -name ".pyc" | xargs rm -rf' % final_path)
    sh('find %s -name "~" | xargs rm -rf' % final_path)
    img_to_patch_path = os.path.join(final_path, 'resources', 'glade',
                                     'splash.png')
    paint_file(img_to_patch_path, '%s' % version)
    sh('rm -rf %s/po %s/desktop %s/consts_prefix.py' % (final_path, final_path, final_path))
    sh('rm -rf %s/resources/extra/*ttf' % final_path)
    sh('rm -rf %s/resources/extra/*xcf' % final_path)
    sh('rm -rf %s/rpm' % final_path)
    sh('rm -rf %s/vmc/common/consts-dev.py' % final_path)

    guide_path = os.path.join(final_path, 'doc', 'guide', 'devel')
    # generate devel doc
    produce_devel_doc(final_path, guide_path)
    produce_api_doc(guide_path)
    # generate user doc
    sh('make -C %s/doc/install html' % final_path)
    sh('make -C %s/doc/user html' % final_path)
    # targz it
    final_name = os.path.basename(final_path)
    sh('cd %s; tar czvf %s.tar.gz %s; cd -' % (tmp_dir, final_name, final_name))
    sh('cd %s; dpkg-buildpackage -rfakeroot -a%s; cd -' % (final_path, arch))
    print "The generated files are in %s" % tmp_dir
    return tmp_dir

def paint_file(path, text):
    print path
    from PIL import Image, ImageFont, ImageDraw
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("resources/extra/FreeSans.ttf", 20)
    draw.text((50, 30), text, font=font)
    im.save(path)
    
if __name__ == '__main__':
    try:
        distro = sys.argv[1]
    except IndexError:
        distro = 'ubuntu'

    try:
        arch = sys.argv[2]
    except IndexError:
        arch = 'i386'

    distros = ['ubuntu', 'fedora', 'opensuse']
    archs = ['i386', 'amd64']
    if distro in distros and arch in archs:
        sh('ln -fs postinst.%s debian/postinst' % distro)
        sh('ln -fs prerm.%s debian/prerm' % distro)
        tmp_dir = produce_source(arch)
        vmc_version = get_vmc_version()
        ###########
        # PREPARE #
        ###########
        sh('rm -rf ../build/*')
        sh('cp admin/install-%s.sh ../build/' % distro)
        if distro != 'ubuntu':
            sh('cd ../build/; sudo alien %s/vodafone-mobile-connect-card-driver-for-linux_%s_%s.deb --to-rpm --scripts; cd -' % (tmp_dir, vmc_version, arch))
            if distro == 'opensuse':
                sh('cp ../opensuse-deps/* ../build/')
        else:
            sh('cp %s/vodafone-mobile-connect-card-driver-for-linux_%s_%s.deb ../build/' % (tmp_dir, vmc_version, arch))
        #########
        # BUILD #
        #########
        sh('cd ..; makeself build vodafone-mobile-connect-card-driver-for-linux-%s-%s-%s-installer.run vmccdfl-%s ./install-%s.sh; cd -' % (vmc_version, distro, arch, vmc_version, distro))
    else:
        if arch in archs:
            print 'Error, distribution "%s" not yet supported' % (distro)
            print 'Choose one of %s' % str(distros)
        else:
            print 'Error, architecture "%s" not yet supported' % arch
            print 'Choose one of %s' % str(archs)
