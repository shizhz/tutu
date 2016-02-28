# -*- coding: utf-8 -*-

import logging

from cmd_sh import ShCommandParser
from cmd_help import HelpCommandParser
from cmd_config import ConfigCommandParser
from exceptions import UnknownCommandException

all_parsers = [HelpCommandParser(), ShCommandParser(), ConfigCommandParser()]

logger = logging.getLogger('tutu.handlers.' + __name__)

class CommandParser(object):
    parsers = all_parsers

    def __init__(self, parsers=parsers):
        self.parsers = parsers

    def parse(self, text):
        txt = text.strip().lower()
        for parser in self.parsers:
            if parser.support(txt) and parser.is_valid(txt):
                return parser.parse(txt)

        raise UnknownCommandException(txt)
