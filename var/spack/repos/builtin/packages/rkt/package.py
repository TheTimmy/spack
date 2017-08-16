##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install rkt
#
# You can edit this file again by typing:
#
#     spack edit rkt
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Rkt(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/rkt"
    url      = "https://github.com/rkt/rkt/archive/master.zip"
    do_checksum = False

    version('1.0.0', git='https://github.com/rkt/rkt.git', branch='master')

    depends_on('git')
    depends_on('go')
    depends_on('acl')
    depends_on('zlib')
    depends_on('glib')
    depends_on('pkg-config')
    depends_on('ruby')
    depends_on('pixman')
    depends_on('gettext')
    depends_on('libcap')
    depends_on('openssl')

    # Use autotools to create the package
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def configure_args(self):
        args = [
            '--disable-functional-tests',
            '--with-stage1-flavors=kvm,fly',
            '--enable-tpm=no',
            '--enable-sdjournal=no'
        ]
        return args

    def build(self, spec, prefix):
        make('V=2')
