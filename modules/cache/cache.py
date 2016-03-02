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

    def is_cached(self, key):
        return self.get_cache(key) is not None

    def get_cache_by_key_prefix(self, key_prefix):
        result = {}
        for key in self.__class__.bucket.keys():
            if key.startswith(key_prefix):
                result[key] = self.get_cache(key)

        return result
