"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User
from utils import get_form_data, create_or_update


def create_app(uri='postgresql:///blogly', echo=True):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SECRET_KEY'] = "omg_it is a secret don't you know?"

    connect_db(app)
    db.create_all()

    @app.route('/')
    def home():
        return redirect('/users')

    @app.route('/users')
    def all_users():
        users = User.get_all_users()
        return render_template('users.html', users=users)

    @app.route('/users/new')
    def new_user():
        return render_template('new_user.html')

    @app.route('/users/new', methods=['POST'])
    def create_new_user():
        data = get_form_data()
        create_or_update(data)

        flash(f'Added new user {data.first_name} {data.last_name}')
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
        data = get_form_data()
        create_or_update(data, user)
        return redirect('/')

    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    def delete_user(user_id):
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

        return redirect('/')

    return app


flask_app = create_app()
