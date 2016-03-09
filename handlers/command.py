# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import logging
import json
import tornado.websocket
import threading

from handlers.base import BaseHandler
from modules.cache import CURRENT as cache
from modules.command import all_commands
from modules.command.cmd_share import ShareCommand
from modules.command.exceptions import *
from modules.mesos.exceptions import *
import modules.command.parser as parser

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

    def cache_cmd(self, args):
        cache.set_cache(self.get_share_code(args), self.get_cmd(args))

    def detect_topic(self, command):
        return 'share' if isinstance(command, ShareCommand) else 'cmd_result'

    def get_share_code(self, args):
        return str(json.loads(args)['shareCode'])

    def get_cmd(self, args):
        return str(json.loads(args)['command'])

    def on_message(self, command):
        logger.info("Recieved command '{0}' from '{1}'".format(command, self.request.remote_ip))
        try:
            self.cache_cmd(command)
            ori_cmd = ""
            cmd = parser.command_parser.parse(self.get_cmd(command))
            ori_cmd = cmd.get_shared_command() if isinstance(cmd, ShareCommand) else "",
            topic = self.detect_topic(cmd)
            result = cmd.execute()
        except UnknownCommandException, e:
            logger.exception(e)
            topic = 'cmd_result'
            result = """Command not found, please use one of the available commands below:\n {0} """.format(self._available_commands()) if 'FUCK' not in command.upper() else 'Fuck you!!!'
        except SharedCommandExpiredException, e:
            logger.exception(e)
            topic = 'internal_error'
            result = """The command other people shared to you has been expired. Please check out the above message about how to use Tutu"""
        except InvalidCommandException, e:
            logger.exception(e)
            topic = 'internal_error'
            result = "Seems you are not using the command the right way. Tey `help` command to get help info."
        except AppNotFoundException, e:
            logger.exception(e)
            topic = 'internal_error'
            result = e.msg
        except Exception, e:
            logger.exception(e)
            topic = 'internal_error'
            result = "Ooops... something wrong happened"
        finally:
            try:
                self._write_json({
                    "topic": topic,
                    "share_code": self.get_share_code(command),
                    "cmd": ori_cmd,
                    "data": result
                })
            except Exception, e:
                logger.exception(e)
                self._write_json({
                    "topic": "internal_error",
                    "share_code": "",
                    "data": "Ooops... something wrong happened: " + str(e)
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
