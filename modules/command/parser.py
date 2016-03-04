# -*- coding: utf-8 -*-

import logging

import cmd_sh
import cmd_help
import cmd_config
import cmd_share
import cmd_apps
from exceptions import UnknownCommandException


logger = logging.getLogger('tutu.modules.command.' + __name__)
all_parsers = [cmd_help.HelpCommandParser(), cmd_sh.ShCommandParser(), cmd_config.ConfigCommandParser(), cmd_share.ShareCommandParser(), cmd_apps.AppsCommandParser(), cmd_apps.AppInfoCommandParser()]

class CommandParser(object):
    parsers = all_parsers

    def __init__(self, parsers=parsers):
        self.parsers = parsers

    def parse(self, text):
        logger.debug('Parsing: {0}'.format(text))
        txt = text.strip().lower()
        for parser in self.parsers:
            if parser.support(txt) and parser.is_valid(txt):
                return parser.parse(txt)

        raise UnknownCommandException(txt)


command_parser = CommandParser()
