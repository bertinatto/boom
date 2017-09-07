# Copyright (C) 2017 Red Hat, Inc., Bryn M. Reeves <bmr@redhat.com>
#
# command_tests.py - Boom command API tests.
#
# This file is part of the boom project.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest
import logging
from sys import stdout
from os import listdir
from os.path import exists
from StringIO import StringIO

log = logging.getLogger()
log.level = logging.DEBUG
log.addHandler(logging.FileHandler("test.log"))

import boom
BOOT_ROOT_TEST = "./tests"
BOOM_ROOT_TEST = BOOT_ROOT_TEST + "/boom"
boom.BOOM_ROOT = BOOM_ROOT_TEST
boom.BOOT_ROOT = BOOT_ROOT_TEST

import boom.osprofile
import boom.bootloader
import boom.command

create_entry = boom.command.create_entry
delete_entries = boom.command.delete_entries
list_entries = boom.command.list_entries
print_entries = boom.command.print_entries

load_profiles = boom.osprofile.load_profiles

get_os_profile_by_id = boom.osprofile.get_os_profile_by_id

class CommandTests(unittest.TestCase):
    def test_list_entries(self):
        path = boom.bootloader.BOOT_ENTRIES_PATH
        nr = len([p for p in listdir(path) if p.endswith(".conf")])
        bes = boom.command.list_entries()
        self.assertTrue(len(bes), nr)

    def test_list_entries_match_machine_id(self):
        machine_id = "611f38fd887d41dea7eb3403b2730a76"
        path = boom.bootloader.BOOT_ENTRIES_PATH
        nr = len([p for p in listdir(path) if p.startswith(machine_id)])
        bes = boom.command.list_entries(machine_id=machine_id)
        self.assertTrue(len(bes), nr)

    def test_list_entries_match_version(self):
        version = "4.10.17-100.fc24"
        path = boom.bootloader.BOOT_ENTRIES_PATH
        nr = len([p for p in listdir(path) if version in p])
        bes = boom.command.list_entries(version=version)
        self.assertTrue(len(bes), nr)

    def test_create_entry_notitle(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")
        with self.assertRaises(ValueError) as cm:
            be = create_entry(None, "2.6.0", "ffffffff", "/dev/vg_hex/root",
                              lvm_root_lv="vg_hex/root", osprofile=osp)
 
    def test_create_entry_noversion(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")
        with self.assertRaises(ValueError) as cm:
            be = create_entry("ATITLE", None, "ffffffff", "/dev/vg_hex/root",
                              lvm_root_lv="vg_hex/root", osprofile=osp)
 
    def test_create_entry_nomachineid(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")
        with self.assertRaises(ValueError) as cm:
            be = create_entry("ATITLE", "2.6.0", "", "/dev/vg_hex/root",
                              lvm_root_lv="vg_hex/root", osprofile=osp)

    def test_create_entry_norootdevice(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")
        with self.assertRaises(ValueError) as cm:
            be = create_entry("ATITLE", "2.6.0", "ffffffff", None,
                              lvm_root_lv="vg_hex/root", osprofile=osp)

    def test_create_entry_noosprofile(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")
        with self.assertRaises(ValueError) as cm:
            be = create_entry("ATITLE", "2.6.0", "ffffffff", "/dev/vg_hex/root",
                              lvm_root_lv="vg_hex/root")

    def test_create_dupe(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")

        title = "Fedora (4.1.1-100.fc24.x86_64) 24 (Workstation Edition)"
        machine_id = "611f38fd887d41dea7eb3403b2730a76"
        version = "4.1.1-100.fc24"
        root_device = "/dev/sda5"
        btrfs_subvol_id = "23"

        with self.assertRaises(ValueError) as cm:
            create_entry(title, version, machine_id, root_device,
                         btrfs_subvol_id=btrfs_subvol_id, osprofile=osp)

    def test_create_delete_entry(self):
        # Fedora 24 (Workstation Edition)
        osp = get_os_profile_by_id("9cb53ddda889d6285fd9ab985a4c47025884999f")
        be = create_entry("ATITLE", "2.6.0", "ffffffff", "/dev/vg_hex/root",
                          lvm_root_lv="vg_hex/root", osprofile=osp)
        self.assertTrue(exists(be._entry_path))

        delete_entries(boot_id=be.boot_id)
        self.assertFalse(exists(be._entry_path))

    def test_delete_entries_no_matching_raises(self):
        with self.assertRaises(IndexError) as cm:
            delete_entries(boot_id="thereisnospoon")

    def test_print_entries_no_matching(self):
        xoutput = ("Boot ID      Title                        " + 
                   "                            Version                  \n")
        output = StringIO()
        print_entries(boot_id="thereisnoboot", out_file=output)
        self.assertEqual(output.getvalue(), xoutput)

    def test_print_entries_default_stdout(self):
        print_entries() 

    def test_print_entries_boot_id_filter(self):
        xoutput = ("Boot ID      Title                                 "
                   "                   Version                  \n"
                   "c629b1dbbbf9 Fedora (4.10.17-100.fc24.x86_64) 24 "
                   "(Workstation Edition 4.10.17-100.fc24         \n")
        output = StringIO()
        print_entries(boot_id="c629b1dbbbf9d461a9266d87f518e47c02c8adfe",
                      out_file=output)
        self.assertEqual(output.getvalue(), xoutput)

    def test_boom_main_noargs(self):
        argv = ['']
        boom.command.main(argv[1:])

# vim: set et ts=4 sw=4 :
