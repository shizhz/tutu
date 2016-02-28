# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
from config.config import CACHE as c_config
from modules.cache.cache import SimpleDictCache

try:
    # init redis cache
    redis_config = c_config['redis']
except KeyError:
    CURRENT = SimpleDictCache()
