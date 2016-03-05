# -*- coding: utf-8 -*-

from handlers.base import BaseHandler

import logging

logger = logging.getLogger('tutu.' + __name__)

class IndexHandler(BaseHandler):
    def get(self):
        self.render_jinja2("index.html")
