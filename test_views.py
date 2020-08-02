"""Anime View tests."""

# run these tests like:
#
#    python -m unittest test_anime_views.py


import os
from unittest import TestCase

from models import db, User, Anime, Follow

os.environ['DATABASE_URL'] = "postgresql:///aniseason-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ViewsTestCase(TestCase):
    """Test views for animes and users."""

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

    def test_anime_view(self):
        """Testing anime view on main page"""
        with self.client as c:
            resp = c.get("/")

        self.assertIn("abc", str(resp.data))

    def setup_anime_follow(self):
        """Setup testing following an anime"""
        self.user.followed_animes.append(self.anime)
        db.session.commit()

    def test_anime_follow(self):
        """Testing viewing followed animes"""
        self.setup_anime_follow()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get("/my-list")

        self.assertIn("abc", str(resp.data))
