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
import os

import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp

import spack
from spack.util.executable import ProcessError, which
from spack.util.chroot import build_chroot_enviroment, remove_chroot_enviroment, run_command


_SPACK_UPSTREAM = 'https://github.com/llnl/spack'

description = "create a new installation of spack in another prefix"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-r', '--remote', action='store', dest='remote',
        help="name of the remote to bootstrap from", default='origin')
    subparser.add_argument(
        'prefix',
        help="names of prefix where we should install spack")
    subparser.add_argument(
        '--isolate', action='store_true', dest='isolate',
        help="isolate the bootstraped enviroment from the system")
    subparser.add_argument(
        '--cores', action='store', dest='cores',
        help="the amount of cores dedicated for the vm")
    subparser.add_argument(
        '--size', action='store', dest='size',
        help="the amount of threads dedicated for the vm")
    subparser.add_argument(
        '--memory', action='store', dest='memory',
        help="the amount of memory dedicated for the vm")
    subparser.add_argument(
        '--disk', action='store', dest='disk',
        help="the location for the vm to store the data")
    subparser.add_argument(
        '--iso', action='store', dest='iso',
        help="the iso to boot from")
    subparser.add_argument(
        '--username', action='store', dest='username',
        help="the iso to boot from")
    subparser.add_argument(
        '--password', action='store', dest='password',
        help="the iso to boot from")


def get_origin_info(remote):
    git_dir = join_path(spack.prefix, '.git')
    git = which('git', required=True)
    try:
        branch = git('symbolic-ref', '--short', 'HEAD', output=str)
    except ProcessError:
        branch = 'develop'
        tty.warn('No branch found; using default branch: %s' % branch)
    if remote == 'origin' and \
       branch not in ('master', 'develop'):
        branch = 'develop'
        tty.warn('Unknown branch found; using default branch: %s' % branch)
    try:
        origin_url = git(
            '--git-dir=%s' % git_dir,
            'config', '--get', 'remote.%s.url' % remote,
            output=str)
    except ProcessError:
        origin_url = _SPACK_UPSTREAM
        tty.warn('No git repository found; '
                 'using default upstream URL: %s' % origin_url)
    return (origin_url.strip(), branch.strip())

def adapt_config(install_dir):
    etc_path = join_path(install_dir, "etc")
    config_path = join_path(etc_path, "spack")

    # Add the boostrap file to the config list
    spack.config.ConfigScope('bootstrap', config_path)
    config = spack.config.get_config("config", "bootstrap")

    #write to the config
    config['isolate'] = True
    spack.config.update_config("config", config, "bootstrap")

def bootstrap(parser, args):
    origin_url, branch = "https://github.com/TheTimmy/spack", "features/bootstrap-vm" #get_origin_info(args.remote)
    prefix = args.prefix
    isolate = args.isolate

    username = args.username
    password = args.password

    cores = args.cores
    size = args.size
    memory = args.memory
    iso = args.iso

    tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))

    if os.path.isfile(prefix):
        tty.die("There is already a file at %s" % prefix)

    if isolate:
        #generate and remove enviroment
        build_chroot_enviroment(cores, memory, prefix, size, iso)

        # copy the files via git to /home/spack in the vm
        run_command(username,
                    'mkdir -p $HOME/spack'
                    'cd $HOME/spack',
                    'git init --shared -q',
                    'git remote add origin {0}'.format(origin_url),
                    'git fetch origin {0}:refs/remotes/origin/{0} -n -q'.format(branch),
                    'git reset --hard origin/{0} -q'.format(branch),
                    'git checkout -B {0} origin/{0} -q'.format(branch))
    else:
        install_dir = prefix

        if os.path.exists(join_path(install_dir, '.git')):
            tty.die("There already seems to be a git repository in %s" % prefix)

        files_in_the_way = os.listdir(install_dir)
        if files_in_the_way:
            tty.die("There are already files there! "
                    "Delete these files before boostrapping spack.",
                    *files_in_the_way)

        tty.msg("Installing:",
                "%s/bin/spack" % install_dir,
                "%s/lib/spack/..." % install_dir)

        os.chdir(install_dir)
        git = which('git', required=True)
        git('init', '--shared', '-q')
        git('remote', 'add', 'origin', origin_url)
        git('fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch),
                               '-n', '-q')
        git('reset', '--hard', 'origin/%s' % branch, '-q')
        git('checkout', '-B', branch, 'origin/%s' % branch, '-q')

    tty.msg("Successfully created a new spack in %s" % prefix,
            "Run %s/bin/spack to use this installation." % prefix)
