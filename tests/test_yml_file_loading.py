import os

from withenv.cli import find_yml_in_dir


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
