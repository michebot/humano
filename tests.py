from server import app
from unittest import TestCase
from model import connect_to_db, example_data
# import doctest


# def load_tests(loader, tests, ignore):
#     """Run doctests and file-based doctests."""

#     tests.addTests(doctest.DocTestSuite(server))
#     return tests


class RouteTestsLoggedOut(TestCase):
    """Route testing when a user is logged out."""

    def setUp(self):
        """Runs before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = ≈

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
        pass


    def test_create_account_success(self):
        result = self.client.post("/sign-up",
                                 data={username=username, 
                                       first_name=first_name, 
                                       last_name=last_name, 
                                       email=email, 
                                       password=password,
                                       phone_number=phone_number},
                                 follow_redirects = True)
        self.assertIn(b"Welcome! Thanks", result.data)
        pass


    def test_create_account_fail(self):
        pass


    def test_login_form(self):
        """The log in form renders"""
        result = self.client.get("/login")
        self.assertIn()
        pass


    def test_login_nonexisting_username(self):
        pass


    def test_login_incorrect_password(self):
        pass


    def test_login_success(self):
        pass


    def test_render_user_home(self):
        pass


    def test_logout(self):
        pass


    def tearDown(self):
        """Runs after every test."""

        db.session.close()
        db.drop_all()
    

# class TestSignUpProcess(TestCase):
#     pass


class RouteTestsLoggedIn(TestCase):
    """"Route tests with user logged in to session."""

    pass