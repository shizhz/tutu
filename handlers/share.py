# -*- coding: utf-8 -*-

from handlers.base import BaseHandler

class ShareHandler(BaseHandler):
    """
    Handling all sharing links
    """
    def get(self, share_code):
        self.set_cookie('share_code', share_code)
        self.redirect('/')
