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

class ZookeeperConnectionException(Exception):pass

class AppNotFoundException(MarathonException):
    def __init__(self, app_id):
        self.msg = 'App not found with id contains: {0}'.format(app_id)
        self.app_id = app_id

