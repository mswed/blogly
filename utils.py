from flask import request
from models import db, User
from collections import namedtuple


def get_user_form_data():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_image = request.form['profile_image']
    data = namedtuple('Data', ['first_name', 'last_name', 'profile_image'])

    return data(first_name, last_name, profile_image)


def create_or_update(data, user=None):
    if user is None:
        user = User(first_name=data.first_name, last_name=data.last_name, image_url=data.profile_image)
    else:
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.image_url = data.profile_image

    db.session.add(user)
    db.session.commit()

    return user
