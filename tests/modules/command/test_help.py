# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

from modules.command.cmd import Command
from modules.command.cmd_help import HelpCommandParser, HelpCommand
from modules.command.models import CommandInfo
from modules.command.exceptions import UnknownCommandException

class TestHelpParser(unittest.TestCase):
    def setUp(self):
        self.command_parser = HelpCommandParser()

    def tearDown(self):
        self.command_parser = None

    def test_support_true(self):
        assert self.command_parser.support('help sh') == True

    def test_support_alias(self):
        assert self.command_parser.support('h sh') == True
        assert self.command_parser.support('he sh') == True
        assert self.command_parser.support('hel sh') == True

    def test_support_false(self):
        assert self.command_parser.support('non-help sh') == False

    def test_parse_help_itself(self):
        text = "help help"
        cmd_help = self.command_parser.parse(text)
        assert isinstance(cmd_help, HelpCommand)

    def test_parse_help_default(self):
        text = "help"
        cmd_help = self.command_parser.parse(text)
        assert isinstance(cmd_help, HelpCommand)

class MockCommand(Command):
    """
    Help info for MockCommand
    """
    name = 'mock_cmd'

class TestHelpCommand(unittest.TestCase):
    def setUp(self):
        self.all_commands = [HelpCommand, MockCommand]
        self.help_cmd = HelpCommand('mock_cmd')

    def tearDown(self):
        self.help_cmd = None

    def test_help_execute(self):
        help_mock_cmd = self.help_cmd.execute(commands=self.all_commands)
        assert MockCommand.help_info() == MockCommand.help_info()

    @raises(UnknownCommandException)
    def test_unknown_command(self):
        self.help_cmd.execute(commands=[])

    def test_unknown_command_msg(self):
        try:
            self.help_cmd.execute(commands=[])
        except UnknownCommandException, e:
            assert 'Unknown Command: mock_cmd' == e.msg
