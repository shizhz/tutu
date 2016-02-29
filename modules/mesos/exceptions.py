# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

class MesosCLIException(Exception): pass

class FileDoesNotExist(MesosCLIException): pass

class MissingExecutor(MesosCLIException): pass

class SlaveDoesNotExist(MesosCLIException): pass

class SkipResult(MesosCLIException): pass

class MarathonException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg

    def __str__(self):
        return self.msg

class MarathonConnectionException(MarathonException):
    def __init__(self, msg):
        MarathonException.__init__(self, msg)

class AppNotFoundException(MarathonException):
    def __init__(self, app_id):
        self.app_id = app_id

