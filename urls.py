# -*- coding: utf-8 -*-

from handlers.index import IndexHandler
from handlers.command import CommandHandler, CommandListHandler
from handlers.share import ShareHandler

rest_patterns = [
    (r"/api/commands", CommandListHandler),
]

routes = [
    (r"/", IndexHandler),
    (r"/invoke", CommandHandler),
    (r"/share", ShareHandler)
]

url_patterns = rest_patterns + routes
