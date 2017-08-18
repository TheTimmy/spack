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
from llnl.util.filesystem import join_path


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

def build_chroot_enviroment(cores, threads, memory, disk, iso):
    if os.path.ismount(dir):
        tty.die("The path is already a bootstraped enviroment")

    buildXMLString = """
<domain type="kvm">
    <name>Spack-VM</name>
    <cpu>
        <topology cores="{0}" sockets="1" threads="{1}" />
    </cpu>
    <uuid>Spack_VM-97b2-11e4-86bf-001e682ee78a</uuid>
    <memory unit="MB">{2}</memory>
    <currentMemory unit="MB">{2}</currentMemory>
    <os>
        <type>hvm</type>
        <boot dev="hd" />
    </os>
    <features>
        <acpi />
        <apic />
        <pae />
    </features>
    <clock offset="utc" />
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>restart</on_crash>
    <devices>
        <disk device="disk" type="file">
            <driver cache="none" name="qemu" type="raw" />
            <source file="{3}" />
            <target dev="hda" />
            <address bus="0" controller="0" target="0" type="drive" unit="0" />
        </disk>
        <disk device="cdrom" type="file">
            <source file="{4}" />
            <driver name="qemu" type="raw" />
            <target bus="ide" dev="hdc" />
            <readyonly />
            <address bus="1" controller="0" target="0" type="drive" unit="0" />
        </disk>
        <interface type="network">
            <source network="default" />
        </interface>
        <graphics port="-1" type="vnc" />
    </devices>
</domain>""".format(cores, threads, memory, disk, iso)

    connection = libvirt.open('qemu:///system')
    connection.defineXML(buildXMLString)
    connection.close()

def remove_chroot_enviroment(dir):
    connection = libvirt.open('qemu:///system')
    virtual_machine = connection.lookupByName("Spack-VM")
    virtual_machine.undefine()
    connection.close()

def run_command(username, password, commands):
    connection = libvirt.open('qemu:///system')
    virtual_machine = connection.lookupByName("Spack-VM")
    if virtual_machine == None:
        tty.die("Could not connect to the virtual machine")

    networkInterface = virtual_machine.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)

    ipAddress = None
    for (name, val) in networkInterface.iteritems():
        if val['addrs']:
            for ipaddr in val['addrs']:
                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                    ipAddress = ipaddr['addr']
                    break
        if ipAddress != None
            break

    if ipAddress == None:
        tty.die("Could not connect the the virtual machine")

    command = ' && '.join([str(x) for x in commands])

    ssh = which('ssh')
    ssh('-t', '-p {0}'.format(password), '{0}@{1}'.format(username, ipAddress), command)
    connection.close()

def isolate_enviroment(username, password):
    tty.msg("Isolate spack")

    run_command(username, password, '/home/spack/bin/spack {0}'.format(sys.argv[1:]))
