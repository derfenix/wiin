# -*- coding: utf-8 -*-
"""
.. module: tools
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import inspect
import json
import sys
import urllib
import urlparse

from flask import request
from flask.ext.restless import ProcessingException

from wiin.init import db, app


def auth_func(*args, **kwargs):
    users = get_model('Users')
    access_token = request.values.get("access_token")

    # Less secure version
    user = users.query.filter_by(auth_key=access_token, active=True).first()

    # More secure version
    # uid = request.values.get("uid")
    # user = users.query.filter_by(auth_key=access_token, id=uid, active=True).first()

    if not user:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)


@app.route('/api/v1/login')
def login():
    args = dict(client_id=app.config.get('FACEBOOK')['consumer_key'],
                redirect_uri=request.url)
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
        if user:
            user.auth_key = access_token
        else:
            user = users(fb_id=str(profile["id"]), name=profile["name"], email=profile['email'],
                         auth_key=access_token, active=True)

        db.session.add(user)
        db.session.commit()
        return json.dumps({'status': True, 'access_token': access_token, 'uid': user.id})
    else:
        return json.dumps(
            {'auth_url': "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args)}
        )


@app.route('/api/v1/logout')
def logout():
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

            include_columns = getattr(model, 'include_columns', False)
            if include_columns:
                kwargs['include_columns'] = include_columns

            exclude_columns = getattr(model, 'exclude_columns', False)
            if exclude_columns:
                kwargs['exclude_columns'] = exclude_columns

            allow_patch_many = getattr(model, 'allow_patch_many', False)
            kwargs['allow_patch_many'] = allow_patch_many

            methods = getattr(model, 'methods', ['GET'])
            kwargs['methods'] = methods

            preprocessors = getattr(model, 'preprocessors', False)
            if preprocessors:
                kwargs['preprocessors'] = preprocessors

            manager.create_api(model, url_prefix='/api/v{0}'.format(version), **kwargs)

