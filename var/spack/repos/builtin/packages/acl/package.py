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
#     spack install acl
#
# You can edit this file again by typing:
#
#     spack edit acl
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Acl(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.linuxfromscratch.org/blfs/view/7.5/postlfs/acl.html"
    url      = "http://download.savannah.gnu.org/releases/acl/acl-2.2.52.src.tar.gz"

    version('2.2.52', 'a61415312426e9c2212bd7dc7929abda')
    version('2.2.51', '3fc0ce99dc5253bdcce4c9cd437bc267')
    version('2.2.50', '4917495f155260c552d9fcff63769a98')
    version('2.2.49', '181445894cca986da9ae0099d5ce2d08')
    version('2.2.48', '6ed035f4b7dffc7de5ef871f86a5cab8')

    # Use autotools to create the package
    depends_on('attr')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def configure_args(self):
        args = []
        return args

    def install(self, spec, prefix):
        make('install')
        make('install-dev')
        make('install-lib')
