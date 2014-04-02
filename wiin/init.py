# -*- coding: utf-8 -*-
"""
.. module: init
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from flask import Flask
from flask.ext import restful
import flask.ext.restless
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://db_user:db_pw@localhost:5432/db_name'

app.config['SQLALCHEMY_BINDS'] = {
    'db1': app.config['SQLALCHEMY_DATABASE_URI'],
}

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

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
