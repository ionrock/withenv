import pytest

from withenv import cli


class TestArgParsing(object):
    def setup(self):
        self.result = {
            'cmd': [],
            'actions': []
        }

    def test_defaults(self):
        assert cli.parse_args([]) == self.result

    def test_mixed_long_with_cmd(self):
        self.result['actions'] = [
            (cli.update_env_from_file, 'foo.yml'),
            (cli.update_env_from_file, 'bar.yml'),
            (cli.update_env_from_dir, 'baz'),
        ]
        self.result['cmd'] = ['ls', '-la']
        args = [
            '-e', 'foo.yml',
            '--environment', 'bar.yml',
            '-d', 'baz',
            'ls', '-la'
        ]
        assert cli.parse_args(args) == self.result
