# -*- coding: utf-8 -*-
import unittest

from modules.command.help import HelpCommandParser
from modules.command.models import CommandInfo

class TestHelp(unittest.TestCase):
    def setUp(self):
        self.command_parser = HelpCommandParser()

    def tearDown(self):
        self.command_parser = None

    def test_support_true(self):
        assert self.command_parser.support('help sh') == True

    def test_support_false(self):
        assert self.command_parser.support('non-help sh') == False

    def test_parse_help_sh_cmd(self):
        text = "help sh"
        cmd_info = self.command_parser.parse(text)
        assert cmd_info.command == 'help'
        assert cmd_info.target_cmd_help is not None
        assert 'sh' in cmd_info.target_cmd_help

    def test_parse_help_itself(self):
        text = "help help"
        cmd_info = self.command_parser.parse(text)
        assert cmd_info.command == 'help'
        assert cmd_info.target_cmd_help is not None
        assert 'NAME: help -' in cmd_info.target_cmd_help

