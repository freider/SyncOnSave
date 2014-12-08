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


import sublime_plugin
import sublime
import os
from syncutil import (
    get_trigger_file_path,
    debug,
    sync_dir,
    parse_trigger_file
)


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
        cur_file = view.file_name()
        trigger_file_path = get_trigger_file_path(cur_file)
        if not trigger_file_path:
            debug("No trigger file found in any parent directory")
            return
        debug("Found {0}".format(trigger_file_path))
        local_dir = os.path.dirname(trigger_file_path)

        with open(trigger_file_path) as f:
            for remote_location in parse_trigger_file(f):
                view.set_status(
                    "SyncOnSave",
                    "Uploading to {0}".format(remote_location)
                )
                status = sync_dir(local_dir, remote_location)
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
