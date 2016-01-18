# -*- coding: utf-8 -*-
import unittest

from modules.command.parser import CommandParser

class MockParser(object):
    def support(self, txt):
        return txt.startswith('mock')

    def parse(self, txt):
        return "MockCommandInfo"

class TestCommandParser(unittest.TestCase):
    def setUp(self):
        self.cmd_parser = CommandParser([MockParser()])

    def tearDown(self):
        self.cmd_parser = None

    def test_parse(self):
        cmd_info = self.cmd_parser.parse('mock cmd')
        assert type(cmd_info) is str
        assert cmd_info == 'MockCommandInfo'

