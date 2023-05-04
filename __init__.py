
import os

import json
from flask import Flask, session, g
import stripe

UPLOAD_DIRECTORY = 'imgs'

stripe.api_key = os.environ['STRIPE_SECRET_KEY']


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev', #change later
            DATABASE=os.path.join(app.instance_path, 'ecommerce.sqlite')
            )

    app.config['UPLOAD_DIRECTORY'] = os.path.join(app.instance_path, UPLOAD_DIRECTORY)

    app.secret_key = b'd93284ufdsaf'
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_DIRECTORY'])
        
    except OSError:
        pass

    @app.before_request
    def load_logged_user():
        from .db import get_db
        user_id = session.get('user_id')
        app.logger.debug(f"user_id = {user_id}")
        

        if user_id is None:
            g.user = None

        else:

            user = get_db().execute(
                    "SELECT * FROM user WHERE id = ?", (user_id,)
                    ).fetchone()

            g.user = user['id']
            g.username = user['username']



        app.logger.debug(f"Loading { g.user } as user")

    @app.before_request
    def load_cart():
        from .db import get_db
        
        cart_id = list()

        db = get_db()
        if g.user is not None:
            cart_id = json.loads(db.execute(
                "SELECT * FROM user WHERE id = ?", (g.user,)
                ).fetchone()['shopping_list'])

        g.cart = list()

        for item_id in cart_id:
            item = db.execute(
                    "SELECT * FROM offer WHERE id = ?", (item_id,)
                    ).fetchone()
            g.cart.append(item)


    from . import auth
    from . import seller
    from . import index

    app.register_blueprint(auth.bp)
    app.register_blueprint(seller.bp)
    app.register_blueprint(index.bp)

    from . import db

    db.init_app(app)

    return app

