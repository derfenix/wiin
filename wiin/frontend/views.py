# -*- coding: utf-8 -*-
"""
.. module: views
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""

from flask import render_template, flash, redirect
from flask.ext.login import current_user, login_user
from flask.globals import request

from wiin.frontend.auth import User
from wiin.frontend.forms import LoginForm, RegistrationForm
from wiin.init import app
from wiin.tools import make_password


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        password = make_password(form.password.data)
        email = form.email.data
        user = User.authenticate(email, password)
        if user:
            login_user(user)
            flash('Login successful')
            return redirect('/')
        else:
            flash('Login failed!')
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User.create(form)
        login_user(user)

    return render_template('registration.html', form=form)