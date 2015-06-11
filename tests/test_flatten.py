from withenv.cli import env


def test_flatten_dict_strings():
    d = {'foo': {'bar': {'baz': 'hello world'}}}
    assert dict(env(d)) == {'foo_bar_baz': 'hello world'}


def test_flatten_dict_numbers():
    d = {'foo': {'bar': {'baz': 1001}}}
    assert dict(env(d)) == {'foo_bar_baz': '1001'}
