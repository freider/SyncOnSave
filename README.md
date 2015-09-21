SyncOnSave
==========

SublimeText 2/3 package for syncing working directory to a remote host/directory, making it easy to develop locally but run remotely.

Usage
-----
Add a name named ".sync" to the root of your project with one line per destination to replicate to in rsync syntax. For example:
remote.host:/path/to/base

Whenever you save, the directory containing the .sync file will be copied to the remote directory.
Note that this is a one-way sync and remote changes will be overridden.

To sync from outside of SublimeText, use the bin/syncpush command line utility. I recommend to symlinking it into somewhere on your $PATH.

Command line utility
--------------------
The syncpush command line utility is included to allow syncing from the terminal without using SublimeText.
Add a symlink to the executable using the following example snippet. This assumes you have a bin directory in your home directory which is on your PATH:

```
ln -s "~/Library/Application\ Support/Sublime\ Text\ 3/Packages/SyncOnSave/bin/syncpush" ~/bin/syncpush
chmod +x ~/bin/syncpush
```
