from models import User, Post, Tag, db
from app import create_app

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

# Add users

bob = User(first_name='Bob', last_name='Bobertson')
mini = User(first_name='Mini', last_name='Mouse')
jessica = User(first_name='Jessica', last_name='Rabbit', image_url='https://wallpaperset.com/w/full/8/9/d/315524.jpg')
roger = User(first_name='Roger', last_name='Rabbit',
             image_url='https://upload.wikimedia.org/wikipedia/en/3/38/Roger-Rabbit.png')
abdalla = User(first_name='Abdalla', last_name='Rantisi')

db.session.add_all([bob, mini, jessica, roger, abdalla])
db.session.commit()

# Add posts
jessica1 = Post(title='This is my first post!', content="I'm not bad, I'm just drawn that way", user_id=3)
jessica2 = Post(title='Looking for my husband', content="He's a rabbit you know?", user_id=3)
jessica3 = Post(title='Selling a dress', content="It's red and stuff", user_id=3)


db.session.add_all([jessica1, jessica2, jessica3])
db.session.commit()

# Add tags
t1 = Tag(name='cartoon')
t2 = Tag(name='fun')
t3 = Tag(name='adventure')

db.session.add_all([t1, t2, t3])
db.session.commit()