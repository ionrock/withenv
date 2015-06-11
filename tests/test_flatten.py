from withenv.cli import flatten


def test_flatten():

    env = {
        'foo': {
            'bar': {
                'baz': 'hello world'
            }
        }
    }

    assert flatten(env) == {'foo_bar_baz': 'hello world'}


def test_flatten_dict():
    d = {'foo': {'bar': {'baz': 'hello world'}}}
    assert flatten(env) == {'foo_bar_baz': 'hello world'}
