# -*- coding: utf-8 -*-
"""
.. module: views
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""
import json
import urllib

from flask import render_template, flash, redirect, session, Response
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.globals import request
from flask.helpers import url_for, stream_with_context
from werkzeug.exceptions import NotFound, Forbidden, InternalServerError

from wiin.frontend.auth import User
from wiin.frontend.forms import LoginForm, RegistrationForm, NewPostForm, NewBrandForm
from wiin.init import app, db
from wiin.models import Brands, Posts
from wiin.tools import _fb_login, app_access_token


@app.route('/')
def index():
    if current_user.is_authenticated() and current_user.admin:
        return redirect(url_for('brands_add'))
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
    if 'auth_url' in response:
        return redirect(response['auth_url'])
    elif 'access_token' in response:
        uid = response['uid']
        user = User.get(uid)
        if user:
            login_user(user)
            return redirect('/')
        else:
            raise Forbidden()
    else:
        raise InternalServerError()


@app.route('/logout')
@login_required
def logout():
    token = session.pop('_csrf_token', None)
    if not token or token != request.args.get('csrf_token'):
        raise Forbidden()

    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User.create(form)
        login_user(user)
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/brands')
@login_required
def brands_list():
    brands = Brands.query.order_by('-id')
    """:type: wiin.models.Brands"""

    if not current_user.admin:
        brands = brands.filter(Brands.managers.contains(current_user.user))

    return render_template('brands_list.html', brands=brands.all())


@app.route('/posts')
@app.route('/posts/<int:brand_id>')
@login_required
def posts_list(brand_id=None):
    items_per_page = 51
    page = int(request.args.get('page', 1)) - 1
    user = current_user.user
    posts = Posts.query

    if not user.admin:
        brands = Brands.query.filter(Brands.managers.contains(user)).all()
        """:type: list[wiin.models.Brands]"""
        posts = posts.join(Brands).filter(Brands.managers.contains(user))
    else:
        brands = Brands.query.all()
        """:type: list[wiin.models.Brands]"""

    brand = None

    if brand_id:
        brand = Brands.query.filter_by(id=brand_id).first()
        """:type: wiin.models.Brands"""

        if not brand:
            raise NotFound()

        if not brand.has_rights():
            raise Forbidden()

        posts = posts.filter(Posts.brand_id == brand_id).order_by('-Posts.id')

    posts = posts[page * items_per_page: (page + 1) * items_per_page]
    """:type: list[wiin.models.Posts]"""

    return render_template('posts_list.html', posts=posts, brand=brand, brands=brands)


@app.route('/posts/add/<int:brand_id>', methods=['GET', 'POST'])
@app.route('/posts/add/<int:brand_id>/<int:post_id>', methods=['GET', 'POST'])
@login_required
def posts_add(brand_id, post_id=None):
    post = None
    if post_id is None:
        form = NewPostForm(request.form)
    else:
        post = Posts.query.filter_by(id=post_id).first()

        if not post:
            raise NotFound()

        if not post.brand.has_rights():
            raise Forbidden()

        if not post.brand.managed:
            raise Forbidden("Brand is in manually managed mode!")

        form = NewPostForm(request.form, obj=post)

    brand = Brands.query.filter_by(id=brand_id).first()
    """:type: wiin.models.Brands"""

    if not brand:
        raise NotFound()

    if not brand.has_rights():
        raise Forbidden()

    if not brand.managed:
        raise Forbidden()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        url = form.url.data
        image_url = form.image_url.data
        publish_at = form.publish_date.data

        if post_id:
            if post_id != form.id.data:
                raise Forbidden()

            post.title = title
            post.text = text
            post.url = url
            post.image_url = image_url
            post.publish_at = publish_at
        else:
            post = Posts(
                brand_id=brand_id, title=title, text=text, url=url, image_url=image_url,
                publish_at=publish_at
            )
        db.session.add(post)
        db.session.commit()
        flash('Post {0}!'.format('updated' if post_id else 'created'))
        return redirect(url_for('posts_list', brand_id=brand_id))

    return render_template('posts_add.html', form=form, brand_id=brand_id)


@app.route('/posts_delete/<int:post_id>', methods=['POST'])
@login_required
def posts_delete(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    """:type: wiin.models.Posts"""

    if not post:
        raise NotFound()

    if not post.brand.has_rights():
        raise Forbidden()

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts_list'))


@app.route('/brands/load_fb_posts')
def load_fb_posts():
    """
    Load posts for all non-managed brands

    :return: Streaming Response
    :rtype: Response
    """

    def generate():
        brands = Brands.query.filter_by(managed=False).all()
        """:type: list[wiin.models.Brands]"""
        for brand in brands:
            # Fetch posts list
            data = json.load(
                urllib.urlopen(
                    'https://graph.facebook.com/%s/feed?access_token=%s' % (
                        brand.fb_id, app_access_token)
                )
            )
            while data['data']:  # While posts list is not empty
                for d in data['data']:
                    fb_id = d['id']
                    # Check if posts already exists
                    if Posts.query.filter_by(fb_id=fb_id).count() > 0:
                        continue

                    message = d.get('message', None)
                    image_url = d.get('picture', None)
                    url = d.get('link', None)
                    created = d['created_time']

                    # Skipt empty posts
                    if not any((message, image_url, url)):
                        continue

                    post = Posts(
                        brand.id,
                        message[0:50] if message else '',
                        message,
                        url,
                        image_url,
                        created=created,
                        fb_id=fb_id
                    )
                    db.session.add(post)
                    yield json.dumps(data['data'], indent=4)

                # List next pages
                if 'paging' in data and 'next' in data['paging']:
                    data = json.load(urllib.urlopen(data['paging']['next']))
                else:
                    data = None

            db.session.commit()

    return Response(stream_with_context(generate()), mimetype='application/json')


def _find_brand_by_name(name):
    data = json.load(
        urllib.urlopen(
            'https://graph.facebook.com/search?q=%s&type=group&access_token=%s'
            % (name, app_access_token)
        )
    )
    if 'data' in data and data['data']:
        brand_id = data['data'][0]['id']
    else:
        return None
    return brand_id


@app.route('/brands/add', methods=['GET', 'POST'])
@app.route('/brands/add/<int:brand_id>', methods=['GET', 'POST'])
@app.route('/brands/add/fb/<string:name>')
@login_required
def brands_add(name=None, brand_id=None):
    """
    Add new brand by FB group name or id

    :param name: name or id of FB group
    :type name: unicode
    :rtype: Response
    :raise NotFound: If group not found
    """
    if not current_user.admin:
        raise Forbidden()

    brand = None

    if name:
        return _brands_add_fb(name)
    else:
        if brand_id:
            brand = Brands.query.filter_by(id=brand_id).first()

            if not brand:
                raise NotFound()

            if not brand.has_rights():
                raise Forbidden()

            if not brand.managed:
                raise Forbidden('Brand is in manually managed mode!')

            form = NewBrandForm(request.form, obj=brand)
        else:
            form = NewBrandForm(request.form)

        if form.validate_on_submit():
            form_brand_id = form.id.data
            name = form.name.data
            hashtags = form.hashtags.data
            profile_img = form.profile_img_url.data
            cover_img = form.cover_img_url.data

            if brand_id:
                if form_brand_id != brand_id:
                    raise Forbidden()

                brand.name = name
                brand.profile_url = profile_img
                brand.cover_url = cover_img
            else:
                brand = Brands(name, profile_url=profile_img, cover_url=cover_img)

            db.session.add(brand)
            db.session.commit()

    return render_template('brands_add.html', form=form)


def _brands_add_fb(name):
    if name.isdigit():
        brand_id = name
    else:
        raise NotFound('No group id')

    data = json.load(
        urllib.urlopen(
            'https://graph.facebook.com/%s?access_token=%s' % (brand_id, app_access_token)
        )
    )

    if data:
        name = data['name']
        image_url = data['icon']
        fb_id = data['id']
        brand = Brands(name, fb_id=fb_id, profile_url=image_url)
        db.session.add(brand)
        db.session.commit()
    else:
        raise NotFound('Group no found')

    return Response(json.dumps(data, indent=4), mimetype='application/json')


@app.route('/brands/switch_managed/<int:brand_id>', methods=['POST'])
@login_required
def brands_switch_managed(brand_id):
    """
    Switch managed status for brand

    :param brand_id: id of brand
    :type brand_id: int
    :return: Operation status in JSON
    :rtype: Response
    :raise Forbidden: If user have no access for this brand
    :raise NotFound: If brand with this id doesn't exists
    """
    brand = Brands.query.filter_by(id=brand_id).first()
    """:type: wiin.models.Brands"""

    if not brand:
        raise NotFound()

    if not brand.has_rights():
        raise Forbidden()

    brand.managed = not brand.managed
    db.session.add(brand)
    db.session.commit()
    return Response(json.dumps({'status': True}), 200, mimetype='application/json')