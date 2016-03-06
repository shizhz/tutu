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

    SYNOPSIS: apps <keywords>

    DESC: list all apps whose id include keywords. If <keywords> is not presented, list all apps in all environments
    """
    name = 'apps'
    alias = []

    def __init__(self, keywords=None):
        self.keywords = keywords

    def filter_apps_by_keywords(self):
        apps_ids = map(lambda app: app.id, itertools.chain.from_iterable(map(Marathon.apps, marathons)))
        if self.keywords:
            return filter(lambda app_id: all([map(lambda kw: kw in app_id)]), apps_ids)
        else:
            return apps_ids

    def execute(self):
        apps_ids = self.filter_apps_by_keywords()

        if not apps_ids:
            return "No apps found!"

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
        return self.support(txt)

    def parse(self, txt):
        if len(txt.split()) >= 2:
            return AppsCommand(keywords=txt.split()[1:])
        else:
            return AppsCommand()

class AppInfoCommand(Command):
    """
    NAME: appinfo

    SYNOPSIS: appinfo <app_id> <app_id> <full>

    DESC: Display detail information for provided apps. Set flag `full` to get verbose information
    """

    name = 'appinfo'
    alias = ['ai']

    def __init__(self, target_apps, verbose=False):
        self.target_apps = target_apps
        self.verbose = verbose

    def verbose_info(self, app):
        return """
 App Id: {0}
 Cpus: {cpus}
 Mem: {mem}M
 Instances: {ins}
 Bamboo address:
        {a_addr}
 Task info: {task_info}
 Container info: {c_info} """.format(app.id, cpus=app.cpus, mem=app.mem, ins=app.instances, c_info=app.container_info(), task_info=app.task_info(), a_addr=app.access_address())

    def short_info(self, app):
        return """
 App Id: {0}
 Bamboo address:
        {a_addr}
 Task info: {task_info}
 Container info: {c_info} """.format(app.id, c_info=app.container_info(), task_info=app.task_info(), a_addr=app.access_address())


    def execute(self):
        apps = filter(lambda app: app.id in self.target_apps, itertools.chain.from_iterable(map(Marathon.apps, marathons)))
        apps_ids = map(lambda app: app.id, apps)
        result = []
        for app_id in self.target_apps:
            if app_id in apps_ids:
                app = filter(lambda a: a.id == app_id, apps)[0]
                if self.verbose:
                    result.append(self.verbose_info(app))
                else:
                    result.append(self.short_info(app))
            else:
                result.append('App Id: {0} - Info not found'.format(app_id))

        return '\n'.join(result)

class AppInfoCommandParser(object):
    support = cmd_indicator(AppInfoCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt) and len(txt.split()) >= 2

    def parse(self, txt):
        cmd_segs = txt.lower().split()
        if 'full' in cmd_segs[1:]:
            return AppInfoCommand([c for c in cmd_segs[1:] if c != 'full'], verbose=True)
        else:
            return AppInfoCommand(txt.split()[1:])
