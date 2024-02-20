"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
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
        return render_template('new_post.html', user=user)

    @app.route('/users/<int:user_id>/posts/new', methods=['POST'])
    def create_new_post(user_id):
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{user_id}')

    @app.route('/posts/<int:post_id>/edit')
    def edit_post(post_id):
        post = db.get_or_404(Post, post_id)
        return render_template('edit_post.html', post=post)

    @app.route('/posts/<int:post_id>/edit', methods=['POST'])
    def update_post(post_id):
        title = request.form['title']
        content = request.form['content']
        post = db.get_or_404(Post, post_id)
        if post is not None:
            post.title = title
            post.content = content
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
    return app


flask_app = create_app(echo=True)
