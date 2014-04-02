# -*- coding: utf-8 -*-
"""
.. module: models
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import datetime
from wiin.init import db


class Users(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'db1'

    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    name = db.Column(db.Unicode(300), nullable=False)
    email = db.Column(db.Unicode(254), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    auth_key = db.Column(db.Unicode(254))

    def __init__(self, name, email, auth_key):
        self.name = name
        self.email = email
        self.auth_key = auth_key
        self.created = datetime.datetime.now()
