"""SQLAlchemy models"""

from datetime import datetime, tzinfo
from pytz import timezone
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False
    )

    followed_animes = db.relationship(
        'Anime',
        secondary="follows",
        backref="followers",
        cascade="all, delete"
    )

    @classmethod
    def register(cls, username, password, is_admin=False):
        """Register user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            is_admin=is_admin
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Follow(db.Model):
    """Many to many model for users and followed animes"""

    __tablename__ = 'follows'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True
    )

    anime_id = db.Column(
        db.Integer,
        db.ForeignKey('animes.id', ondelete="CASCADE"),
        primary_key=True
    )
    
class Anime(db.Model):
    """Anime model"""

    __tablename__ = 'animes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    season = db.Column(
        db.Text,
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    airing_datetime = db.Column(
        db.DateTime
    )

    image = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text,
        default="This anime has no description."
    )

    member_count = db.Column(
        db.Integer,
        nullable=False
    )

    watch_link = db.Column(
        db.Text
    )

    def get_day(self):
        """Gets the number of days until the next episode."""
        if self.airing_datetime:
            day = self.airing_datetime.weekday()
            current_day = datetime.now(timezone('US/Pacific')).weekday()

            if day >= current_day:
                days = day - current_day
            else:
                days = day - current_day + 7

            if days == 0:
                return "Newest episode airs today!"
            else:
                return f"{days} days until new episode"
        else:
            return "No airdate information."

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
