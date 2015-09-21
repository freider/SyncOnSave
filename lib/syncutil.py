from __future__ import print_function  # for Python 2.x/SublimeText 2
import subprocess
import sys
import os

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


def get_trigger_file_path(bottom_dir):
    """
    :bottom_dir: directory or file where to start search
                 for sync definition file

    """
    test_dir = bottom_dir

    while test_dir != '/':
        for test_trigger in TRIGGER_FILES:
            test_file = os.path.join(test_dir, test_trigger)
            debug("Testing " + test_file)
            if os.path.exists(test_file):
                return test_file
        test_dir = os.path.dirname(test_dir)


def sync_dir(local_dir, remote_location):
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
    return status


def parse_trigger_file(tfile):
    for line in tfile:
        remote_location = line.strip()
        if remote_location:
            yield remote_location


def trigger_from_dir(dirpath):
    current_dir = dirpath
    trigger_file_path = get_trigger_file_path(dirpath)
    if trigger_file_path is None:
        debug("No trigger file matching names in {}".format(TRIGGER_FILES))
        return
    debug("Using {0}".format(trigger_file_path))

    with open(trigger_file_path) as f:
        for remote_location in parse_trigger_file(f):
            debug("Uploading {0} to {1}".format(current_dir, remote_location))
            sync_dir(current_dir, remote_location)

if __name__ == "__main__":
    trigger_from_dir(os.getcwd())
