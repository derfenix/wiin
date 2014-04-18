# -*- coding: utf-8 -*-
"""
.. module: forms
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from flask.ext.wtf import Form

from wtforms.fields.simple import TextField, PasswordField
from wtforms.validators import Email, Required, Length, EqualTo
from wiin.frontend.auth import User


class LoginForm(Form):
    email = TextField('email', validators=[Email(), Required(), Length(max=254)])
    password = PasswordField('password', validators=[Required(), Length(min=5, max=300)])


class RegistrationForm(Form):
    name = TextField('name', validators=[Required(), Length(max=300)])
    email = TextField('email', validators=[Email(), Required(), Length(max=254)])
    password = PasswordField('password', validators=[Required(), Length(min=5, max=300)])
    password2 = PasswordField('password2',
                              validators=[
                                  Required(), EqualTo('password', "Passwords must be identical")
                              ])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if User.email_registred(self.email.data).first():
            self.email.errors.append('Email already registred!')
            return False