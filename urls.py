# -*- coding: utf-8 -*-

from handlers.index import IndexHandler
from handlers.command import CommandHandler, CommandListHandler
from handlers.share import ShareHandler

rest_patterns = [
    (r"/api/commands", CommandListHandler),
    (r"/api/invoke", CommandHandler),
    (r"/api/share", ShareHandler)
]

routes = [
    (r"/", IndexHandler),
]

url_patterns = rest_patterns + routes
