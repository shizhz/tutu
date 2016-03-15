# -*- coding: utf-8 -*-

import logging

from cmd import Command, validator, cmd_indicator
from cmd_sh import ShCommand
from cmd_apps import AppsCommand, AppInfoCommand
from cmd_config import ConfigCommand
from cmd_share import ShareCommand
from models import CommandInfo
from exceptions import UnknownCommandException

logger = logging.getLogger('tutu.modules.command.' + __name__)
_all_commands = [ShCommand, AppsCommand, ConfigCommand, ShareCommand, AppInfoCommand]

class HelpCommand(Command):
    """
    NAME: help(h, he, hel) - get help info for specified command

    SYNOPSIS: help <command>

    DESC: get help info for specified command, about how to use it and what it's used for.

    E.G. help help
         help sh
    """
    name = 'help'
    alias = ['h', 'he', 'hel']

    def __init__(self, target_cmd):
        self.target_cmd = target_cmd

    def _cmd_notfound(self):
        raise UnknownCommandException(self.target_cmd)

    def _help_infos(self, commands=_all_commands):
        commands = list(set(commands + [self.__class__]))
        return dict(map(lambda cmd: [cmd.name, cmd.help_info()], commands))

    def execute(self, commands=_all_commands):
        return self._help_infos(commands=commands).get(self.target_cmd) or self._cmd_notfound()

class HelpCommandParser(object):
    support = cmd_indicator(HelpCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) >= 1

    def parse(self, txt):
        """
        help command should be the format like:
        - help sh
        - help show
        """
        try:
            target_cmd = txt.split()[1]
        except IndexError:
            target_cmd = 'help'

        return HelpCommand(target_cmd)

