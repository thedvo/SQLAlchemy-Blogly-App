from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


db.drop_all()
db.create_all()


class UserTest(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample User."""

        User.query.delete()

        user = User(first_name="Nikola", last_name="Jokic", image_url='https://www.gannett-cdn.com/presto/2021/06/08/USAT/f5999f17-9937-4f91-87a6-6067e2c0589e-2021-06-08_Nikola_Jokic1.jpg?crop=3090,2097,x74,y50')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Nikola', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Nikola Jokic</h1>', html)
            

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "Giannis", "last_name": "Antetokounmpo", "image_url": "https://phantom-marca.unidadeditorial.es/11d941d78a4b21d34da29b800eb0d576/resize/1320/f/jpg/assets/multimedia/imagenes/2021/12/05/16386648037085.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Giannis Antetokounmpo</h1>", html)


    def test_edit_route(self):
        with app.test_client() as client:
            d = {"first_name": "Giannisss", "last_name": "Antetokounmpoo", "image_url": "https://phantom-marca.unidadeditorial.es/11d941d78a4b21d34da29b800eb0d576/resize/1320/f/jpg/assets/multimedia/imagenes/2021/12/05/16386648037085.jpg"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
