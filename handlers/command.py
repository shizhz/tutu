# -*- coding: utf-8 -*-

import logging
import json

from handlers.base import BaseHandler
from modules.command import all_commands

logger = logging.getLogger('tutu.handlers.' + __name__)

class CommandHandler(BaseHandler):
    """
    Handling all command
    """
    pass

class CommandListHandler(BaseHandler):
    def get(self):
        commands = [{"name": c.name, "aliases": c.alias} for c in all_commands]
        logger.info("All Commands: %s", str(commands))
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(commands))
