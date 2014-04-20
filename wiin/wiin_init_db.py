#!python2
# -*- coding: utf-8 -*-
"""
.. module: init_db
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wiin.models import *


def migration1():
    m = [
        "ALTER TABLE users ADD password VARCHAR(90)",
        "ALTER TABLE users ALTER COLUMN fb_id DROP NOT NULL",
        "ALTER TABLE users ALTER COLUMN auth_key DROP NOT NULL",
    ]

    for i in m:
        try:
            db.engine.execute(i, bind='db1')
        except Exception as e:
            print e


if __name__ == "__main__":
    db.create_all(bind='db1')
    migration1()