##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import argparse
import llnl.util.tty as tty
import spack
import spack.cmd
import os
from spack.util.executable import which
from llnl.util.filesystem import join_path, mkdirp
from spack.util.chroot import build_chroot_enviroment,  \
                              remove_chroot_enviroment, \
                              isolate_enviroment,       \
                              run_command

description = "starts an isolated bash session for spack"
section = "admin"
level = "long"

def setup_parser(subparser):
    subparser.add_argument(
        '--start-environment', action='store_true', dest='start_enviroment',
        help="start or generate a environment")
    subparser.add_argument(
        '--stop-environment', action='store_true', dest='stop_environment',
        help="stop the environment")
    subparser.add_argument(
        '--remove-environment', action='store_true', dest='remove_environment',
        help="delete the environment")
    subparser.add_argument(
        '--cli', action='store_true', dest='cli',
        help="connect to a bash session with a ssh client to the generated environment")
    subparser.add_argument(
        '--username', action='store', dest='username',
        help="the iso to boot from")

def isolate(parser, args):
    username = args.username
    if args.start_enviroment:
        tty.msg("Build bootstraped enviroment")
        virsh = which('virsh', required=True)
        virsh('start Spack-VM')

    if args.stop_environment:
        tty.msg("Stop bootstraped enviroment")
        virsh = which('virsh', required=True)
        virsh('start Spack-VM')

    if args.remove_environment:
        tty.msg("Remove bootstraped enviroment")
        remove_chroot_enviroment(spack.spack_bootstrap_root)

    if args.cli:
        tty.msg("Start bash session")
        run_command(username, 'bash')
