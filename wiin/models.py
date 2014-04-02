# -*- coding: utf-8 -*-
"""
.. module: models
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import datetime

from wiin.init import db


brand_likes = db.Table(
    'brand_likes',
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

brand_follows = db.Table(
    'brand_follows',
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

posts_likes = db.Table(
    'posts_likes',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

posts_links_followed = db.Table(
    'posts_links_followed',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class Users(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'db1'
    api_version = (1,)

    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    name = db.Column(db.Unicode(300), nullable=False)
    email = db.Column(db.Unicode(254), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    auth_key = db.Column(db.Unicode(254))
    brands_likes = db.relationship(
        'Brands', secondary=brand_likes, backref=db.backref('users_likes', lazy='dynamic'),
        lazy='dynamic'
    )
    brands_follows = db.relationship(
        'Brands', secondary=brand_follows, backref=db.backref('users_follows', lazy='dynamic'),
        lazy='dynamic'
    )
    posts_likes = db.relationship(
        'Posts', secondary=posts_likes, backref=db.backref('users_likes', lazy='dynamic'),
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comments', backref='user', lazy='dynamic'
    )

    def __init__(self, name, email, auth_key):
        self.name = name
        self.email = email
        self.auth_key = auth_key
        self.created = datetime.datetime.now()


class Brands(db.Model):
    __tablename__ = 'brands'
    __bind_key__ = 'db1'
    api_version = (1,)

    id = db.Column(db.Integer, db.Sequence('brands_id_seq'), primary_key=True)
    name = db.Column(db.Unicode(300), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    posts = db.relationship(
        'Posts', backref='brand', lazy='dynamic'
    )

    def __init__(self, name):
        self.name = name
        self.created = datetime.datetime.now()


class Posts(db.Model):
    __tablename__ = 'posts'
    __bind_key__ = 'db1'
    api_version = (1,)

    id = db.Column(db.Integer, db.Sequence('posts_id_seq'), primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    title = db.Column(db.Unicode(500), nullable=False)
    text = db.Column(db.Unicode, nullable=False)
    url = db.Column(db.Unicode(600))
    image_url = db.Column(db.Unicode(350))
    created = db.Column(db.TIMESTAMP, nullable=False)
    comments = db.relationship(
        'Comments', backref='post', lazy='dynamic'
    )
    post_link_followed = db.relationship(
        'Users', secondary=posts_links_followed,
        backref=db.backref('posts_links_followed', lazy='dynamic'), lazy='dynamic'
    )

    def __init__(self, brand_id, title, text, url=None, image_url=None):
        self.brand_id = brand_id
        self.title = title
        self.text = text
        self.url = url
        self.image_url = image_url
        self.created = datetime.datetime.now()


class Comments(db.Model):
    __tablename__ = 'comments'
    __bind_key__ = 'db1'
    api_version = (1,)

    id = db.Column(db.Integer, db.Sequence('comments_id_seq'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Unicode, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, post_id, user_id, text):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.created = datetime.datetime.now()
