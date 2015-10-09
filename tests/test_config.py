import os

from mock import patch, Mock
from withenv import config


class TestConfig(object):

    @patch.object(config, 'find_config_file', Mock(return_value='.werc'))
    def test_load_config_returns_actions(self):
        assert config.load_config_file() == [('alias', '.werc')]

    def test_find_config(self):
        config_path = config.find_config_file(
            start=os.path.dirname(os.path.abspath(__file__)),
            filename='test.werc'
        )
        assert config
