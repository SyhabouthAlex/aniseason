"""Reset AniSeason database."""
from app import db
from models import User, Anime


db.drop_all()
db.create_all()

db.session.commit()
