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

    def __repr__(self):
        return f'<User {self.full_name} ({self.id})>'

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
    tags = db.relationship('Tag', secondary='posts_tags', cascade='all', backref='posts')

    def __repr__(self):
        return f'<Post {self.title} ({self.id})>'

    @property
    def nice_timestamp(self):
        return self.created_at.strftime('%b %d, %Y - %H:%M %p')


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    posts_tags = db.relationship('PostTag', cascade='all')

    @classmethod
    def get_all_tags(cls):
        return cls.query.order_by(Tag.name).all()

    def __repr__(self):
        return f'<Tag {self.name} ({self.id})>'


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

