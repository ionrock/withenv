import os
import sys
import json
import subprocess

from heapq import heappush

import yaml
import six

from .args import parse_args
from .env import compile


def print_help_and_exit(*args):
    help = '''usage: we [OPTIONS]... COMMAND

Prepare the environment variables prior to running a command.

    -e, --environment    use a specific YAML file
    -d, --directory      recursively use a directory of YAML files
    -a, --alias          use an alias YAML file for flags

    -h, --help           display this message

More than one flag can be used a time. Each flag will be applied to
the environment variables in order, allowing a cascade of changes.
'''
    print(help)
    sys.exit(0)


def main():
    args = parse_args()

    os.environ = compile(args.actions)

    if args.cmd:
        sys.exit(subprocess.call(' '.join(args.cmd), shell=True))
    else:
        # print our env as a file sourceable in bash.
        items = sorted([(k, v) for k, v in six.iteritems(os.environ)])
        for k, v in items:
            print("export %s='%s'" % (k, v))

if __name__ == '__main__':
    main()
