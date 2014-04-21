# -*- coding: utf-8 -*-
"""
.. module: models
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import datetime

from flask.ext.login import current_user
from flask.ext.security import UserMixin

from wiin.init import db
from wiin.tools import auth_func


brand_likes = db.Table(
    'brand_likes',
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    info={'bind_key': 'db1'}
)

brand_follows = db.Table(
    'brand_follows',
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    info={'bind_key': 'db1'}
)

brands_managers = db.Table(
    'brands_managers',
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    info={'bind_key': 'db1'}
)

posts_likes = db.Table(
    'posts_likes',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    info={'bind_key': 'db1'}
)

posts_links_followed = db.Table(
    'posts_links_followed',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    info={'bind_key': 'db1'}
)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    __bind_key__ = 'db1'
    api_version = (1,)
    preprocessors = {'GET_MANY': [auth_func], 'GET_SINGLE': [auth_func],
                     'PUT_SINGLE': [auth_func], 'PUT_MANY': [auth_func],
                     'POST': [auth_func], "DELETE": [auth_func]}
    exclude_columns = ('password', 'auth_key')

    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    fb_id = db.Column(db.Unicode(255), nullable=True, unique=True)
    password = db.Column(db.String(88), nullable=True)
    name = db.Column(db.Unicode(300), nullable=False)
    email = db.Column(db.Unicode(254), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    auth_key = db.Column(db.Unicode(254))
    active = db.Column(db.Boolean())
    admin = db.Column(db.Boolean(), default=False)
    brands_likes = db.relationship(
        'Brands', secondary=brand_likes, backref=db.backref('users_likes', lazy='dynamic'),
        lazy='dynamic'
    )
    brands_follows = db.relationship(
        'Brands', secondary=brand_follows, backref=db.backref('users_follows', lazy='dynamic'),
        lazy='dynamic'
    )
    brands_manage = db.relationship(
        'Brands', secondary=brands_managers, backref=db.backref('managers', lazy='dynamic'),
        lazy='dynamic'
    )
    posts_likes = db.relationship(
        'Posts', secondary=posts_likes, backref=db.backref('users_likes', lazy='dynamic'),
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comments', backref='user', lazy='dynamic'
    )

    def __init__(self, name, email, auth_key=None, fb_id=None, password=None):
        self.fb_id = fb_id
        self.name = name
        self.email = email
        self.password = password
        self.auth_key = auth_key
        self.active = True
        self.created = datetime.datetime.now()


class Brands(db.Model):
    __tablename__ = 'brands'
    __bind_key__ = 'db1'
    api_version = (1,)
    exclude_columns = (
        'posts', 'users_likes', 'users_follows', 'managers.auth_key',
        'managers.password', 'users_likes.password', 'users_likes.auth_key',
        'users_follows.auth_key', 'users_follows.password'
    )
    preprocessors = {'GET_MANY': [auth_func], 'GET_SINGLE': [auth_func],
                     'PUT_SINGLE': [auth_func], 'PUT_MANY': [auth_func],
                     'POST': [auth_func], "DELETE": [auth_func]}

    id = db.Column(db.Integer, db.Sequence('brands_id_seq'), primary_key=True)
    name = db.Column(db.Unicode(300), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    fb_id = db.Column(db.Unicode(255), nullable=True, unique=True)
    profile_url = db.Column(db.Unicode(500), nullable=True)
    cover_url = db.Column(db.Unicode(500), nullable=True)
    managed = db.Column(db.BOOLEAN(True), default=False)
    posts = db.relationship(
        'Posts', backref='brand', lazy='dynamic'
    )

    def __init__(self, name, fb_id=None, profile_url=None, cover_url=None):
        self.name = name
        self.fb_id = fb_id
        self.profile_url = profile_url
        self.cover_url = cover_url
        self.created = datetime.datetime.now()

    def has_rights(self):
        if current_user.admin:
            return True
        return current_user.user in self.managers.all()


class Posts(db.Model):
    __tablename__ = 'posts'
    __bind_key__ = 'db1'
    api_version = (1,)
    preprocessors = {'GET_MANY': [auth_func], 'GET_SINGLE': [auth_func],
                     'PUT_SINGLE': [auth_func], 'PUT_MANY': [auth_func],
                     'POST': [auth_func], "DELETE": [auth_func]}
    exclude_columns = (
        'comments', 'post_link_followed.password', 'post_link_followed.auth_key',
    )

    id = db.Column(db.Integer, db.Sequence('posts_id_seq'), primary_key=True)
    fb_id = db.Column(db.String(100), nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    title = db.Column(db.Unicode(500), nullable=True)
    text = db.Column(db.Unicode, nullable=True)
    url = db.Column(db.Unicode(600))
    image_url = db.Column(db.Unicode(350))
    created = db.Column(db.TIMESTAMP, nullable=False)
    publish_at = db.Column(db.TIMESTAMP, nullable=True)
    comments = db.relationship(
        'Comments', backref='post', lazy='dynamic'
    )

    post_link_followed = db.relationship(
        'Users', secondary=posts_links_followed,
        backref=db.backref('posts_links_followed', lazy='dynamic'), lazy='dynamic'
    )

    def __init__(self, brand_id, title, text, url=None, image_url=None, publish_at=None,
                 created=None, fb_id=None):
        self.publish_at = publish_at
        self.brand_id = brand_id
        self.title = title
        self.text = text
        self.url = url
        self.image_url = image_url
        self.fb_id = fb_id
        if not created:
            self.created = datetime.datetime.now()
        else:
            self.created = created


class Comments(db.Model):
    __tablename__ = 'posts_comments'
    __bind_key__ = 'db1'
    api_version = (1,)
    preprocessors = {'GET_MANY': [auth_func], 'GET_SINGLE': [auth_func],
                     'PUT_SINGLE': [auth_func], 'PUT_MANY': [auth_func],
                     'POST': [auth_func], "DELETE": [auth_func]}
    exclude_columns = (
    )

    id = db.Column(db.Integer, db.Sequence('posts_comments_id_seq'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Unicode, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, post_id, user_id, text):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.created = datetime.datetime.now()


