import os
import sys
import subprocess

import six

from .config import load_config_file
from .args import parse_args
from .env import compile


class Executor(object):

    def __init__(self, cmd):
        self.cmd = cmd

    def expanded_cmd(self):
        cmd = []
        for part in self.cmd:
            cmd.append(os.path.expandvars(part))
        return cmd

    def __call__(self):
        try:
            proc = subprocess.Popen(self.expanded_cmd())
            proc.wait()
        except OSError as e:
            print(e)
            sys.exit(e.errno)
        except (SystemExit, KeyboardInterrupt):
            proc.kill()

        return proc


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

        cmd = Executor(args.cmd)
        proc = cmd()

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
