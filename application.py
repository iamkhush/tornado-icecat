#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from tornado import ioloop
from tornado.options import options
from monstor.app import make_app


settings = {
    'installed_apps': [
        'icecat',
    ],
    'cookie_secret': 'V9AiQHufNTdLSmPK',
    'template_path': os.path.join(os.getcwd(), 'templates')
}
application = make_app(**settings)

if __name__ == '__main__':
    application.listen(options.port, address=options.address)
    ioloop.IOLoop.instance().start()
