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
import re
import os
import sys
import copy
import spack
import subprocess
import llnl.util.tty as tty
from itertools import product
from spack.util.executable import which
from llnl.util.filesystem import join_path, mkdirp


def mount_bind_path(realpath, chrootpath):
    mount = True
    if os.path.isfile(realpath):
        if not os.path.exists(os.path.dirname(chrootpath)):
            os.makedirs(os.path.dirname(chrootpath))

        if not os.path.exists(chrootpath):
            with open(chrootpath, "w") as out:
                pass
    else:
        # Don't include empty directories
        if os.listdir(realpath):
            if not os.path.exists(chrootpath):
                os.makedirs(chrootpath)
        else:
            mount = False

    if mount:
        os.system ("sudo mount --bind %s %s" % (realpath, chrootpath))

def umount_bind_path(chrootpath):
    # Don't unmount no existing directories
    if os.path.exists(chrootpath):
        os.system ("sudo umount -l %s" % (chrootpath))

def build_chroot_enviroment(cores, memory, disk, size, iso):
    # use virt-install to handle the installation and to provide a
    # setup screen for the user. alternatively this could be done here
    return
    install = which('virt-install')
    install('--virt-type=kvm',
            '--name=Spack-VM',
            '--ram={0}'.format(memory),
            '--vcpus={0}'.format(cores),
            '--hvm',
            '--cdrom={0}'.format(iso),
            '--network=default',
            '--disk',
            'path={0}.qcow2,size={1},bus=virtio,format=qcow2'.format(disk, size))
    tty.msg("successfully created the bootstrap environment")

def remove_chroot_enviroment(dir):
    pass

def run_command(username, *commands):
    bash = which('virsh', required=True)
    grep = which('grep', required=True)
    arp = which('arp', required=True)
    ssh = which('ssh', required=True)

    vms = bash('domiflist', 'Spack-VM', output=str)
    mac = re.search(r'(([0-9a-f]{2}:){5}[0-9a-f]{2})', vms).group(0)
    ips = arp('-en', output=str)
    ip = re.search(r'(([0-9]{3}\.){3}([0-9]{2}))\s+\w+\s+' + mac, ips).group(1)

    command = ' && '.join([str(x) for x in commands])
    ssh('-t', '{0}@{1}'.format(username, ip), command)

def isolate_enviroment(username, password):
    tty.msg("Isolate spack")
    run_command(username, password, '/home/spack/bin/spack {0}'.format(sys.argv[1:]))
