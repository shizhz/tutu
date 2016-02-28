# -*- coding: utf-8 -*-

from cmd_help import HelpCommand
from cmd_sh import ShCommand
from cmd_config import ConfigCommand
from parser import CommandParser

all_commands = [HelpCommand, ShCommand, ConfigCommand]
command_parser = CommandParser()
