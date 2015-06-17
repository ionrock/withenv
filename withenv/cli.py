import os
import sys
import json
import subprocess

from heapq import heappush

import yaml
import six

from .flatten import flatten


def find_yml_in_dir(dirname):
    def is_yaml(fn):
        return fn.endswith(('yml', 'yaml'))

    fnames = []  # a heap

    for dirpath, dirnames, filenames in os.walk(dirname):
        for fn in filter(is_yaml, filenames):
            heappush(fnames, os.path.join(dirpath, fn))

    return fnames


def update_env_from_dir(dirname):
    for fname in find_yml_in_dir(dirname):
        update_env_from_file(fname)


def update_env_from_file(fname):
    new_env = yaml.safe_load(open(fname))
    flat_env = {}

    # Order isn't important
    if isinstance(new_env, dict):
        new_env = [new_env]

    for item in new_env:
        for k, v in flatten(item):
            os.environ[k] = v


def parse_args(args=None):
    """
    A really simple command line parser. There are only a couple flags
    with a single value after the flag.
    """

    args = args if args is not None else sys.argv[1:]

    results = {
        'cmd': [],
        'actions': [],
    }

    flags = {
        '-e': update_env_from_file,
        '--environment': update_env_from_file,
        '-d': update_env_from_dir,
        '--directory': update_env_from_dir,
    }

    action = None

    while args:
        arg = args.pop(0)
        if not action:
            for flag, func in six.iteritems(flags):
                if arg.startswith(flag):
                    action = func

            # Done with our flags
            if not action:
                results['cmd'] = [arg] + args
                break
        elif action:
            results['actions'].append((action, arg))
            action = None

    return results


def main():
    args = parse_args()

    for func, arg in args['actions']:
        func(arg)

    if args['cmd']:
        subprocess.call(' '.join(args['cmd']), shell=True)
    else:
        # print our env as a file sourceable in bash.
        items = sorted([(k, v) for k, v in six.iteritems(os.environ)])
        for k, v in items:
            print("export %s='%s'" % (k, v))

if __name__ == '__main__':
    main()
