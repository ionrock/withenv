import pytest

from withenv.cli import parse_args


class TestArgParsing(object):
    def setup(self):
        self.result = {
            'cmd': [],
            'env_files': [],
            'env_dirs': [],
        }

    def test_defaults(self):
        assert parse_args([]) == self.result

    def test_single_short(self):
        self.result['env_files'].append('foo.yml')
        assert parse_args(['-e', 'foo.yml']) == self.result

    def test_single_long(self):
        self.result['env_files'].append('foo.yml')
        assert parse_args(['--environment', 'foo.yml']) == self.result

    def test_multi_short(self):
        self.result['env_files'] = ['foo.yml', 'bar.yml']

        args = [
            '-e', 'foo.yml',
            '-e', 'bar.yml',
        ]
        assert parse_args(args) == self.result

    def test_multi_long(self):
        self.result['env_files'] = ['foo.yml', 'bar.yml']
        args = [
            '--environment', 'foo.yml',
            '--environment', 'bar.yml',
        ]
        assert parse_args(args) == self.result

    def test_mixed_long(self):
        self.result['env_files'] = ['foo.yml', 'bar.yml', 'baz.yml']

        args = [
            '-e', 'foo.yml',
            '--environment', 'bar.yml',
            '-e', 'baz.yml',
        ]
        assert parse_args(args) == self.result

    def test_mixed_long_with_cmd(self):
        self.result['env_files'] = ['foo.yml', 'bar.yml', 'baz.yml']
        self.result['cmd'] = ['ls', '-la']
        args = [
            '-e', 'foo.yml',
            '--environment', 'bar.yml',
            '-e', 'baz.yml',
            'ls', '-la'
        ]
        assert parse_args(args) == self.result
