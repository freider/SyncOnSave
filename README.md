SyncOnSave
==========

SublimeText 2/3 package for syncing working directory to a remote host/directory, making it easy to develop locally but run remotely.

Usage
------------
Add a name named ".sync" to the root of your project with one line per destination to replicate to in rsync syntax. For example:
remote.host:/path/to/base

Whenever you save, the directory containing the .sync file will be copied to the remote directory.
Note that this is a one-way sync and remote changes will be overridden.
