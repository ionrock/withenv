import os
import sys
import json
import subprocess

from heapq import heappush

import yaml


def flatten(node, prefix=None):
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
            for kid in flatten(v, prefix=k):
                print(kid)
                yield kid


def find_yml_in_dir(dirname):
    def is_yaml(fn):
        return fn.endswith(('yml', 'yaml'))

    fnames = []  # a heap

    for dirpath, dirnames, filenames in os.walk(dirname):
        for fn in filter(is_yaml, filenames):
            heappush(fnames, os.path.join(dirpath, fn))

    return fnames


def update_yaml_from_dir(dirname):
    for fname in find_yml_in_dir(dirname):
        update_env_from_yaml(fname)


def update_env_from_file(fname):
    new_env = yaml.safe_load(open(fn))
    flat_env = dict(flatten(new_env))
    os.environ.update(flat_env)


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
        '-d': update_yaml_from_dir,
        '--directory': update_yaml_from_dir,
    }

    state = None

    while args:
        arg = args.pop(0)
        if not state:
            for flag, key in flags.iteritems():
                if arg.startswith(flag):
                    state = key

            # Done with our flags
            if not state:
                results['cmd'] = [arg] + args
                break

        elif state:
            results[args].append((state, arg))
            state = None

    return results


def main():
    args = parse_args()

    map(lambda func, arg: func(arg), args['actions'])

    if args['cmd']:
        subprocess.call(args['cmd'])

if __name__ == '__main__':
    main()
