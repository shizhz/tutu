# -*- coding: utf-8 -*-

from handlers.index import IndexHandler
from handlers.command import CommandListHandler, CommandWSHandler
from handlers.share import ShareHandler
from handlers.marathon import MarathonEventsHandler, MarathonAppsListHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/share/(.*)", ShareHandler),
    (r"/ws/invoke", CommandWSHandler),
    (r"/api/commands", CommandListHandler),
    (r"/api/marathon/apps", MarathonAppsListHandler),
    (r"/api/marathon/callback", MarathonEventsHandler),
]
