# -*- coding: utf-8 -*-

from models import CommandInfo
from cmd import Command, CommandContext, validator, cmd_indicator

class ShCommand(Command):
    """
    NAME: sh - execute shell command within application container on remote machine

    SYNOPSIS: sh [--env|-e <ENV>] <marathin_app_id> <raw bash command>

    DESC: execute shell within the specified application container and get the result, the target container will be found by marathon_app_id.\n

    You can also optionally specify target `ENV` by --env or -e

    E.G. sh dev-some-service ls /opt/logs
         sh dev-some-service tail -n 200 /opt/logs/out.log
         sh --env dev some-service tail -n 200 /opt/logs/out.log
         sh -e prod some-service tail -n 200 /opt/logs/out.log
    """
    name = 'sh'
    alias = ['shell', 'bash']

    def __init__(self, env, marathon_app_id, sh):
        self.env = env
        self.marathon_app_id = marathon_app_id
        self.sh = sh

    def execute(self, context):
        pass

class ShCommandParser(object):
    support = cmd_indicator(ShCommand)

    def has_env_option(self, txt):
        cmd_segs = txt.split()
        return '-e' == cmd_segs[1].lower() or '--env' == cmd_segs[1].lower()

    def parse_env(self, txt):
        cmd_segs = txt.split()

        def parse_by_arg():
            if self.has_env_option(txt):
                return cmd_segs[2]

        def parse_by_app_id():
            app_id_index = 1 + (2 if self.has_env_option(txt) else 0)
            app_id = cmd_segs[app_id_index]
            return app_id.split('-')[0]

        return parse_by_arg() or parse_by_app_id()

    def parse_marathon_app_id(self, txt):
        cmd_segs = txt.split()

        return cmd_segs[3] if self.has_env_option(txt) else cmd_segs[1]

    def parse_remote_sh(self, txt):
        cmd_segs = txt.split()

        return cmd_segs[4:] if self.has_env_option(txt) else cmd_segs[2:]

    @validator
    def is_valid(self, txt):
        cmd_segs = txt.split()
        return self.support(txt) and (len(cmd_segs) >= 5 if self.has_env_option(txt) else len(cmd_segs) >= 3)

    def parse(self, txt):
        """
        sh command should be the format like:
        - sh dev-some-service ls /opt/logs
        - sh dev-some-service tail -f /opt/logs/out.log
        - sh -e dev some-service tail -f /opt/logs/out.log
        """
        env = self.parse_env(txt)
        marathon_app_id = self.parse_marathon_app_id(txt)
        sh = self.parse_remote_sh(txt)
        return ShCommand(env, marathon_app_id, sh)

class ShCommandContext(CommandContext):
    def __init__(self, env, marathon_app_id):
        self.env = env
        self.marathon_app_id = marathon_app_id

    def enter(self):
        # TODO: Return a open connection to remote machine
        return self

    def exit(self, type, value, traceback):
        # TODO: Close connection
        pass
