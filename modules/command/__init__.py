# -*- coding: utf-8 -*-

import parser
import cmd_help
import cmd_sh
import cmd_config
import parser

all_commands = [cmd_help.HelpCommand, cmd_sh.ShCommand, cmd_config.ConfigCommand]
command_parser = parser.CommandParser()
