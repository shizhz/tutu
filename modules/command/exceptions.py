# -*- coding: utf-8 -*-

class CommandException(Exception): 
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg

class UnknownCommandException(CommandException):
    def __init__(self, cmd):
       super(UnknownCommandException, self).__init__('Unknown Command: ' + cmd)

class SharedCommandExpiredException(CommandException): pass

class InvalidParserParameterException(CommandException): pass

class InvalidCommandException(CommandException): pass
