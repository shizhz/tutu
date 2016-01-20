# -*- coding: utf-8 -*-

from exceptions import InvalidParserParameterException, InvalidCommandException

class Command(object):
    """
    Abstract of all commands Tutu knows
    """
    def execute(self, context):
        """
        Execute this command within context
        """
        pass

    @classmethod
    def help_info(cls):
        if cls.__doc__ == Command.__doc__:
            return "No help info"
        else:
            return cls.__doc__

class CommandContext(object):
    def __enter__(self):
        return self.enter() # define method `enter` in all subclass

    def __exit__(self, type, value, traceback):
        self.exit(self, type, value, traceback) # define method `exit` in all subclass

def validator(fn):
    """
    This decorator is limited for `is_valid` method for parsers,
    which always accepts two parameters:
    - The first one: the bound instance
    - The second one: the text to be parsed
    """
    def w(*args):
        if len(args) < 2:
            raise InvalidParserParameterException(args)
        txt = args[1]

        if not txt or not isinstance(txt, str):
            raise InvalidParserParameterException(txt)

        if not fn(args[0], txt.strip()):
            raise InvalidCommandException(txt)

        return True
    return w

def cmd_indicator(command):
    def indicator(txt):
        cmd = txt.split()[0]
        alias = command.alias or []
        name = command.name

        valid_names = alias.append(name)

        return cmd in valid_names

    return indicator
