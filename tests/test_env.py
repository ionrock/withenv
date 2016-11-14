import os

from withenv.env import find_yml_in_dir, compile, compiled_value


HERE = os.path.dirname(os.path.abspath(__file__))


class EnvInfo(object):

    def envs_path(self, *tail):
        return os.path.join(HERE, 'envs', *tail)

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
        result = set(list(find_yml_in_dir(self.env)))
        assert result == set(self.env_files)


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

    def test_compile_with_empty_file(self):
        actions = [
            ('file', self.envs_path('empty.yml'))
        ]

        assert compile(actions, {}) == {}

    def test_compile_with_empty_alias(self):
        actions = [
            ('alias', self.envs_path('empty.yml'))
        ]
        assert compile(actions, {}) == {}

    def test_compile_with_overrides(self):
        actions = [
            ('directory', self.env),
            ('override', 'C=False'),
        ]

        assert compile(actions, {})['C'] == 'False'

    def test_compile_with_script(self):
        actions = [
            ('script', 'cat %s' % self.env_files[0]),
        ]

        assert compile(actions, {})['A'] == 'True'


class TestCompileValue(object):
    def setup(self):
        os.environ['MYTESTVAR'] = 'foo'

    def teardown(self):
        del os.environ['MYTESTVAR']

    def test_expand_envvars(self):
        assert 'hello-foo' == compiled_value('hello-$MYTESTVAR')
        assert 'hello-foo' == compiled_value('hello-${MYTESTVAR}')
        assert 'hello-$(MYTESTVAR)' == compiled_value('hello-$(MYTESTVAR)')
