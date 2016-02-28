# -*- coding: utf-8 -*-

from handlers.index import IndexHandler
from handlers.command import CommandListHandler, CommandWSHandler
from handlers.share import ShareHandler

rest_patterns = [
    (r"/ws/invoke", CommandWSHandler),
    (r"/api/commands", CommandListHandler)
]

routes = [
    (r"/", IndexHandler),
    (r"/share/(.*)", ShareHandler)
]

url_patterns = rest_patterns + routes
