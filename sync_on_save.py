# Copyright 2013 Elias Freider

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function  # for Python 2.x/SublimeText 2
import sublime_plugin
import sublime

import subprocess
import os
import sys

# TODO: make the following globals into settings
TRIGGER_FILES = [
    '.sync',
]
EXCLUDE_PATTERNS = [
    '*~',
    '.DS_Store',
] + TRIGGER_FILES


def debug(message):
    print("SyncOnSave:", message, file=sys.stderr)


class SyncOnSave(sublime_plugin.EventListener):
    """Sync changes to remote machine/directory on save

    Uses rsync to sync to a remote machine. To specify what to sync where,
    put a ".sync" trigger file in the directory you want to sync.
    It must be the directory or some parent directory of your current
    working file. Upon saving any file within the directory with the
    trigger file, the directory containing the trigger file will be
    synced to all destinations listed in the trigger file as per
    rsync syntax e.g:

        my.remote.machine:/home/freider/proj
        192.168.0.12:/var/www
        /local/dir

    """
    def sync_working_dir(self, view):
        test_dir = view.file_name()
        trigger_file = None
        while test_dir != '/':
            for test_trigger in TRIGGER_FILES:
                test_file = os.path.join(test_dir, test_trigger)
                debug("Testing " + test_file)
                if os.path.exists(test_file):
                    trigger_file = test_file
                    break
            test_dir = os.path.dirname(test_dir)
        if not trigger_file:
            debug("No trigger file found in any parent directory")
            return
        debug("Found {0}".format(trigger_file))
        local_dir = os.path.dirname(trigger_file)
        with open(trigger_file) as f:
            for line in f:
                remote_location = line.strip()
                if not remote_location:
                    continue
                view.set_status(
                    "SyncOnSave",
                    "Uploading to {0}".format(remote_location)
                )
                cmd = ['rsync', '-av', '--delete']
                for pattern in EXCLUDE_PATTERNS:
                    cmd += ['--exclude', pattern]
                cmd += [local_dir, remote_location]
                print(cmd)
                p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
                for line in p.stdout:
                    debug(line.decode('utf8').rstrip('\n'))
                status = p.wait()
            if status:
                view.set_status("SyncOnSave", "Error on sync")
        # TODO: multiple destination status
        view.set_status("SyncOnSave", "Successfully synced")

    def on_post_save(self, view):
        # SublimeText 2.0 fallback
        if int(sublime.version()) < 3000:
            self.sync_working_dir(view)

    def on_post_save_async(self, view):
        # async is preferable
        if int(sublime.version()) >= 3000:
            self.sync_working_dir(view)

    def on_modified(self, view):
        view.set_status("SyncOnSave", "")  # clear sync status in status bar
