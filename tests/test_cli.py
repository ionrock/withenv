import subprocess

from mock import patch

from withenv import cli


class TestMain(object):

    def parse_args():
        return {
            'actions': [],
            'cmd': 'ls -la'.split(),
        }

    @patch.object(cli, 'parse_args', parse_args)
    @patch.object(cli.sys, 'exit')
    def test_main_calls_command(self, exit):
        cli.main()
        exit.assert_called_with(0)

    def test_we_return_code(self):
        assert subprocess.call('we echo'.split()) == 0
        assert subprocess.call('we eccho'.split()) == 127
