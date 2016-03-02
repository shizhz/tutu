#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from config.config import TEST
from settings import settings
from urls import url_patterns
from handlers.marathon import registry_marathon_event_handler

class Tutu(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)

def main():
    http_server = tornado.httpserver.HTTPServer(Tutu())
    http_server.listen(options.port)

    ioloop = tornado.ioloop.IOLoop.instance()
    if not TEST:
        ioloop.add_timeout(ioloop.time(), registry_marathon_event_handler)

    ioloop.start()

if __name__ == "__main__":
    main()
