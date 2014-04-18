# -*- coding: utf-8 -*-
"""
.. module: forms
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
from wtforms import Form
from wtforms.fields.simple import TextField, PasswordField
from wtforms.validators import Email, Required, Length


class LoginForm(Form):
    email = TextField('email', validators=[Email(), Required()])
    password = PasswordField('password', validators=[Required(), Length(min=5, max=300)])