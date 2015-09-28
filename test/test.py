from unittest import TestCase
import mock
from synconsave_lib import syncutil
import subprocess
from StringIO import StringIO


def make_true_if(true_if_val):
    def true_if(val):
        return val == true_if_val
    return true_if


class TestTriggerFilePath(TestCase):
    @mock.patch('os.path.exists', new=make_true_if("/foo/bar/.sync"))
    def test_in_dir(self):
        tfp = syncutil.get_trigger_file_path("/foo/bar")
        self.assertEquals(tfp, "/foo/bar/.sync")

    @mock.patch('os.path.exists', new=make_true_if("/foo/bar/.sync"))
    def test_grandparent(self):
        tfp = syncutil.get_trigger_file_path("/foo/bar/baz/boo")
        self.assertEquals(tfp, "/foo/bar/.sync")

    @mock.patch('os.path.exists', return_value=False)
    def test_none(self, mock_exists):
        tfp = syncutil.get_trigger_file_path("/foo/bar/baz/boo")
        self.assertEquals(tfp, None)


def fake_process(status):
    p = mock.MagicMock()
    p.wait = mock.MagicMock(return_value=status)
    p.stdout = []
    return p


class TestSyncDir(TestCase):
    @mock.patch('subprocess.Popen', return_value=fake_process(0))
    def test_simple(self, Popen):
        syncutil.sync_dir("FROM", "TO")
        Popen.assert_called_once_with([
            'rsync', '-av', '--delete', '--exclude',
            '*~', '--exclude', '.DS_Store', '--exclude',
            '.sync', 'FROM', 'TO'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class TestParseTriggerFile(TestCase):
    def test_two(self):
        fakefile = StringIO(
            "my.remote.host:homedirsubfolder\n"
            "my.other.host:other\n"
        )
        res = syncutil.parse_trigger_file(fakefile)
        self.assertEqual(
            list(res),
            [
                "my.remote.host:homedirsubfolder",
                "my.other.host:other"
            ]
        )

    def test_no_trailing_newline(self):
        fakefile = StringIO(
            "my.remote.host:homedirsubfolder\n"
            "my.other.host:other"
        )
        res = syncutil.parse_trigger_file(fakefile)
        self.assertEqual(
            list(res),
            [
                "my.remote.host:homedirsubfolder",
                "my.other.host:other"
            ]
        )
