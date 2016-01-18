# -*- coding: utf-8 -*-

class Command(object):
    def execute(self, context, **kwargs):
        pass

class CommandInfo(object):
    def __init__(self, command, **kwargs):
        self.command = command
        self.__dict__.update(kwargs)
