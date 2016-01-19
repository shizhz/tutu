# -*- coding: utf-8 -*-

class CommandException(Exception): 
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg

class UnknownCommandException(CommandException): pass

class InvalidParserParameterException(CommandException): pass

class InvalidCommandException(CommandException): pass
