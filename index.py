
from flask import request, flash, redirect, url_for, g, session, render_template, Blueprint, current_app, send_from_directory, current_app
import json
import stripe

bp = Blueprint('main', __name__)

@bp.route('/img/<name>')
def img(name:str):
    return send_from_directory(current_app.config['UPLOAD_DIRECTORY'], name)

@bp.route("/", defaults={'search': None})
@bp.route("/<search>")
def home(search: str):
    from .db import get_db
    db = get_db()
    # flash('Testing error messages')

    if search is not None and search != '':
        offers = db.execute(
                "SELECT * FROM offer \
                WHERE offername LIKE ?", (f"%{search}%",)
                ).fetchall()

    else:
        offers = db.execute(
                "SELECT * FROM offer"
                ).fetchall()



    return render_template("index.html", offers=offers)


@bp.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if g.user is None:
        flash("You must be logged in to checkout")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        from .db import get_db

        db = get_db()

        stripe_cart = list()

        for cart_item in g.cart:
            # cart_item = db.execute(
            #         "SELECT * FROM offer WHERE id = ?", (str(cart_item_id),)
            #         ).fetchone()

            # app.logger.debug(f'cart_item_id = {cart_item_id}')

            stripe_cart.append({
                'price_data' : {
                    'product_data': {
                        'name': cart_item['offername']
                        },
                    'unit_amount': int(cart_item['price']*100),
                    'currency': 'usd',
                    },
                'quantity': 1,
                })

        try:
            db.execute(
                    "UPDATE user SET shopping_list = json(?) WHERE id = ?", (str([]), g.user)
                    )
            db.commit()

        except Exception as e:
            flash('Some error occurred, we are sorry!')
            current_app.logger.debug(e.__str__())
            return url_for('main.home')

        else:
            pass
            
        checkout_session = stripe.checkout.Session.create(
                line_items=stripe_cart,
                payment_method_types=['card'],
                mode='payment',
                success_url=request.host_url + 'checkout/success',
                cancel_url=request.host_url + 'checkout/cancel'
                )

        return redirect(checkout_session.url)


    from .db import get_db

    products_json = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (g.user,)
            ).fetchone()['shopping_list']

    products_id = json.loads(products_json)
    products = list()

    for id in products_id:
        product = get_db().execute(
                "SELECT * FROM offer WHERE id = ?", (id,)
                ).fetchone()
        products.append(product)

    return render_template('checkout.html', products=products)

@bp.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):

    from .db import get_db

    if request.method == 'POST':
        user = get_db().execute(
                "SELECT * FROM user WHERE id = ?", (g.user,)
                ).fetchone()

        current_products = json.loads(user['shopping_list'])
        current_app.logger.debug(f"\ncurrent_products = {current_products}")

        current_products.append(id)
        current_app.logger.debug(f"changed currend_products = {current_products}\n")
        db = get_db()
        db.execute("UPDATE user\nSET shopping_list = json(?)\nWHERE id = ?",
                         (str(current_products),g.user,))
        db.commit()

        


    offer = get_db().execute(
            "SELECT * FROM offer WHERE id = ?", (id,)
            ).fetchone()

    return render_template('product.html', product=offer)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/search', methods=['POST'])
def search():
    return redirect(url_for('main.home', search=request.form['bsearch']))

@bp.route('/checkout/success')
def checkout_success():
    return render_template('success.html')

@bp.route('/checkout/cancel')
def checkout_cancel():
    return render_template('cancel.html')
