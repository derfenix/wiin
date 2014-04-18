#!python2
# -*- coding: utf-8 -*-
"""
.. module: init_db
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wiin.models import *


def migration1():
    db.engine.execute("ALTER TABLE users ADD password VARCHAR(90)", bind='db1')

if __name__ == "__main__":
    db.create_all(bind='db1')
    migration1()