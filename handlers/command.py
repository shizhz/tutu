# -*- coding: utf-8 -*-

import logging
import json

from handlers.base import BaseHandler
from modules.command import all_commands
from modules.command.parser import CommandParser

logger = logging.getLogger('tutu.handlers.' + __name__)

class CommandHandler(BaseHandler):
    """
    Handling all command
    """
    def post(self):
        cParser = CommandParser()
        cmd = cParser.parse(self.get_json_argument('command'))
        self.write_json({
            'result': cmd.execute()
        })

class CommandListHandler(BaseHandler):
    def get(self):
        commands = [{"name": c.name, "aliases": c.alias} for c in all_commands]
        logger.info("All Commands: %s", str(commands))
        self.write_json(commands)
