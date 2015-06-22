import os

from withenv.env import find_yml_in_dir, compile


HERE = os.path.dirname(os.path.abspath(__file__))


class EnvInfo(object):

    def setup(self):
        self.env = os.path.join(HERE, 'envs', 'foo')
        self.base = os.path.join(HERE, 'envs', 'foo', 'default')
        self.env_files = [
            os.path.join(self.base, 'a.yml'),
            os.path.join(self.base, 'b.yaml'),
            os.path.join(self.base, 'c.yml'),
        ]


class TestFindYmlInDir(EnvInfo):

    def test_load_dir(self):
        base = os.path.join(HERE, 'envs', 'foo', 'default')
        result = list(find_yml_in_dir(self.env))
        assert result == self.env_files


class TestCompileEnv(EnvInfo):
    foo_env = {
        'A': 'True',
        'B': 'True',
        'C': 'True',
    }

    def test_compile_with_directory(self):
        actions = [('directory', self.env)]
        assert compile(actions, {}) == self.foo_env

    def test_compile_with_alias(self):
        actions = [('alias', os.path.join(HERE, 'envs', 'alias.yml'))]
        assert compile(actions, {}) == self.foo_env

    def test_compile_with_files(self):
        actions = [
            ('file', fname) for fname in self.env_files
        ]
        assert compile(actions, {}) == self.foo_env