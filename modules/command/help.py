# -*- coding: utf-8 -*-

from parser import CommandParser
from models import CommandInfo

class HelpCommandParser(CommandParser):
    def support(self, text):
        return text.startswith('help')

    def parse(self, text):
        """
        help command should be the format like:
        - help sh
        - help show
        """
        help_cmd = text.split()[0]
        target_cmd = ' '.join(text.split()[1:])
        if self.support(target_cmd.strip()):
            # return if it's asking for help info of `help` command itself
            return CommandInfo(help_cmd, target_cmd_help=self.help())

        target_cmd_info = super(HelpCommandParser, self).parse(target_cmd)
        return CommandInfo(help_cmd, target_cmd_help=target_cmd_info.help)

    def help(self):
        return """
        NAME: help - get help info for specified command
        SYNOPSIS: help <command>
        DESC: get help info for specified command, about how to use it and what it's used for.
        E.G. help help
             help sh
        """
