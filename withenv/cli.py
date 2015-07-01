import os
import sys
import json
import subprocess

from heapq import heappush

import yaml
import six

from .args import parse_args
from .env import compile


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
