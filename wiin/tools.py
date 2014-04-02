# -*- coding: utf-8 -*-
"""
.. module: tools
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import inspect
import sys

from wiin.init import db


def auth_func(*args, **kwargs):
    # if not current_user.is_authenticated():
    #     raise ProcessingException(description='Not authenticated!', code=401)
    return True


def list_models():
    classes = inspect.getmembers(sys.modules['wiin'].models)
    for name, cl in classes:
        if inspect.isclass(cl) and cl.__module__ == 'wiin.models' and issubclass(cl, db.Model):
            yield cl


def build_api(manager, version=1):
    for model in list_models():
        if version in model.api_version:
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

    return manager