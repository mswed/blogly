from app import create_app
from models import db, User
from unittest import TestCase


class TestRoutes(TestCase):
    def setUp(self):
        # Create the app
        self.app = create_app(uri='postgresql:///blogly_test', echo=False)
        db.drop_all()
        db.create_all()

        # Seed
        bob = User(first_name='Bob', last_name='Bobertson')
        mini = User(first_name='Mini', last_name='Mouse')
        jessica = User(first_name='Jessica', last_name='Rabbit',
                       image_url='https://wallpaperset.com/w/full/8/9/d/315524.jpg')
        roger = User(first_name='Roger', last_name='Rabbit',
                     image_url='https://upload.wikimedia.org/wikipedia/en/3/38/Roger-Rabbit.png')
        abdalla = User(first_name='Abdalla', last_name='Rantisi')

        db.session.add(bob)
        db.session.add(mini)
        db.session.add(jessica)
        db.session.add(roger)
        db.session.add(abdalla)

        db.session.commit()

    def tearDown(self):

        db.session.rollback()

    def test_user_list(self):
        with self.app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob Bobertson', html)
            self.assertIn('<a href="/users/3">Jessica Rabbit</a>', html)

    def test_root(self):
        with self.app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob Bobertson', html)
            self.assertIn('<a href="/users/3">Jessica Rabbit</a>', html)

    def test_delete(self):
        with self.app.test_client() as client:
            resp = client.post('/users/2/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Mini Mouse', html)
            self.assertIn('<a href="/users/3">Jessica Rabbit</a>', html)

    def test_edit(self):
        with self.app.test_client() as client:
            resp = client.post('/users/4/edit',
                               data = {'first_name': 'James',
                                       'last_name': 'Bond',
                                       'profile_image': 'https://i2-prod.manchestereveningnews.co.uk/incoming/article7746339.ece/ALTERNATES/s1227b/CS30386896.jpg'},
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/4">James Bond</a>', html)
