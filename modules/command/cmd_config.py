# -*- coding: utf-8 -*-

import logging

from cmd import Command, validator, cmd_indicator
from config import config

logger = logging.getLogger('tutu.modules.command.' + __name__)

class ConfigCommand(Command):
    """
    NAME: configs(cf)

    SYNOPSIS: configs

    DESC: Get config information
    """
    name = 'configs'
    alias = ['cf']

    def execute(self):
        return config.help_info()

class ConfigCommandParser(object):
    support = cmd_indicator(ConfigCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) == 1

    def parse(self, txt):
        return ConfigCommand()

