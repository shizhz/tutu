# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import logging
import json
import tornado.websocket
import threading

from handlers.base import BaseHandler
from modules.command import all_commands
from modules.command.parser import CommandParser

logger = logging.getLogger('tutu.handlers.' + __name__)

class CommandWSHandler(tornado.websocket.WebSocketHandler):
    lock = threading.Lock()
    connections = 0

    def open(self):
        with self.lock:
            self.__class__.connections += 1
            logger.info("New connection from: {0}, current total connections: {1}".format(self.request.remote_ip, self.__class__.connections))

    def on_message(self, command):
        logger.info("Recieved command '{0}' from '{1}'".format(command, self.request.remote_ip))
        self.write_message(json.dumps({
            "topic": "cmd_result",
            "data": "Command Result {0}".format(command)
        }))

    def on_close(self):
        with self.lock:
            self.__class__.connections -= 1
            logger.info("Remove connection from: {0}, current total connections: {1}".format(self.request.remote_ip, self.__class__.connections))

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
