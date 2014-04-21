#!python2
# -*- coding: utf-8 -*-
"""
.. module: init_db
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wiin.models import *


def initial_data():
    m = [
        "INSERT INTO users (id, fb_id, password, name, email, created, auth_key, active, admin) VALUES (nextval('users_id_seq'), null, 'sha256:YxFYVQwg8bnk1HN4:d459bc969d0e231e0896568be9b4530d881b6b389a869fb72b4e5311d808b67f', 'admin', 'admin@admin.ad', '2014-04-21 17:22:03.528', null, true, true)"

    ]

    for i in m:
        try:
            db.engine.execute(i, bind='db1')
        except Exception as e:
            print e


if __name__ == "__main__":
    db.drop_all(bind='db1')
    db.create_all(bind='db1')
    initial_data()