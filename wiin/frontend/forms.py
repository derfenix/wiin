# -*- coding: utf-8 -*-
"""
.. module: forms
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import datetime

from flask.ext.wtf import Form
from wtforms.fields.html5 import URLField, DateTimeField
from wtforms.fields.simple import TextField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import Email, Required, Length, EqualTo, Optional
from wtforms.widgets.core import PasswordInput

from wiin.frontend.auth import User


class LoginForm(Form):
    email = TextField('email', validators=[Email(), Required(), Length(max=254)])
    password = PasswordField('password', validators=[Required(), Length(min=5, max=300)],
                             widget=PasswordInput(False))


class RegistrationForm(Form):
    name = TextField('name', validators=[Required(), Length(max=300)])
    email = TextField('email', validators=[Email(), Required(), Length(max=254)])
    password = PasswordField('password', validators=[Required(), Length(min=5, max=300)],
                             widget=PasswordInput(False))
    password2 = PasswordField('password2',
                              validators=[
                                  Required(), EqualTo('password', "Passwords must be identical")
                              ], widget=PasswordInput(False))

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if User.email_registred(self.email.data):
            self.email.errors.append('Email already registred!')
            return False
        return True


class NewPostForm(Form):
    id = HiddenField()
    title = TextField('Title', validators=[Length(min=3, max=500)])
    text = TextAreaField('Text', validators=[Required(), ])
    url = URLField('URL')
    image_url = URLField('Image URL')
    publish_date = DateTimeField("Publish at date", default=datetime.datetime.now())


class NewBrandForm(Form):
    id = HiddenField()
    name = TextField('Name', validators=[Required(), Length(min=2, max=300)])
    hashtags = TextField('Brand hash tags', validators=[Optional()])
    profile_img_url = URLField("Add profile picture")
    cover_img_url = URLField("Add cover picture")