import os
import six


def flatten_list(node, prefix=None):
    for v in node:
        for kid in flatten_dict(v, prefix):
            yield kid


def flatten_dict(node, prefix=None):
    """
    This is an iterator that returns a list of flattened env
    vars based on the conf file supplied
    """
    for k, v in six.iteritems(node):
        if prefix:
            k = '%s_%s' % (prefix, k)

        # We have a value we can stringify
        if not isinstance(v, (dict, list)):
            yield (k, os.path.expandvars(str(v)))
        else:
            for kid in flatten(v, prefix=k):
                yield kid


def flatten(node, prefix=None):
    flat_func = flatten_dict
    if isinstance(node, list):
        flat_func = flatten_list

    for kid in flat_func(node, prefix):
        yield kid
