# -*- coding: utf-8 -*-
"""
.. module: init
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import ConfigParser
import sys

import os
from flask import Flask
from flask.ext import restful
from flask.ext.login import LoginManager
import flask.ext.restless
from flask.ext.sqlalchemy import SQLAlchemy


prefix = getattr(sys, "prefix")
if prefix == '/usr':
    prefix = ''

config = ConfigParser.ConfigParser(
    defaults={'DEBUG': 'False', 'SQLALCHEMY_ECHO': 'False'}
)
config.read(['wiin.cfg', prefix + '/etc/wiin.cfg'])

frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
templates_path = os.path.join(frontend_path, 'templates')
static_path = os.path.join(frontend_path, 'static')

app = Flask(__name__, template_folder=templates_path, static_folder=static_path,
            static_url_path='/static')

app.config['SECRET_KEY'] = config.get('Main', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('Main', 'SQLALCHEMY_DATABASE_URI')
# noinspection PyArgumentList
app.config['SQLALCHEMY_BINDS'] = {
    'db1': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB1',
                      app.config['SQLALCHEMY_DATABASE_URI']),
    # 'db2': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB2'),
    # 'db3': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB3'),
    # 'db4': config.get('Main', 'SQLALCHEMY_DATABASE_URI_DB4'),
}
app.config['SQLALCHEMY_ECHO'] = config.getboolean('Main', 'SQLALCHEMY_ECHO')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = config.getboolean(
    'Main', 'SQLALCHEMY_COMMIT_ON_TEARDOWN'
)
app.config['FACEBOOK'] = {
    'consumer_key': config.get('FACEBOOK', 'consumer_key'),
    'consumer_secret': config.get('FACEBOOK', 'consumer_secret'),
    'frontend_redirect_url': config.get('FACEBOOK', 'frontend_redirect_url'),
    'api_redirect_url': config.get('FACEBOOK', 'frontend_redirect_url'),
}

api = restful.Api(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

manager = flask.ext.restless.APIManager(
    app, flask_sqlalchemy_db=db,
)
