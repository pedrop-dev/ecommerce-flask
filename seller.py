from flask import request, flash, redirect, url_for, g, session, render_template, Blueprint, current_app
from .utils import BUYER, SELLER
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'svg'}

bp = Blueprint('seller', __name__)

def allowed_filename(filename:str):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG

def create_new_offer(img_path: str, price: str, title: str, file) -> None:
    from .db import get_db

    error = None

    db = get_db()
    user = db.execute(
            'SELECT * FROM user WHERE id = ?', 
            (str(g.user),)
            ).fetchone()

    username = user['username']
    current_app.logger.debug(f'user[\'username\'] = { username}')

    try:
        db.execute(
                "INSERT INTO offer (username, price, offername, image) VALUES (?, ?, ?, ?)", 
                (user['username'], price, title, img_path,)
                )
        db.commit()

    except Exception as e:
        error = 'Some error occurred, we are sorry!'
        log_error = e.__str__()
        current_app.logger.error(f"Error inserting values into database: {log_error}")

    else:
        file.save(os.path.join(current_app.config['UPLOAD_DIRECTORY'], file.filename))

    if error is None:
        pass

    else:
        flash(error)

            
@bp.route("/seller", methods=["GET", "POST"])
def seller():
    if request.method == 'POST':
        if 'bimage' not in request.files:
            flash('Couldn\'t find file part')
            return redirect(url_for(request.url))

        file = request.files['bimage']
        if file.filename == '' or file.filename is None:
            flash('Please select an image to sell your product')
            return redirect(url_for(request.url))

        if not allowed_filename(file.filename):
            flash('Filename is not allowed')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        create_new_offer(filename, request.form['bprice'], request.form['btitle'],file)
        return redirect(url_for('main.home'))
        


    else:
        if g.user is None:
            flash('You must be logged in as a seller to sell in this website')
            return redirect(url_for('auth.login'))


        error = None
        if session['user_type'] != SELLER:
            error = "User must be seller to sell in this website"
        
        if error is None:
            return render_template('seller.html')

        else:
            flash(error)
            return redirect(url_for('main.home'))

