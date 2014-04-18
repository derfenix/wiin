# -*- coding: utf-8 -*-
"""
.. module: auth
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from flask.ext.login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.login_view = 'frontend.views.login'


class User(UserMixin):
    def __init__(self, uid):
        self.id = uid

    @staticmethod
    def get(userid):
        return User(userid)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)