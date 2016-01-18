from handlers.base import BaseHandler

import logging
logger = logging.getLogger('tutu.' + __name__)


class IndexHandler(BaseHandler):
    def get(self):
        logger.debug("Rendering index.html")
        self.render("index.html")
