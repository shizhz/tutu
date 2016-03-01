# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import logging
from tornado.options import options
from tornado import gen
import requests

from config.config import marathon_zks
from handlers.base import BaseHandler
from modules.mesos.marathon import Marathon
from modules.cache import CURRENT as cache


logger = logging.getLogger('tutu.handlers.' + __name__)

@gen.coroutine
def registry_marathon_event_handler():
    logger.debug('Registry Marathon callbacks')
    marathon_callback_url = options.access_address.rstrip('/') + '/api/marathon/callback'
    marathons = map(lambda zk: Marathon(zk), marathon_zks)

    for marathon in marathons:
        marathon.register_callback(marathon_callback_url)

class MarathonEventsHandler(BaseHandler):
    def post(self):
        self.load_json()
        print(str(self.request.arguments))

