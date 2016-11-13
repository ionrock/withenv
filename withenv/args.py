import sys

from argparse import ArgumentParser, Action, REMAINDER


class AddToEnvsAction(Action):

    action_map = {
        '-e': 'file',
        '--env': 'file',

        '-d': 'directory',
        '--dir': 'directory',

        '-a': 'alias',
        '--alias': 'alias',

        '-E': 'override',
        '--envvar': 'override',

        '-s': 'script',
        '--script': 'script',
    }

    def __init__(self, *args, **kw):
        super(AddToEnvsAction, self).__init__(*args, **kw)
        self.env_type = self.action_map.get(self.dest)

    def __call__(self, parser, namespace, values, option_string):
        envs = getattr(namespace, self.dest) or []
        envs.append((self.action_map[option_string], values))
        setattr(namespace, self.dest, envs)


def parse_args(args=None):
    parser = ArgumentParser(
        prog='we',
        usage='%(prog)s -h [-e ENV_YAML] [-d DIR] [-a ALIAS_YAML] CMD',
        description=('Prepare the environment variables '
                     'prior to running a command.'),

        epilog=('More than one flag can be used a time. '
                'Each flag will be applied to the environment '
                'variables in order, allowing a cascade of changes.')
    )

    parser.add_argument(
        '--clean', action='store_true', default=False,
        help='Only use the enviroment from the YAML',
    )

    parser.add_argument(
        '-e', '--env', dest='actions',
        nargs='?', action=AddToEnvsAction,
        help='a YAML file to include in the environment',
        metavar='YML',
    )

    parser.add_argument(
        '-d', '--dir', dest='actions',
        nargs='?', action=AddToEnvsAction,
        help=('a directory containing YAML files to '
              'recursively apply to the environment'),
        metavar='DIR',
    )

    parser.add_argument(
        '-a', '--alias', dest='actions',
        nargs='?', action=AddToEnvsAction,
        help=('a YAML file containing a list of '
              'file/directory to apply to the environment'),
        metavar='ALIAS YML',
    )

    parser.add_argument(
        '-E', '--envvar', dest='actions',
        nargs='?', action=AddToEnvsAction,
        help=('override a single envvar'),
        metavar='ENVVAR',
    )

    parser.add_argument(
        '-s', '--script', dest='actions',
        nargs='?', action=AddToEnvsAction,
        help=('use the yaml or json output from a script or command'),
        metavar='SCRIPT',
    )

    parser.add_argument(
        '-D', '--dump',
        help=('Dump the env to a file and remove when the process exits'),
        metavar='ENVFILE',
    )

    parser.add_argument(
        'cmd', nargs=REMAINDER,
        help='The command to run with the supplied environment.',
        metavar='CMD'
    )

    args = args if args is not None else sys.argv[1:]

    return parser.parse_args(args)
