# -*- coding: utf-8 -*-

import paramiko
import contextlib
from paramiko.client import SSHClient
import logging

from models import CommandInfo
from cmd import Command, CommandContext, validator, cmd_indicator
from modules.mesos.marathon import marathon_of_env
from config.config import PUBKEY_LOCATION

logger = logging.getLogger('tutu.modules.command.' + __name__)

@contextlib.contextmanager
def ssh_client(*args, **kwargs):
    client = SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(*args, **kwargs)
    except Exception, e:
        logger.warn("Could not connect to remote host.")
        logger.exception(e)
        raise e
    try:
        yield client
    finally:
        logger.debug("Closing ssh connection with remote host: " + str(args))
        client.close()

class ShCommand(Command):
    """
    NAME: sh - execute shell command within application container on remote machine

    SYNOPSIS: sh [--env|-e <ENV>] <marathin_app_id> <raw bash command>

    DESC: execute shell within the specified application container and get the result, the target container will be found by marathon_app_id.\n

    You can also optionally specify target `ENV` by --env or -e

    NOTE: Please DO NOT use commands which never terminate automatically. like `tail -f`

    E.G. sh dev-some-service ls /opt/logs
         sh dev-some-service tail 200 /opt/logs/out.log
         sh --env dev some-service tail 200 /opt/logs/out.log
         sh -e prod some-service tail 200 /opt/logs/out.log
    """
    name = 'sh'
    alias = ['shell', 'bash']

    def __init__(self, env, marathon_app_id, sh):
        self.env = env
        self.marathon_app_id = marathon_app_id
        self.sh = sh
        self.notification = ""

    def cmd(self):
        if 'cat' == self.sh[0]:
            self.notification = 'Command `cat` has a very high possibility to cause the whole system blocked. Use `tail -n 100` instead.\n'
            return ' '.join(['tail -n 100'] + self.sh[1:])
        if 'tail' == self.sh[0] and '-f' in self.sh:
            self.notification = 'Drop option `-f` due to it will block the whole system for current implementation.\n'
            self.sh = filter(lambda cc: cc != '-f', self.sh)
        return ' '.join(self.sh)

    def cmd_to_parse_container_id(self, docker_image, exposed_port=None):
        if exposed_port:
            return "docker ps | grep -E '" + docker_image + ".*:" + str(exposed_port) + "' | awk '{print $1}'"
        else:
            return "docker ps | grep -E '" + docker_image + "' | awk '{print $1}'"

    def sh_in_docker(self, image_name, exposed_port=None):
        return 'docker exec `' + self.cmd_to_parse_container_id(image_name, exposed_port=exposed_port) + '` {cmd}'.format(cmd=self.cmd())

    def exec_sh_on_task(self, marathon_app, task):
        with ssh_client(task.host, username='root', key_filename=PUBKEY_LOCATION) as sc:
            cmd = self.sh_in_docker(marathon_app.docker_container_info().image, exposed_port=task.ports[0])
            logger.debug('Executing command : {0} on host: {1}'.format(cmd, task.host))
            stdin, stdout, stderr = sc.exec_command(cmd)

            out = stdout.readlines()
            err = stderr.readlines()

            if out:
                return self.notification + '\n\t'.join(out)
            elif err:
                return self.notification + """
        Something wrong happened while executing command: {0}:
                {1}""".format(self.cmd(), '\n\t'.join(err))

    def execute(self):
        marathon = marathon_of_env(self.env)
        apps = marathon.apps_by_id_contains(self.marathon_app_id)

        if len(apps) > 1:
            return 'More than one app found: {0}. Please choose the right one.'.format(map(lambda app: app.id, apps))

        marathon_app = apps[0]
        return '\n'.join(map(lambda t: self.exec_sh_on_task(marathon_app, t), marathon_app.tasks))

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
