import os
import sys
import subprocess

import six

from .config import load_config_file
from .args import parse_args
from .env import compile


def main():
    args = parse_args()

    actions = load_config_file()
    actions.extend(args.actions or [])

    env = None
    if args.clean:
        env = {}

    os.environ = compile(actions, env)

    if args.cmd:
        if args.dump:
            print('Writing dump file: %s' % args.dump)
            with open(args.dump, 'w+') as fh:
                for k, v in os.environ.iteritems():
                    fh.write('%s=%s\n' % (k, v))

        proc = subprocess.Popen(' '.join(args.cmd), shell=True)
        try:
            proc.wait()
        except (SystemExit, KeyboardInterrupt):
            proc.kill()

        if args.dump:
            os.remove(args.dump)

        sys.exit(proc.returncode)

    else:
        # print our env as a file sourceable in bash.
        items = sorted([(k, v) for k, v in six.iteritems(os.environ)])
        for k, v in items:
            print("export %s='%s'" % (k, v))

if __name__ == '__main__':
    main()
