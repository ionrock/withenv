import sys

from argparse import ArgumentParser, Action, REMAINDER


class AddToEnvsAction(Action):

    action_map = {
        '-e': 'file',
        '--environment': 'file',
        '-d': 'directory',
        '--directory': 'directory',
        '-a': 'alias',
        '--alias': 'alias',
    }

    def __init__(self, *args, **kw):
        super(AddToEnvsAction, self).__init__(*args, **kw)
        self.env_type = self.action_map.get(self.dest)

    def __call__(self, parser, namespace, values, option_string):
        envs = getattr(namespace, self.dest) or []
        envs.append((self.action_map[option_string], values))
        setattr(namespace, self.dest, envs)


def parse_args(args=None):
    actions = []
    parser = ArgumentParser()
    parser.add_argument('-e', '--environment', dest='actions',
                        nargs='?', action=AddToEnvsAction)

    parser.add_argument('-d', '--directory', dest='actions',
                        nargs='?', action=AddToEnvsAction)

    parser.add_argument('-a', '--alias', dest='actions',
                        nargs='?', action=AddToEnvsAction)

    parser.add_argument('cmd', nargs=REMAINDER)

    args = args if args is not None else sys.argv[1:]

    return parser.parse_args(args)
