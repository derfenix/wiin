# -*- coding: utf-8 -*-
"""
.. module: views
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""

from flask import render_template, flash, redirect
from flask.ext.login import current_user
from flask.globals import request

from wiin.frontend.forms import LoginForm
from wiin.init import app


@app.route('/')
def index():
    print current_user
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            flash('Login requested for OpenID=')
            return redirect('/')
        else:
            flash('Login failed!')
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    pass