# -*- coding: utf-8 -*-

from models import CommandInfo

class ShCommandParser(object):
    def support(self, text):
        return text.startswith("sh")

    def parse(self, text):
        """
        sh command should be the format like:
        - sh dev-some-service ls /opt/logs
        - sh dev-some-service tail -f /opt/logs/out.log
        """
        cmd_segs = text.split()
        cmd = cmd_segs[0]
        marathon_app_id = cmd_segs[1] if len(cmd_segs) >= 2 else None
        remote_cmd = cmd_segs[2:] if len(cmd_segs) >= 3 else None

        return CommandInfo(cmd, marathon_app_id=marathon_app_id, remote_cmd=remote_cmd, help=self.help())

    def help(self):
        return """
        NAME: sh - execute shell command within application container on remote machine
        SYNOPSIS: sh <marathin_app_id> <raw bash command>
        DESC: execute shell within the specified application container and get the result, the target container will be found by marathon_app_id.\n
        E.G. sh dev-some-service ls /opt/logs
             sh dev-some-service tail -n 200 /opt/logs/out.log
        """
