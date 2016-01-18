# -*- coding: utf-8 -*-

from handlers.index import IndexHandler

url_patterns = [
    (r"/", IndexHandler),
]
