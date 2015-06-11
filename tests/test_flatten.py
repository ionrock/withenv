from withenv.cli import flatten


def test_flatten_dict_strings():
    d = {'foo': {'bar': {'baz': 'hello world'}}}
    assert dict(flatten(d)) == {'foo_bar_baz': 'hello world'}


def test_flatten_dict_numbers():
    d = {'foo': {'bar': {'baz': 1001}}}
    assert dict(flatten(d)) == {'foo_bar_baz': '1001'}
