"""User View tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Anime, Follow

os.environ['DATABASE_URL'] = "postgresql:///aniseason-test"

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserModelTestCase(TestCase):
    """Test views for animes."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.user_id = 123
        user = User.register("a","test12")
        user.id = self.user_id

        self.anime_id = 123
        anime = Anime(title="abc", season="sum", year=2018, member_count=1234)
        db.session.add(anime)
        anime.id = self.anime_id

        db.session.commit()

        self.user = User.query.get(self.user_id)
        self.anime = Anime.query.get(self.anime_id)

        self.client = app.test_client()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_model(self):
        """Test user model"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD",
            is_admin=False
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.followed_animes), 0)

    def test_user_create_invalid(self):
        """Test creating an invalid user"""

        u = User.register("a", "password")
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_user_authenticate(self):
        """Test authenticating a user"""

        u = User.authenticate(self.user.username, "test12")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.user_id)
    
    def test_user_authenticate_username_invalid(self):
        """Test authenticating a user with an invalid username"""

        self.assertFalse(User.authenticate("dsaijgnaifd", "test12"))

    def test_user_authenticate_password_invalid(self):
        """Test authenticating a user with an invalid password"""

        self.assertFalse(User.authenticate(self.user.username, "asdfdasfwer"))