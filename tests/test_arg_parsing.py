import pytest

from withenv.args import parse_args


class TestArgParsing(object):
    def test_defaults(self):
        args = parse_args([])
        assert args.actions is None
        assert args.cmd == []

    def test_mixed_long_with_cmd(self):
        actions = [
            ('file', 'foo.yml'),
            ('file', 'bar.yml'),
            ('directory', 'baz'),
        ]
        cmd = 'ls -la'.split()

        result = parse_args([
            '-e', 'foo.yml',
            '--env', 'bar.yml',
            '-d', 'baz',
            'ls', '-la'
        ])

        assert result.actions == actions
        assert result.cmd == cmd
