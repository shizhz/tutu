# -*- coding: utf-8 -*-

import logging

from cmd import Command, validator, cmd_indicator
from modules.cache import CURRENT as cache
import parser

logger = logging.getLogger('tutu.modules.command.' + __name__)

class ShareCommand(Command):
    """
    NAME: share

    SYNOPSIS: share <share code>

    DESC: Parse and execute command by share code. This command is not supposed to be used directly by user.
    """
    name = 'share'
    alias = []

    def __init__(self, share_code):
        self.share_code = share_code

    def get_shared_command(self):
        return cache.get_cache(self.share_code)

    def execute(self):
        return parser.command_parser.parse(self.get_shared_command()).execute()


class ShareCommandParser(object):
    support = cmd_indicator(ShareCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) == 2

    def parse(self, txt):
        share_code = txt.split()[-1]
        return ShareCommand(share_code)

