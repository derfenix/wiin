#!python2
# -*- coding: utf-8 -*-
"""
.. module: server
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wiin.init import manager, config

# noinspection PyUnresolvedReferences
import wiin.models
from wiin.tools import build_api
# noinspection PyUnresolvedReferences
from wiin.frontend.views import *
import sys

build_api(manager)

host = None
port = None
if len(sys.argv) > 1:
    if len(sys.argv) >= 2:
        host = sys.argv[1]

        if len(sys.argv) >= 3:
            port = int(sys.argv[2])

if __name__ == "__main__":
    app.run(host=host, port=port, debug=config.getboolean('Main', 'DEBUG'))