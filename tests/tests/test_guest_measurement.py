#!/usr/bin/env python3
#
# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import time
import subprocess

import Qemu
from common import *

def test_guest_measurement_check_rtmr(qm):
    """
    Boot measurements check
    Run the tdrtmrcheck program in the guest
    The program will compare the RTMR values it gets:
    - from the report that is generated
    - from the event log entries
    The RTMR values should match
    """
    qm.run()

    m = Qemu.QemuSSH(qm)

    deploy_and_setup(m)

    m.check_exec('tdrtmrcheck')

    qm.stop()

def test_guest_measurement_kernel_args(qm):
    """
    If the kernel command line is changed, the RTMR value
    should be different
    """
    qm.run()
    m = Qemu.QemuSSH(qm)
    deploy_and_setup(m)

    report1 = get_report(m)

    add_earlyprintk_cmd = r'''
      sed -i -E "s/GRUB_CMDLINE_LINUX=\"(.*)\"/GRUB_CMDLINE_LINUX=\"\1 earlyprintk=ttyS0,115200\"/g" /etc/default/grub
      update-grub
      grub-install
    '''
    m.check_exec(add_earlyprintk_cmd)

    qm.reboot()
    m = Qemu.QemuSSH(qm)

    # verify the command line
    m.check_exec('grep earlyprintk=ttyS0,115200 /proc/cmdline')

    report2 = get_report(m)

    assert report1['td_info']['mrtd'] == report2['td_info']['mrtd']
    assert report1['td_info']['rtmr_0'] != report2['td_info']['rtmr_0']
    assert report1['td_info']['rtmr_1'] != report2['td_info']['rtmr_1']
    assert report1['td_info']['rtmr_2'] != report2['td_info']['rtmr_2']
    assert report1['td_info']['rtmr_3'] == report2['td_info']['rtmr_3']

    qm.stop()
