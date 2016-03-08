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
            return filter(lambda app_id: all(map(lambda kw: kw in app_id, self.keywords)), apps_ids)
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

        for e in envs:
            apps_ids_in_env = filter(lambda app_id: app_id.upper().startswith(e['app-prefix'].upper()), apps_ids)
            if len(apps_ids_in_env):
                result += env_apps_tmpl.format(e['name'].upper(), ', '.join(apps_ids_in_env))

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

    DESC: Display detail information for provided apps. Set flag `full` to get verbose information, at least one <app_id> should be provided
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
 API-Gateway:
        {api_gateway}
 Task info: {task_info}
 Container info: {c_info} """.format(app.id, cpus=app.cpus, mem=app.mem, ins=app.instances, c_info=app.container_info(verbose=True), task_info=app.task_info(), a_addr=app.str_bamboo_address(), api_gateway=app.str_api_gateway_address())

    def short_info(self, app):
        return """
 App Id: {0}
 Bamboo address:
        {a_addr}
 API-Gateway:
        {api_gateway}
 Task info: {task_info}
 Container info: {c_info} """.format(app.id, c_info=app.container_info(verbose=False), task_info=app.task_info(), a_addr=app.str_bamboo_address(), api_gateway=app.str_api_gateway_address())

    def find_apps(self):
        def filter_by_kw(kw):
            def app_id_contains(app):
                return kw in app.id
            def app_id_endswith(app):
                return app.id.endswith(kw[:-1])
            def app_id_startswith(app):
                return app.id.startswith(kw[1:])

            return app_id_endswith if kw.endswith('$') else app_id_startswith if kw.startswith('^') else app_id_contains

        return filter(lambda app: any(map(lambda ta: filter_by_kw(ta)(app), self.target_apps)), itertools.chain.from_iterable(map(Marathon.apps, marathons)))

    def execute(self):
        apps = self.find_apps()

        if len(apps) == 0:
            return "No App found."

        return '\n'.join(map(lambda app: self.verbose_info(app) if self.verbose else self.short_info(app), apps))

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
