import os
import sys
import json
import subprocess

import yaml


def env(node, prefix=None):
    """
    This is an iterator that returns a list of flattened env
    vars based on the conf file supplied
    """
    for k, v in node.iteritems():
        if prefix:
            k = prefix + '_' + k

        if not isinstance(v, dict):
            yield (k, os.path.expandvars(str(v)))
        else:
            for kid in env(v, prefix=k):
                print(kid)
                yield kid


def parse_args(args=None):
    """
    A really simple command line parser. There are only a couple flags
    with a single value after the flag.
    """

    args = args if args is not None else sys.argv[1:]

    results = {
        'cmd': [],
        'env_files': [],
    }

    state = None

    while args:
        arg = args.pop(0)
        if not state:
            if arg.startswith('-e') or arg.startswith('--environment'):
                state = 'env_files'
            else:
                results['cmd'] = [arg] + args
                break
        elif state:
            results[state].append(arg)
            state = None

    return results


def main():
    args = parse_args()

    print(args)
    for fn in args.get('env_files'):
        new_env = yaml.safe_load(open(fn))
        flat_env = dict(env(new_env))
        os.environ.update(flat_env)

    if args['cmd']:
        subprocess.call(args['cmd'])

if __name__ == '__main__':
    main()
