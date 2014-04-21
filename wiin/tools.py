# -*- coding: utf-8 -*-
"""
.. module: tools
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import hashlib
import inspect
import json
import random
import sys
import urllib
import urlparse

from flask import request, session
from flask.ext.restless import ProcessingException

from wiin.init import db, app


CHARS = 'qwertyuiopasdfghjklzxcvbnm123456789QWERTYUIOPASDFGHJKLZXCVBNM'

app_access_token = "{0}|{1}".format(
    app.config.get('FACEBOOK')['consumer_key'],
    app.config.get('FACEBOOK')['consumer_secret']
)


def auth_func(*args, **kwargs):
    users = get_model('Users')
    access_token = request.values.get("access_token")

    # Less secure version
    user = users.query.filter_by(auth_key=access_token, active=True).first()

    # More secure version
    # uid = request.values.get("uid")
    # user = users.query.filter_by(auth_key=access_token, id=uid, active=True).first()

    if not user:
        raise ProcessingException(description='Not Authorized',
                                  code=401)


@app.route('/api/v1/login')
def api_login():
    return _fb_login()


def _fb_login():
    args = dict(client_id=app.config.get('FACEBOOK')['consumer_key'],
                redirect_uri=request.url, scope='user_groups,email')
    if request.args.get('code'):
        args["client_secret"] = app.config.get('FACEBOOK')['consumer_secret']
        args["code"] = request.args.get("code")
        response = urlparse.parse_qs(
            urllib.urlopen(
                "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)
            ).read()
        )
        access_token = response["access_token"][-1]
        profile = json.load(
            urllib.urlopen(
                "https://graph.facebook.com/me?" + urllib.urlencode(
                    dict(access_token=access_token)
                )
            )
        )
        users = get_model('Users')
        user = users.query.filter_by(fb_id=str(profile['id'])).first()

        if user:  # FB account already registred
            user.auth_key = access_token
        else:  # New FB account
            # Test is FB account's email already registred
            if users.query.filter_by(email=profile['email']).first():
                # Only uniqie emails are allowed, return error
                return json.dumps(
                    {
                        'status': False,
                        'code': 115,
                        'message': "This email already registred"}
                ), 409

            # E-mail is unique, create new user
            user = users(fb_id=str(profile["id"]), name=profile["name"], email=profile['email'],
                         auth_key=access_token)
            bind_brands_management(user)

        db.session.add(user)
        db.session.commit()
        return json.dumps({'status': True, 'access_token': access_token, 'uid': user.id})
    else:
        return json.dumps(
            {
                'auth_url': "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args)
            }
        )


@app.route('/api/v1/logout')
def api_logout():
    users = get_model('Users')
    access_token = request.values.get("access_token")
    user = users.query.filter_by(auth_key=access_token, active=True).first()
    if user:
        user.auth_key = None
        db.session.add(user)
        db.session.commit()
        res = {'status': True}
    else:
        res = {'status': False, 'message': "Not authenticated"}

    return json.dumps(res)


def get_model(model_name):
    mod = __import__('wiin.models', fromlist=['models'])
    model = getattr(mod, model_name, None)
    return model


def list_models():
    """
    Models generator

    :return: models generator
    :rtype: enumerate[flask.ext.sqlalchemy.SQLAlchemy]
    """
    classes = inspect.getmembers(sys.modules['wiin'].models)
    for name, cl in classes:
        if inspect.isclass(cl) and cl.__module__ == 'wiin.models' and issubclass(cl, db.Model):
            yield cl


def build_api(manager, version=1):
    """
    Build API endpoints for models

    :param manager: restfull manager instance
    :type manager: flask.ext.restless.APIManager
    :param version: API version
    :type version: int
    """
    for model in list_models():
        if hasattr(model, 'api_version') and version in model.api_version:
            kwargs = {}

            # list of columns, that should be responsed. By default - all fields responsed
            include_columns = getattr(model, 'include_columns', False)
            if include_columns:
                kwargs['include_columns'] = include_columns

            # list of fields, that should be hidden from response
            exclude_columns = getattr(model, 'exclude_columns', False)
            if exclude_columns:
                kwargs['exclude_columns'] = exclude_columns

            # Allow modify many records at once
            # PUT /api/v1/users {'email':'new@email.em'}
            allow_patch_many = getattr(model, 'allow_patch_many', False)
            kwargs['allow_patch_many'] = allow_patch_many

            # Available methods for this API endpoint
            # After development phase - leave just GET by default
            methods = getattr(model, 'methods', ['GET', 'POST', 'PUT', 'DELETE'])
            kwargs['methods'] = methods

            # List of preproccessors for endpoint. For details see
            # https://flask-restless.readthedocs.org/en/latest/customizing.html#request-preprocessors-and-postprocessors
            preprocessors = getattr(model, 'preprocessors', False)
            if preprocessors:
                kwargs['preprocessors'] = preprocessors

            manager.create_api(model, url_prefix='/api/v{0}'.format(version), **kwargs)


def random_string(l=16):
    s = ''
    for i in xrange(0, l):
        s += random.choice(CHARS)
    return s


def make_password(raw_password, salt=None):
    """
    Generate password for storing in db

    :param raw_password: raw password string
    :type raw_password: str|unicode
    :param salt: salt string for password. If not specified - will be generated new one
    :type salt: str|unicode
    :return: password string
    :rtype: str
    """
    if salt is None:
        salt = random_string(16)
    h = hashlib.sha256()
    h.update(raw_password)
    h.update(salt)
    h.update(app.config.get('SECRET_KEY'))
    return "sha256:{salt}:{hex}".format(salt=salt, hex=h.hexdigest())


def check_password(password_from_db, raw_string):
    _algo, salt, password_hash = password_from_db.split(':')
    password = make_password(raw_string, salt)
    return password == password_from_db


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = random_string(64)
    return session['_csrf_token']


def get_fb_groups(user):
    """
    Get user's facebook groups

    :param user: User instance
    :type user: wiin.models.Users
    :return: dict of list of groups with admin rights and without admin rights
    :rtype: dict[list]
    """
    data = json.load(
        urllib.urlopen(
            'https://graph.facebook.com/me/groups?access_token=%s' % user.auth_key
        )
    )
    data = data
    admins = []
    other = []
    while data:
        d = data['data']
        admins += [g for g in d if 'administrator' in g]
        other += [g for g in d if 'administrator' not in g]
        if 'paging' in data and 'next' in data['paging']:
            next_page = data['paging']['next']
            data = json.load(urllib.urlopen(next_page))
        else:
            data = None

    return {
        'admin': admins,
        'other': other
    }


def bind_brands_management(user):
    """
    Set user as manager for each fb brand-group, where he is admin

    :param user: user instance
    :type user: wiin.models.Users
    :return: count of brands, which for user is setted as admin
    :rtype: int
    """
    groups = get_fb_groups(user)
    brands_model = get_model('Brands')
    """:type: wiin.models.Brands"""
    i = 0
    for g in groups['other']:
        brand = brands_model.query.filter_by(fb_id=g['id'])
        brand = brand.first()
        """:type: wiin.models.Brands"""
        if brand:
            brand.managers.append(user)
            db.session.add(brand)
            i += 1
    return i

