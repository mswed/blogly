"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag
from utils import get_user_form_data, create_or_update


def create_app(uri='postgresql:///blogly', echo=True):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SECRET_KEY'] = "omg_it is a secret don't you know?"

    connect_db(app)
    db.create_all()

    ###################################################################################################################
    # USER ROUTES
    ###################################################################################################################

    @app.route('/')
    def home():
        posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

        return render_template('home.html', posts=posts)

    @app.route('/users')
    def all_users():
        users = User.get_all_users()
        return render_template('users.html', users=users)

    @app.route('/users/new')
    def new_user():
        return render_template('new_user.html')

    @app.route('/users/new', methods=['POST'])
    def create_new_user():
        data = get_user_form_data()
        user = create_or_update(data)

        flash(f'Added new user {user.full_name}', 'text-success')

        return redirect('/')

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        user = db.get_or_404(User, user_id)

        return render_template('user_details.html', user=user, user_id=user_id)

    @app.route('/users/<int:user_id>/edit')
    def edit_user(user_id):
        user = db.get_or_404(User, user_id)
        return render_template('edit_user.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=['POST'])
    def update_user(user_id):
        user = db.get_or_404(User, user_id)
        data = get_user_form_data()
        create_or_update(data, user)
        return redirect('/')

    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    def delete_user(user_id):
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

        return redirect('/')

    ###################################################################################################################
    # POST ROUTES
    ###################################################################################################################
    @app.route('/posts/<int:post_id>')
    def show_post(post_id):
        post = db.get_or_404(Post, post_id)

        return render_template('post_details.html', post=post)

    @app.route('/users/<int:user_id>/posts/new')
    def new_post(user_id):
        user = User.query.get(user_id)
        tags = Tag.get_all_tags()
        return render_template('new_post.html', user=user, tags=tags)

    @app.route('/users/<int:user_id>/posts/new', methods=['POST'])
    def create_new_post(user_id):
        # import pdb
        # pdb.set_trace()
        title = request.form['title']
        content = request.form['content']
        tags = []
        for k, v in request.form.to_dict().items():
            if k not in ['title', 'content']:
                t = Tag.query.filter_by(name=k).first()
                tags.append(t)
        post = Post(title=title, content=content, user_id=user_id)
        for t in tags:
            post.tags.append(t)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{user_id}')

    @app.route('/posts/<int:post_id>/edit')
    def edit_post(post_id):
        post = db.get_or_404(Post, post_id)
        tags = Tag.get_all_tags()

        return render_template('edit_post.html', post=post, tags=tags)

    @app.route('/posts/<int:post_id>/edit', methods=['POST'])
    def update_post(post_id):
        title = request.form['title']
        content = request.form['content']
        tags = []
        for k, v in request.form.to_dict().items():
            if k not in ['title', 'content']:
                t = Tag.query.filter_by(name=k).first()
                tags.append(t)

        post = db.get_or_404(Post, post_id)
        if post is not None:
            post.title = title
            post.content = content
            post.tags = tags
            db.session.add(post)
            db.session.commit()
        return redirect(f'/posts/{post.id}')

    @app.route('/posts/<int:post_id>/delete', methods=['POST'])
    def delete_post(post_id):
        post = Post.query.filter_by(id=post_id)
        post_user = post.first().user.id
        post.delete()
        db.session.commit()

        return redirect(f'/users/{post_user}')

    ###################################################################################################################
    # TAG ROUTES
    ###################################################################################################################
    @app.route('/tags')
    def tag_list():
        tags = Tag.get_all_tags()
        return render_template('tags.html', tags=tags)

    @app.route('/tags/<int:tag_id>')
    def show_tag(tag_id):
        tag = db.get_or_404(Tag, tag_id)

        return render_template('tag_details.html', tag=tag)

    @app.route('/tags/new')
    def new_tag():
        return render_template('new_tag.html')

    @app.route('/tags/new', methods=['POST'])
    def create_new_tag():
        name = request.form['tag_name']
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

    @app.route('/tags/<int:tag_id>/edit')
    def edit_tag(tag_id):
        tag = db.get_or_404(Tag, tag_id)

        return render_template('edit_tag.html', tag=tag)

    @app.route('/tags/<int:tag_id>/edit', methods=['POST'])
    def update_tag(tag_id):
        name = request.form['tag_name']
        tag = db.get_or_404(Tag, tag_id)
        tag.name = name

        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

    @app.route('/tags/<int:tag_id>/delete', methods=['POST'])
    def delete_tag(tag_id):
        tag = Tag.query.filter_by(id=tag_id)
        tag.delete()
        db.session.commit()

        return redirect(f'/tags')
    ###################################################################################################################
    # GENERAL ROUTES
    ###################################################################################################################
    @app.errorhandler(404)
    def not_found(e):
        return render_template('not_found.html'), 404

    return app


flask_app = create_app(echo=False)
