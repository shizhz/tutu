# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import string
import random

class Cache(object):
    pass

class SimpleDictCache(Cache):
    bucket = {}

    def set_cache(self, key, value):
        self.__class__.bucket[key] = value

    def get_cache(self, key, default=None):
        try:
            return self.__class__.bucket[key]
        except KeyError:
            return default
