# -*- coding: utf-8 -*-

import parser
import cmd_help
import cmd_sh
import cmd_config
import cmd_apps

all_commands = [cmd_help.HelpCommand, cmd_sh.ShCommand, cmd_config.ConfigCommand, cmd_apps.AppsCommand, cmd_apps.AppInfoCommand]
