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

    def envs(self):
        return [env_config_of(self.env)] if self.env else envs

    def is_env_valid(self):
        return bool(env_config_of(self.env)) if self.env else True

    def execute(self):
        if not self.is_env_valid():
            return "Invalid environment: {0}. Available environments are: {1}".format(self.env, ', '.join(map(lambda e: e['name'], envs)))

        ms = filter(lambda a: a, [marathon_of_env(self.env)] if self.env else marathons)
        apps_ids = map(lambda app: app.id, itertools.chain.from_iterable(map(Marathon.apps, ms)))

        env_apps_tmpl = """
Environment - {0}:
  {1}
        """

        result = ""

        for e in self.envs():
            result += env_apps_tmpl.format(e['name'].upper(), ', '.join(filter(lambda app_id: app_id.upper().startswith(e['app-prefix'].upper()), apps_ids)))

        return result

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

class AppInfoCommand(Command):
    """
    NAME: appinfo

    SYNOPSIS: appinfo <app_id> <app_id>

    DESC: Display detail information for provided apps
    """

    name = 'appinfo'
    alias = ['ai']

    def __init__(self, target_apps):
        self.target_apps = target_apps

    def execute(self):
        apps = filter(lambda app: app.id in self.target_apps, itertools.chain.from_iterable(map(Marathon.apps, marathons)))
        apps_ids = map(lambda app: app.id, apps)
        result = []
        for app_id in self.target_apps:
            if app_id in apps_ids:
                app = filter(lambda a: a.id == app_id, apps)[0]
                app_info = "App Id: {0}".format(app.id)
                result.append("""
 App Id: {0}
 Cpus: {cpus}
 Mem: {mem}M
 Instances: {ins}
 Bamboo address:
        {a_addr}
 Task info: {task_info}
 Container info: {c_info} """.format(app.id, cpus=app.cpus, mem=app.mem, ins=app.instances, c_info=app.container_info(), task_info=app.task_info(), a_addr=app.access_address()))
            else:
                result.append('App Id: {0} - Info not found'.format(app_id))

        return '\n'.join(result)

class AppInfoCommandParser(object):
    support = cmd_indicator(AppInfoCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) >= 2

    def parse(self, txt):
        return AppInfoCommand(txt.split()[1:])