# -*- coding: utf-8 -*-

import itertools
import logging

from config.config import CACHE as cache_cfg
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

    def execute(self):
        ms = [marathon_of_env(self.env)] if self.env else marathons
        apps = map(Marathon.apps, ms)
        return ', '.join(map(lambda app: app.id, itertools.chain.from_iterable(apps)))

class AppsCommandParser(object):
    support = cmd_indicator(AppsCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) <= 2

    def parse(self, txt):
        if txt.split() == 2:
            return AppsCommand(txt.split()[-1])
        else:
            return AppsCommand()

