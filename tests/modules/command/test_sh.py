# -*- coding: utf-8 -*-
import unittest

from modules.command.sh import ShCommandParser
from modules.command.models import CommandInfo

class TestSh(unittest.TestCase):
    def setUp(self):
        self.sh_command_parser = ShCommandParser()

    def tearDown(self):
        self.sh_command_parser = None

    def test_support_true(self):
        assert self.sh_command_parser.support('sh dev-member-web ls /opt') == True

    def test_support_false(self):
        assert self.sh_command_parser.support('non-sh dev-member-web ls /opt') == False

    def test_parse_sh_cmd(self):
        text = "sh dev-member-web ls /opt"
        cmd_info = self.sh_command_parser.parse(text)
        assert cmd_info.command == 'sh'
        assert cmd_info.marathon_app_id == 'dev-member-web'
        assert cmd_info.remote_cmd == ['ls', '/opt']
