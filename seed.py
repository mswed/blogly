from models import User, db
from app import app

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

db.session.add(bob)
db.session.add(mini)
db.session.add(jessica)
db.session.add(roger)
db.session.add(abdalla)

db.session.commit()
