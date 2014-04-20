# -*- coding: utf-8 -*-
"""
.. module: views
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import json

from flask import render_template, flash, redirect
from flask.ext.login import login_user
from flask.globals import request
from flask.helpers import url_for

from wiin.frontend.auth import User
from wiin.frontend.forms import LoginForm, RegistrationForm
from wiin.init import app
from wiin.tools import _fb_login


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        user = User.authenticate(email, password)
        if user:
            login_user(user)
            flash('Login successful')
            return redirect('/')
        else:
            flash('Login failed!')
    return render_template('login.html', form=form)


@app.route('/fblogin')
def fb_login():
    response = json.loads(_fb_login())
    print response
    if 'auth_url' in response:
        return redirect(response['auth_url'])
    elif 'access_token' in response:
        uid = response['uid']
        user = User.get(uid)
        login_user(user)
        return redirect('/')
    else:
        return '', 500


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User.create(form)
        login_user(user)
        return redirect(url_for('login'))

    return render_template('registration.html', form=form)