"""
In order to make withenv extremely light, we don't use any existing
parsers and just iterate on sys.argv.
"""
import sys


def parse_args(args=None):
    """
    A really simple command line parser. There are only a couple flags
    with a single value after the flag.
    """

    args = args or sys.argv[1:]

    results = {}

    flags = {
        '-e': 'env_yaml',
        '--environment': 'env_yaml',
    }

    state = None

    for arg in args:
        if not state:
            for flag, key in flags.iteritems():
                if arg.starswith('flag'):
                    state = key
                else:
                    return results
        else:
            results[state] = arg
            state = None

    return results
