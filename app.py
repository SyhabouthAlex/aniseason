import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError
from forms import RegisterForm, LoginForm, AnimeEditForm
from models import db, connect_db, User, Anime, Follow

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///aniseason'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "very secret key")

engine = create_engine("postgresql:///aniseason")
metadata = MetaData()
metadata.bind = engine

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def homepage():
    """Show all animes in database."""
    try:
        animes = Anime.query.order_by(Anime.member_count.desc(), Anime.year.desc()).all()
        return render_template('home.html', animes=animes, len=len(animes))
    except:
        flash("There was a problem rendering the database.", 'danger')
        return render_template('base.html')

@app.route('/refreshanimes', methods=["POST"])
def refresh():
    """Refreshes all the animes of the season using an array of animes."""

    animes = request.json["anime"]
    excluded_types = ["OVA", "ONA", "Movie"]

    db.session.commit()
    Follow.__table__.drop(engine)
    Anime.__table__.drop(engine)
    Anime.__table__.create(engine)
    Follow.__table__.create(engine)

    for anime in animes:
        if anime["members"] > 10000 and anime["type"] not in excluded_types and anime["airing_start"].startswith(str(request.json["season_year"])):
            a = Anime(title=anime["title"], season=request.json["season_name"], year=request.json["season_year"], airing_datetime=anime["airing_start"], image=anime["image_url"],
            description=anime["synopsis"], member_count=anime["members"])
            db.session.add(a)
    
    db.session.commit()
    return redirect('/')

@app.route('/login')
def login_and_register():
    """Show login and register forms."""

    register_form = RegisterForm()
    login_form = LoginForm()

    return render_template('login.html', register_form=register_form, login_form=login_form)

@app.route('/register', methods=["POST"])
def register():
    """Handle user registration"""

    register_form = RegisterForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
        try:
            user = User.register(
                username=register_form.username.data,
                password=register_form.password.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('login.html', register_form=register_form, login_form=login_form)

        do_login(user)
        return redirect("/")

@app.route('/login', methods=["POST"])
def login():
    """Handle user login"""
    register_form = RegisterForm()
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.authenticate(login_form.username.data,
                                 login_form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

@app.route('/logout')
def logout():
    """Handle user logout."""

    do_logout()
    flash("Successfully logged out.", 'success')
    return redirect("/")

@app.route('/edit/<int:anime_id>', methods=["GET", "POST"])
def edit_anime(anime_id):
    """Edit anime information."""

    if not g.user or not g.user.is_admin:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    anime = Anime.query.get_or_404(anime_id)
    form = AnimeEditForm(obj=anime)

    if form.validate_on_submit():
        anime.title = form.title.data
        anime.season = form.season.data
        anime.year = form.year.data
        anime.airing_datetime = form.airing_datetime.data
        anime.image = form.image.data
        anime.description = form.description.data
        anime.watch_link = form.watch_link.data

        db.session.commit()
        return redirect("/")

    return render_template('anime-edit.html', form=form)
