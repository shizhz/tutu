# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import logging
import json
import tornado.websocket
import threading

from handlers.base import BaseHandler
from modules.cache import CURRENT as cache
from modules.command import all_commands, command_parser
from modules.command.cmd_share import ShareCommand
from modules.command.exceptions import *
from modules.command.parser import CommandParser

logger = logging.getLogger('tutu.handlers.' + __name__)

class CommandWSHandler(tornado.websocket.WebSocketHandler):
    lock = threading.Lock()
    connections = 0

    def _available_commands(self):
        return ", ".join([c.name for c in all_commands])

    def _write_json(self, data):
        self.write_message(json.dumps(data))

    def open(self):
        with self.lock:
            self.__class__.connections += 1
            logger.info("New connection from: {0}, current total connections: {1}".format(self.request.remote_ip, self.__class__.connections))

        self._write_json({
            "topic": "ws_open",
            "data": self._available_commands()
        })

    def cache_cmd(self, command):
        share_code = cache.random_cache_key()

        cache.set_cache(share_code, command)

        return share_code

    def detect_topic(self, command):
        return 'share' if isinstance(command, ShareCommand) else 'cmd_result'

    def on_message(self, command):
        logger.info("Recieved command '{0}' from '{1}'".format(command, self.request.remote_ip))
        try:
            cmd = command_parser.parse(command)
            result = cmd.execute()
        except UnknownCommandException:
            result = """Command not found, please use one of the available commands below:\n {0} """.format(self._available_commands())
        except Exception, e:
            logger.exception(e)
            result = "Ooops... something wrong happened"
        finally:
            self._write_json({
                "topic": self.detect_topic(cmd),
                "share_code": self.cache_cmd(command),
                "data": result
            })

    def on_close(self):
        with self.lock:
            self.__class__.connections -= 1
            logger.info("Remove connection from: {0}, current total connections: {1}".format(self.request.remote_ip, self.__class__.connections))

class CommandListHandler(BaseHandler):
    def get(self):
        commands = [{"name": c.name, "aliases": c.alias} for c in all_commands]
        logger.info("All Commands: %s", str(commands))
        self.write_json(commands)
