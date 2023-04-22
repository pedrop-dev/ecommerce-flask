
import os
import functools

from sqlite3 import IntegrityError
from flask import Flask, render_template, request, url_for, redirect, session, flash, get_flashed_messages, g
from werkzeug.security import check_password_hash, generate_password_hash


BUYER = 1
SELLER = 2

def login_user(email: str, password: str) -> int:
    from .db import get_db

    error = None

    db = get_db()

    user = db.execute(
            'SELECT * FROM user WHERE email = ?',
            (email,)
            ).fetchone()

    if user is None:
        error = 'Incorrect Username'

    elif not check_password_hash(user['password'], password):
        error = 'Incorrect Password'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        session['user_type'] = user['userType']
        return 0

    else:
        flash(error)
        return 1

def register_user(username: str, email: str, password: str, userType: int) -> int:
    from .db import get_db
    error = None
    if not username:
        error = 'Username is required'

    elif not email:
        error = "Email is required"

    elif not password:
        error = 'Password is required'

    db = get_db()
    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, email, password, userType) VALUES (?, ?, ?, ?)",
                (username, email, generate_password_hash(password), userType)
                )
            db.commit()
        except db.IntegrityError:
            error = f"{username} or {email} is already registered"

        else:
            return 0

    flash(error)
    return 1

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev', #change later
            DATABASE=os.path.join(app.instance_path, 'ecommerce.sqlite')
            )

    app.secret_key = b'd93284ufdsaf'
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    @app.route("/seller")
    def seller():
        if g.user is None:
            return redirect(url_for('login'))


        error = None
        if session['user_type'] == SELLER:
            error = "User must be seller to sell in this website"
        
        if error is None:
            return render_template('seller.html')

        else:
            flash(error)
            return redirect(url_for('home'))

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            if login_user(request.form['bemail'], request.form['bpassword']):
                return redirect(url_for("login"))

            return redirect(url_for("home"))

        else:
            return render_template("login.html")


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == "POST":
            if register_user(request.form['busername'], request.form['bemail'], request.form['bpassword'], int(request.form['busertype'])) == 0:
                return redirect(url_for("login"))

            return redirect(request.url)

        else:
            return render_template("register.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    from . import db
    db.init_app(app)

    return app
