# -*- coding: utf-8 -*-

from handlers.index import IndexHandler
from handlers.command import CommandHandler
from handlers.share import ShareHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/invoke", CommandHandler),
    (r"/share", ShareHandler)
]
