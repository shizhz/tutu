# -*- coding: utf-8 -*-

from __future__ import print_function, with_statement

import requests
import logging
from tornado.options import options
from tornado import gen

from handlers.base import BaseHandler
from modules.mesos.marathon import marathons, MarathonApp
from modules.cache import CURRENT as cache
from modules.util import val_from_json, has_val
from config.config import TEST

logger = logging.getLogger('tutu.handlers.' + __name__)

@gen.coroutine
def registry_marathon_event_handler():
    logger.debug('Registry Marathon callbacks')
    marathon_callback_url = options.access_address.rstrip('/') + '/api/marathon/callback'

    for marathon in marathons:
        marathon.register_callback(marathon_callback_url)

class MarathonEventsHandler(BaseHandler):
    registry = {}

    def initialize(self):
        try:
            MarathonEventsHandler.registry_event_handler(['deployment_info', 'deployment_step_success', 'deployment_step_failure'], MarathonEventsHandler.deployment_events_handler)
        except Exception, e:
            logger.exception(e)

    @classmethod
    def registry_event_handler(cls, evt_types, handler):
        for evt_type in evt_types:
            cls.registry[evt_type] = handler

    def deployment_events_handler(self):
        marathon_apps = map(MarathonApp, val_from_json(self.evt_data, 'plan.target.apps'))
        marathon = filter(lambda m: m.contains_ip(self.request.remote_ip), marathons)[0]
        logger.debug("Cache apps info for Marathon: {0}".format(marathon.id))
        cache.set_cache(marathon.cache_key, marathon_apps)

    @property
    def evt_data(self):
        return self.request.arguments

    @property
    def evt_type(self):
        return val_from_json(self.evt_data, 'eventType')

    def process_marathon_event(self):
        handler = self.registry.get(self.evt_type)

        if handler:
            logger.debug('Process marathon event: {0}'.format(self.evt_type))
            handler(self)
        else:
            logger.debug('Ignoring marathon event: {0}'.format(self.evt_type))

    def post(self):
        try:
            self.load_json()
            self.process_marathon_event()
        except Exception, e:
            logger.exception(e)
            print("Exception happened")

class MarathonAppsListHandler(BaseHandler):
    def get(self):
        if TEST:
            apps_ids = [['dev-currency-service', 'dev-cms'], ['sit-currency-service', 'sit-app1']]
        else:
            apps_ids = map(lambda m: m.ids_of_apps(), marathons)

        self.write_json(map(lambda app_id: {"name": app_id}, [x for y in apps_ids for x in y]))
