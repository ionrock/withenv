import time
import subprocess
import tempfile
import signal


from mock import patch, Mock

from withenv import cli


class TestMain(object):

    def parse_args():
        return Mock(actions=[], cmd='ls -la'.split())

    @patch.object(cli, 'parse_args', parse_args)
    @patch.object(cli.sys, 'exit')
    def test_main_calls_command(self, exit):
        cli.main()
        exit.assert_called_with(0)

    def test_we_return_code(self):
        assert subprocess.call('we echo'.split()) == 0
        assert subprocess.call('we eccho'.split()) == 127

    def test_we_catches_ctrl_c(self):
        fd, path = tempfile.mkstemp()
        with open(path, 'wb+') as fh:
            proc = subprocess.Popen(['we', 'sleep', '10'],
                                    stdout=fh,
                                    stderr=subprocess.STDOUT)
            time.sleep(.5)
            proc.send_signal(signal.SIGINT)
            proc.wait()

        assert open(path).read() == ''
