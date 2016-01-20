# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

from modules.command.exceptions import InvalidCommandException
from modules.command.cmd_sh import ShCommandParser

class TestSh(unittest.TestCase):
    def setUp(self):
        self.sh_command_parser = ShCommandParser()

    def tearDown(self):
        self.sh_command_parser = None

    def test_support_true(self):
        assert self.sh_command_parser.support('sh dev-member-web ls /opt') == True

    def test_support_false(self):
        assert self.sh_command_parser.support('non-sh dev-member-web ls /opt') == False

    def test_support_false_when_no_remote_sh_provided(self):
        assert self.sh_command_parser.support('non-sh dev-member-web') == False

    def test_support_false_when_env_provided_but_no_remote_sh_provided(self):
        assert self.sh_command_parser.support('non-sh -e dev member-web') == False

    @raises(InvalidCommandException)
    def test_parse_failed_when_env_provided_but_no_remote_sh_provided(self):
        # TODO: fix this test tomorrow, it's time to sleep now :-)
        self.sh_command_parser.parse('non-sh -e dev member-web')

    def test_parse_sh_cmd_without_env_option(self):
        text = "sh dev-member-web ls /opt"
        cmd_sh = self.sh_command_parser.parse(text)

        assert cmd_sh.name == 'sh'
        assert cmd_sh.env == 'dev'
        assert cmd_sh.marathon_app_id == 'dev-member-web'
        assert cmd_sh.sh == ['ls', '/opt']

    def test_parse_sh_cmd_with_short_env_option(self):
        text = "sh -e dev member-web ls /opt"
        cmd_sh = self.sh_command_parser.parse(text)

        assert cmd_sh.name == 'sh'
        assert cmd_sh.env == 'dev'
        assert cmd_sh.marathon_app_id == 'member-web'
        assert cmd_sh.sh == ['ls', '/opt']

    def test_parse_sh_cmd_with_long_env_option(self):
        text = "sh --env dev member-web ls /opt"
        cmd_sh = self.sh_command_parser.parse(text)

        assert cmd_sh.name == 'sh'
        assert cmd_sh.env == 'dev'
        assert cmd_sh.marathon_app_id == 'member-web'
        assert cmd_sh.sh == ['ls', '/opt']
