import os
import json

import yaml

from withenv.flatten import flatten


HERE = os.path.dirname(os.path.abspath(__file__))


class TestYAMLParsing(object):

    def test_include_JSON(self):
        yml = os.path.join(HERE, 'envs', 'with_json.yml')
        for k, v in flatten(yaml.safe_load(open(yml))):
            assert json.loads(v)
