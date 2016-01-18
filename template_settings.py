# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from settings import TEMPLATE_ROOT as template_root
import logging
logger = logging.getLogger('tutu.' + __name__)

class Jinja2TemplateRender(object):
    def render_template(self, temp_name, **kwargs):
        logger.debug("Rendering %s with jinja2 template engine", temp_name)
        env = Environment(loader=FileSystemLoader([template_root]))
        try:
            template = env.get_template(temp_name)
        except TemplateNotFound:
            raise TemplateNotFound(temp_name)
        return template.render(kwargs)

