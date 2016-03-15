# -*- coding: utf-8 -*-

from __future__ import print_function

import logging

from config.config import CACHE as cache_cfg, envs, env_config_of
from modules.util import flat_list
from modules.cache import CURRENT as cache
from cmd import Command, validator, cmd_indicator
from modules.mesos.marathon import marathon_of_env, marathons, Marathon

logger = logging.getLogger('tutu.modules.command.' + __name__)

def find_apps_by_id_patterns(patterns):
    return flat_list(map(lambda m: m.apps_by_id_patterns(patterns), marathons))

class AppsCommand(Command):
    """
    NAME: apps

    SYNOPSIS: apps <pattern>

    DESC: list all apps whose id matches provided pattern. If <pattern> is not presented, list all apps in all environments
    """
    name = 'apps'
    alias = []

    def __init__(self, app_id_pattern=['.*']):
        self.app_id_pattern = app_id_pattern

    def execute(self):
        apps = find_apps_by_id_patterns(self.app_id_pattern)

        if not apps:
            return "No apps found!"

        env_apps_tmpl = """
Environment - {0}:
  {1}
        """

        result = ""

        for e in envs:
            apps_in_env = filter(lambda app: app.id.upper().startswith(e['app-prefix'].upper()), apps)
            if len(apps_in_env):
                result += env_apps_tmpl.format(e['name'].upper(), ', '.join(map(lambda app: app.id, apps_in_env)))

        env_prefixes = map(lambda env: env['app-prefix'].upper(), envs)
        others = filter(lambda app: all(map(lambda env_prefix: not app.id.upper().startswith(env_prefix), env_prefixes)), apps)

        if len(others):
            result += """
Environment - Others:
  {0}
            """.format(', '.join(map(lambda o: o.id, others)))

        return result if result else "No apps found according current app-prefix for each environment"

class AppsCommandParser(object):
    support = cmd_indicator(AppsCommand)

    @validator
    def is_valid(self, txt):
        return self.support(txt)

    def parse(self, txt):
        if len(txt.split()) >= 2:
            return AppsCommand(app_id_pattern=txt.split()[1:])
        else:
            return AppsCommand()

class AppInfoCommand(Command):
    """
    NAME: appinfo(ai)

    SYNOPSIS: appinfo <pattern> <pattern> <full>

    DESC: Display detail information for provided apps. Set flag `full` to get verbose information, at least one <pattern> should be provided
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

    def execute(self):
        apps = find_apps_by_id_patterns(self.target_apps)

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
