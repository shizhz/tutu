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
        marathon_app_id = cmd_segs[1]
        remote_cmd = cmd_segs[2:]

        return CommandInfo(cmd, marathon_app_id=marathon_app_id, remote_cmd=remote_cmd)
