"""
Compile our environment from directories and files.
"""
import os
import shlex
import subprocess

from heapq import heappush

import yaml

from withenv.flatten import flatten


def path_relative_to(root, fname):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        root = os.path.dirname(root)
    return os.path.normpath(os.path.join(root, fname))


def string_to_cmd(command):
    return [
        os.path.expandvars(part)
        for part in shlex.split(command)
    ]


def find_piped_cmds(cmd):
    if '|' not in cmd:
        return None

    cmds = []
    cur = []
    for part in cmd:
        if part == '|':
            cmds.append(cur)
            cur = []
        else:
            cur.append(part)
    cmds.append(cur)
    return cmds


def get_cmd_output(cmd):
    cmds = find_piped_cmds(cmd)

    if not cmds:
        return subprocess.check_output(cmd)

    # we have multiple commands
    proc = subprocess.Popen(cmds[0], stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    for cmd in cmds[1:]:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        stdout, _ = proc.communicate(stdout)
    proc.wait()
    return stdout


def compiled_value(v):
    if v.startswith('`') and v.endswith('`'):
        cmd = string_to_cmd(v[1:-1])
        v = get_cmd_output(cmd).strip()
    return os.path.expandvars(v)


def load_shell_env_file(fname):
    # look for lines with export and parse them
    env = {}
    with open(fname) as fh:
        for line in fh:
            if line.startswith('export'):
                prefix, _, envvar = line.partition(' ')
                k, _, v = envvar.partition('=')
                env[k] = compiled_value(v)

    return env


def load_env_file(fname):
    if fname.endswith(('yml', 'yaml')):
        return yaml.safe_load(open(fname))
    return load_shell_env_file(fname)


def find_yml_in_dir(dirname):
    def is_yaml(fn):
        return fn.endswith(('yml', 'yaml'))

    fnames = []  # a heap

    for dirpath, dirnames, filenames in os.walk(dirname):
        for fn in filter(is_yaml, filenames):
            heappush(fnames, os.path.join(dirpath, fn))

    return fnames


def update_env_from_obj(new_env, env):
    # Order isn't important
    if isinstance(new_env, dict):
        new_env = [new_env]

    if not new_env:
        return

    for item in new_env:
        for k, v in flatten(item):
            env[k] = compiled_value(v)


def update_env_from_dir(dirname, env):
    for fname in find_yml_in_dir(dirname):
        update_env_from_file(fname, env)


def update_env_from_file(fname, env):
    new_env = yaml.safe_load(open(fname))
    update_env_from_obj(new_env, env)


def update_env_from_alias(fname, env):
    action_list = yaml.safe_load(open(fname))
    if not action_list:
        return env

    actions = []
    for action in action_list:
        for k, v in action.items():
            if not k == 'override':
                v = path_relative_to(fname, v)
            actions.append((k, v))

    return compile(actions, env)


def update_env_from_override(override, env):
    k, _, v = override.partition('=')
    env[k] = compiled_value(v)


def update_env_from_script(script, env):
    doc = get_cmd_output(string_to_cmd(script))
    try:
        new_env = yaml.safe_load(doc)
        update_env_from_obj(new_env, env)
    except yaml.YAMLError as e:
        print('Invalid YAML: %s' % e)
        os.exit(1)


def find_action(name):
    actions = {
        'file': update_env_from_file,
        'directory': update_env_from_dir,
        'alias': update_env_from_alias,
        'override': update_env_from_override,
        'script': update_env_from_script,
    }
    return actions[name]


def compile(actions=None, env=None):
    actions = actions or []
    env = env if env is not None else os.environ

    for action, arg in actions:
        find_action(action)(arg, env)
    return env
