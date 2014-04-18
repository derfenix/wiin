# -*- coding: utf-8 -*-
"""
.. module: auth
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from flask.ext.login import UserMixin

from wiin.models import Users
from wiin.init import login_manager, db

from wiin.tools import make_password, check_password


class User(UserMixin):
    def __init__(self, u):
        self.id = u.id
        self.email = u.email
        self.name = u.name
        self.active = u.active

    def is_active(self):
        return self.active

    @staticmethod
    def get(userid):
        user = Users.query.filter_by(id=userid).first()
        return User(user)

    @staticmethod
    def authenticate(email, password):
        user = Users.query.filter_by(email=email).first()

        if not user:
            return None

        if not check_password(user.password, password):
            return None

        return User(user)

    @staticmethod
    def email_registred(email):
        user = Users.query.with_entities(Users.id).filter_by(email=email).first()
        return user

    @staticmethod
    def create(form):
        password = make_password(form.password.data)
        user = Users(email=form.email.data, name=form.name.data, password=password)
        db.session.add(user)
        db.session.commit()
        return user


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)