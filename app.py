from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, User, Product, CartItem, Order, OrderItem
from datetime import timedelta

# create the app
app = Flask(__name__)

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = 'supersecretkey'

# initialize the app with the extension

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# create routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def home():
    return render_template('home.html', active_page='home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        address = request.form.get("address")
        phone = request.form.get("phone")
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "warning")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please use another.", "warning")
            return redirect(url_for("register"))

        new_user = User(
            username=username,
            email=email,
            fname=fname,
            lname=lname,
            address=address,
            phone=phone,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get('next')

    if request.method == "POST":
        identifier = request.form["username"]
        password = request.form["password"]
        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            session_cart = session.get('cart', {})
            for product_id, quantity in session_cart.items():
                cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
                if cart_item:
                    cart_item.quantity += quantity
                else:
                    new_item = CartItem(user_id=user.id, product_id=product_id, quantity=quantity)
                    db.session.add(new_item)
            db.session.commit()
            session.pop('cart', None)

            flash("Logged in successfully.", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route('/shop')
def shop():
    products = Product.query.order_by(Product.id.asc()).all()
    return render_template('shop.html', products=products, active_page='shop')

@app.route('/cart')
def cart():
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return render_template('cart.html', cart_items=cart_items)
    else:
        session_cart = session.get('cart', {})
        products = Product.query.filter(Product.id.in_(session_cart.keys())).all()
        cart_items = []
        total = 0

        for product in products:
            qty = session_cart[str(product.id)]
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })

        return render_template('cart.html', cart_items=cart_items, total=total)

# Add to cart functionality using session
def add_to_session_cart(product_id, quantity):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    session['cart'] = cart

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if current_user.is_authenticated:
        # Update DB cart for logged-in users
        for key in request.form:
            if key.startswith('quantities[') and key.endswith(']'):
                item_id = key[11:-1]
                quantity = request.form.get(key, type=int)
                cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
                if cart_item:
                    if quantity and quantity > 0:
                        cart_item.quantity = quantity
                    else:
                        db.session.delete(cart_item)
        # Remove items explicitly checked for removal
        remove_ids = request.form.getlist('remove')
        for item_id in remove_ids:
            cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
            if cart_item:
                db.session.delete(cart_item)
        db.session.commit()
    else:
        # Update session cart for guests
        cart = session.get('cart', {})
        # Update quantities
        for key in request.form:
            if key.startswith('quantities[') and key.endswith(']'):
                item_id = key[11:-1]
                quantity = request.form.get(key, type=int)
                if quantity and quantity > 0:
                    cart[item_id] = quantity
                else:
                    cart.pop(item_id, None)
        # Remove items explicitly checked for removal
        remove_ids = request.form.getlist('remove')
        for item_id in remove_ids:
            cart.pop(item_id, None)
        session['cart'] = cart

    flash("Cart updated successfully!", "success")
    return redirect(url_for('cart'))

@app.context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        count = CartItem.query.filter_by(user_id=current_user.id).count()
    else:
        cart = session.get('cart', {})
        count = sum(cart.values())
    return dict(cart_count=count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart_item = None
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        db.session.commit()
    else:
        add_to_session_cart(product_id, quantity)
    return redirect(url_for('shop'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart'))

    if request.method == 'POST':
        total = sum(item.product.price * item.quantity for item in cart_items)

        new_order = Order(user_id=current_user.id, total_amount=total)
        db.session.add(new_order)
        db.session.flush()  # Get new_order.id without committing yet

        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            db.session.delete(item)  # Clear cart

        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for('order_confirmation', order_id=new_order.id))

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        flash("Access denied to this order.", "danger")
        return redirect(url_for('home'))

    return render_template('order-confirmation.html', order=order, timedelta=timedelta)

@app.route('/order-history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template('order-history.html', orders=orders)

if __name__ == "__main__":
    app.run(debug=True)