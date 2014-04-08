# -*- coding: utf-8 -*-
"""
.. module: init
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import ConfigParser
import sys

from flask import Flask
from flask.ext import restful
import flask.ext.restless
from flask.ext.sqlalchemy import SQLAlchemy


prefix = getattr(sys, "prefix")
if prefix == '/user':
    prefix = '/'
config = ConfigParser.ConfigParser()
config.read(['wiin.cfg', prefix + '/etc/wiin.cfg'])

app = Flask(__name__)

app.config['SECRET_KEY'] = config.get('Main', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('Main', 'SQLALCHEMY_DATABASE_URI')
# noinspection PyArgumentList
app.config['SQLALCHEMY_BINDS'] = {
    'db1': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB1',
                      app.config['SQLALCHEMY_DATABASE_URI']),
    'db2': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB2'),
    'db3': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB3'),
    'db4': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB4'),
}
app.config['SQLALCHEMY_ECHO'] = config.get('Main', 'SQLALCHEMY_ECHO')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = config.get('Main', 'SQLALCHEMY_COMMIT_ON_TEARDOWN')
app.config['FACEBOOK'] = {
    'consumer_key': config.get('FACEBOOK', 'consumer_key'),
    'consumer_secret': config.get('FACEBOOK', 'consumer_secret')
}

try:
    from local_settings import *

    app.config.update(config)
except ImportError:
    pass

api = restful.Api(app)
db = SQLAlchemy(app)

manager = flask.ext.restless.APIManager(
    app, flask_sqlalchemy_db=db,
)
