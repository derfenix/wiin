# -*- coding: utf-8 -*-
"""
.. module: server
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wiin.init import manager, app

# noinspection PyUnresolvedReferences
import wiin.models
from wiin.tools import build_api

manager = build_api(manager)

if __name__ == "__main__":
    app.run(debug=True)