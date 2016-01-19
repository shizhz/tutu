# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

from modules.command.parser import CommandParser
from modules.command.exceptions import UnknownCommandException, InvalidCommandException

class MockParser(object):
    def is_valid(self, cmd):
        return True

    def support(self, txt):
        return txt.startswith('mock')

    def parse(self, txt):
        return "MockCommandInfo"

class MockNotValidParser(object):
    def is_valid(self, cmd):
        return False

class TestCommandParser(unittest.TestCase):
    def test_parse(self):
        cmd_parser = CommandParser(parsers=[MockParser()])
        cmd_info = cmd_parser.parse('mock cmd')
        assert type(cmd_info) is str
        assert cmd_info == 'MockCommandInfo'

    @raises(InvalidCommandException)
    def test_is_not_valid(self):
        cmd_parser = CommandParser(parsers=[MockNotValidParser()])
        cmd_info = cmd_parser.parse('mock cmd')

    @raises(UnknownCommandException)
    def test_unknownexception(self):
        cmd_parser = CommandParser(parsers=[MockParser()])
        cmd_parser.parse('unknown cmd')
