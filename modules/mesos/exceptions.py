# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

class MesosCLIException(Exception): pass

class FileDoesNotExist(MesosCLIException): pass

class MissingExecutor(MesosCLIException): pass

class SlaveDoesNotExist(MesosCLIException): pass

class SkipResult(MesosCLIException): pass
