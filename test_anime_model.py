"""Anime model tests."""

# run these tests like:
#
#    python -m unittest test_anime_model.py


import os
from unittest import TestCase

from models import db, User, Anime, Follow

os.environ['DATABASE_URL'] = "postgresql:///aniseason-test"

from app import app

db.create_all()

class AnimeModelTestCase(TestCase):
    """Test anime model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.user_id = 123
        user = User.register("a","test12")
        user.id = self.user_id
        db.session.commit()

        self.user = User.query.get(self.user_id)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_anime_model(self):
        """Testing anime model"""
        
        anime = Anime(title="abc", season="sum", year=2018, member_count=1234)

        db.session.add(anime)
        db.session.commit()

        animes = Anime.query.all()

        self.assertEqual(len(animes), 1)
        self.assertEqual(animes[0].title, "abc")

    def test_anime_follow(self):
        """Testing following an anime"""
        anime = Anime(title="abc", season="sum", year=2018, member_count=1234)

        db.session.add(anime)
        db.session.commit()

        self.user.followed_animes.append(anime)
        db.session.commit()
        
        followed = User.query.get(self.user_id).followed_animes

        self.assertEqual(len(followed), 1)
        self.assertEqual(followed[0].season, anime.season)