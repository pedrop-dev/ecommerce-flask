from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



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
                "INSERT INTO user (username, email, password, userType, shopping_list) VALUES (?, ?, ?, ?, ?)",
                (username, email, generate_password_hash(password), userType, '[]')
                )
            db.commit()
        except db.IntegrityError:
            error = f"{username} or {email} is already registered"

        except Exception as e:
            error = e.__str__()


        else:
            return 0

    flash(error)
    return 1

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None:
        flash('User already logged in')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        if login_user(request.form['bemail'], request.form['bpassword']):
            return redirect(url_for("auth.login"))

        return redirect(url_for("main.home"))

    else:
        return render_template("login.html")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if g.user is not None:
        flash('User already logged in')
        return redirect(url_for('main.home'))

    if request.method == "POST":
        if register_user(request.form['busername'], request.form['bemail'], request.form['bpassword'], int(request.form['busertype'])) == 0: # No errors
            return redirect(url_for("auth.login"))

        return redirect(request.url) # if there is error stay in same url

    else:
        return render_template("register.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
