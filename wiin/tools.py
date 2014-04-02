# -*- coding: utf-8 -*-
"""
.. module: tools
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import inspect
import sys
from wiin.init import db


def list_models():
    classes = inspect.getmembers(sys.modules['wiin'].models)
    for name, cl in classes:
        if inspect.isclass(cl) and cl.__module__ == 'wiin.models' and issubclass(cl, db.Model):
            yield cl


def build_api(manager):
    for model in list_models():
        manager.create_api(model, methods=['GET', 'POST', 'DELETE'])

    return manager