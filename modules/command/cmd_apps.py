# -*- coding: utf-8 -*-

from __future__ import print_function

import itertools
import logging

from config.config import CACHE as cache_cfg, envs, env_config_of
from modules.cache import CURRENT as cache
from cmd import Command, validator, cmd_indicator
from modules.mesos.marathon import marathon_of_env, marathons, Marathon

logger = logging.getLogger('tutu.modules.command.' + __name__)

class AppsCommand(Command):
    """
    NAME: apps

    SYNOPSIS: apps <env>

    DESC: list all apps, <env> is optional
    """
    name = 'apps'
    alias = []

    def __init__(self, env=None):
        self.env = env

    def _env_app_prefixes(self):
        env_config = env_config_of(self.env)

        return [env_config_of['app-prefix']] if env_config else map(lambda e: e['app-prefix'], envs)

    def execute(self):
        ms = filter(lambda a: a, [marathon_of_env(self.env)] if self.env else marathons)

        apps = map(Marathon.apps, ms)
        apps_ids = map(lambda app: app.id, itertools.chain.from_iterable(apps))

        if self.env:
            apps_ids = filter(lambda app_id: app_id.startswith(self.env), apps_ids)

        apps_group = map(lambda app_prefix: filter(lambda app_id: app_id.upper().startswith(app_prefix.upper()), app_ids), self._env_app_prefixes())

        result = ', '.join(apps_ids)

        return result if result else "No environment found: " + self.env

class AppsCommandParser(object):
    support = cmd_indicator(AppsCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) <= 2

    def parse(self, txt):
        if len(txt.split()) == 2:
            return AppsCommand(env=txt.split()[-1])
        else:
            return AppsCommand()

