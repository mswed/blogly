"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(),
                          nullable=False,
                          default='https://cdn0.iconfinder.com/data/icons/ui-3-1/512/user-1024.png')

    @classmethod
    def get_all_users(cls):
        return cls.query.order_by(User.first_name, User.last_name).all()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
