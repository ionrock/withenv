"""
Compile our environment from directories and files.
"""
import os

from heapq import heappush

import yaml

from withenv.flatten import flatten


def find_yml_in_dir(dirname):
    def is_yaml(fn):
        return fn.endswith(('yml', 'yaml'))

    fnames = []  # a heap

    for dirpath, dirnames, filenames in os.walk(dirname):
        for fn in filter(is_yaml, filenames):
            heappush(fnames, os.path.join(dirpath, fn))

    return fnames


def update_env_from_dir(dirname, env):
    for fname in find_yml_in_dir(dirname):
        update_env_from_file(fname, env)


def update_env_from_file(fname, env):
    new_env = yaml.safe_load(open(fname))
    flat_env = {}

    # Order isn't important
    if isinstance(new_env, dict):
        new_env = [new_env]

    for item in new_env:
        for k, v in flatten(item):
            env[k] = v


def update_env_from_alias(fname, env):
    action_list = yaml.safe_load(open(fname))
    actions = [
        (k, v) for action in action_list
        for k, v in action.items()
    ]
    print(actions)
    return compile(actions, env)


def find_action(name):
    actions = {
        'file': update_env_from_file,
        'directory': update_env_from_dir,
        'alias': update_env_from_alias,
    }
    return actions[name]


def compile(actions=None, env=None):
    actions = actions or []
    env = env if env is not None else os.environ

    for action, arg in actions:
        find_action(action)(arg, env)
    return env
