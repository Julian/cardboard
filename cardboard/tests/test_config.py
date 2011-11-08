from ConfigParser import ConfigParser
import platform
import unittest

import mock

from cardboard import config as c


class TestConfig(unittest.TestCase):
    def test_get(self):
        config = mock.Mock(spec=ConfigParser)
        g = c.get(config, "foo", "bar")
        config.get.assert_called_once_with("foo", "bar")
        self.assertIs(g, config.get.return_value)
