# -*- coding: utf-8 -*-

from cmd import Command, CommandContext, validator, cmd_indicator
from cmd_sh import ShCommand
from models import CommandInfo

class HelpCommand(Command):
    """
    NAME: help - get help info for specified command

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

    def execute(self, context):
        with context as cmds:
            return cmds.get(self.target_cmd) or self._cmd_notfound()

class HelpCommandParser(object):
    support = cmd_indicator(HelpCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) > 1

    def parse(self, txt):
        """
        help command should be the format like:
        - help sh
        - help show
        """
        target_cmd = txt.split()[1]
        return HelpCommand(target_cmd)

class HelpCommandContext(CommandContext):
    all_commands = [ShCommand, HelpCommand]
    def enter(self):
        return dict(map(lambda cmd: [cmd.name, cmd.help_info()], self.all_commands))

    def exit(self, type, value, traceback):
        pass
