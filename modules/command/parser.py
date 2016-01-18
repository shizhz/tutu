# -*- coding: utf-8 -*-

from sh import ShCommandParser

class CommandParser(object):
    parsers = [ShCommandParser()]

    def __init__(self, parsers=parsers):
        self.parsers = parsers

    def parse(self, text):
        txt = text.strip().lower()
        for parser in self.parsers:
            if parser.support(txt):
                return parser.parse(txt)
