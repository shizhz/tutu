# -*- coding: utf-8 -*-
import unittest

from modules.command.cmd import Command
from modules.command.cmd_help import HelpCommandParser, HelpCommand, HelpCommandContext
from modules.command.models import CommandInfo

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


class TestHelpCommandContext(unittest.TestCase):
    def setUp(self):
        self.cmd_ctx = HelpCommandContext()
        self.cmd_ctx.all_commands = [HelpCommand]

    def tearDown(self):
        self.cmd_ctx = None

    def test_context(self):
        with self.cmd_ctx as ctx:
            assert isinstance(ctx, dict) is True
            assert HelpCommand.help_info() == ctx.get('help')

class MockCommand(Command):
    """
    Help info for MockCommand
    """
    name = 'mock_cmd'

class TestHelpCommand(unittest.TestCase):
    def setUp(self):
        self.cmd_ctx = HelpCommandContext()
        self.cmd_ctx.all_commands = [HelpCommand, MockCommand]
        self.help_cmd = HelpCommand('mock_cmd')

    def tearDown(self):
        self.cmd_ctx = None
        self.help_cmd = None

    def test_help_execute(self):
        help_mock_cmd = self.help_cmd.execute(self.cmd_ctx)
        assert MockCommand.help_info() == MockCommand.help_info()
