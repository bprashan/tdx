#!/usr/bin/env python3
#
# Copyright 2024 Canonical Ltd.
# Authors:
# - Hector Cao <hector.cao@canonical.com>
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

import Qemu
import util
from common import *

def test_guest_report(qm):
    """
    Boot measurements check
    """
    qm.run()

    m = Qemu.QemuSSH(qm)

    deploy_and_setup(m)

    m.check_exec(f'python3 {guest_workdir}/tests/guest/test_tdreport.py')

    qm.stop()

def test_guest_report_2vms():
    """
    When we run 2 VMs
    The reports generated for these 2 VMs should be identical
    """
    qm1 = Qemu.QemuMachine()
    qm2 = Qemu.QemuMachine()

    with qm1, qm2:
        qm1.run()
        qm2.run()

        m1 = Qemu.QemuSSH(qm1)
        deploy_and_setup(m1)
        m2 = Qemu.QemuSSH(qm2)
        deploy_and_setup(m2)

        report1 = get_report(m1)
        report2 = get_report(m2)

        assert len(report1) > 0
        assert report1 == report2, f'The reports are not identical {report1} - {report2}'

        qm1.stop()
        qm2.stop()

def test_guest_report_reboot(qm):
    """
    The report after VM reboot should not be the same
    the field tee_info_hash should be different
    """
    qm.run()
    m = Qemu.QemuSSH(qm)
    deploy_and_setup(m)

    report1 = get_report(m)

    qm.reboot()
    m = Qemu.QemuSSH(qm)

    report2 = get_report(m)

    assert len(report1) > 0
    assert report1 == report2, f'The reports are not identical {report1} - {report2}'

    qm.stop()
