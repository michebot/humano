from server import app, example_data
from unittest import TestCase
from model import connect_to_db, db
from flask import session
# import doctest


# def load_tests(loader, tests, ignore):
#     """Run doctests and file-based doctests."""

#     tests.addTests(doctest.DocTestSuite(server))
#     return tests


class RouteTests(TestCase):
    """Route testing when a user is logged out."""

    def setUp(self):
        """Runs before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"

        # Connect to test DB
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1


    def test_signup_form(self):
        """The sign up form renders"""
        result = self.client.get("/sign-up")
        self.assertIn(b"First Name", result.data)


    def test_create_account_success(self):
        result = self.client.post("/sign-up",
                                 data={"username": "marylamb", 
                                       "first_name": "mary", 
                                       "last_name": "lamb", 
                                       "email": "mary@lamb.com", 
                                       "password": "password",
                                       "phone_number": "12345678901"},
                                 follow_redirects = True)
        self.assertIn(b"Log Out", result.data)


    def test_create_account_fail(self):
        result = self.client.post("/sign-up",
                                 data={"username": "marylamb", 
                                       "first_name": "mary", 
                                       "last_name": "lamb", 
                                       "email": "mary@lamb.com", 
                                       "password": "password",
                                       "phone_number": "12345678901"},
                                 follow_redirects = True)
        self.assertIn(b"Looks like this username is taken", result.data)


    def test_login_form(self):
        """The log in form renders"""
        result = self.client.get("/login")
        self.assertIn(b"Log In", result.data)
        pass


    def test_login_nonexisting_username(self):
        result = self.client.post("/login",
                                 data={"username": "gob",  
                                       "password": "password"},
                                 follow_redirects = True)
        self.assertIn(b"Log In", result.data)


    def test_login_incorrect_password(self):
        result = self.client.post("/login",
                                 data={"username": "marylamb",  
                                       "password": "pass"},
                                 follow_redirects = True)
        self.assertIn(b"Username", result.data)


    def test_login_success(self):
        result = self.client.post("/login",
                                 data={"username": "marylamb",  
                                       "password": "password"},
                                 follow_redirects = True)
        self.assertIn(b"Welcome, Mary", result.data)


    def test_render_user_home(self):
        result = self.client.get("/user-home")
        self.assertIn(b"Add Contact", result.data)


    def test_logout(self):
        result = self.client.get("/logout", follow_redirects = True)
        self.assertIn(b"You have been logged out", result.data)


    def tearDown(self):
        """Runs after every test."""

        db.session.close()
        db.drop_all()


if __name__ == '__main__':
    import unittest
    unittest.main()