from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, User, Product, CartItem

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
            flash("Logged in successfully.", "success")
            return redirect(url_for(next_page)) if next_page else redirect(url_for("home"))
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

@app.route('/checkout')
def checkout():
    if not current_user.is_authenticated:
        flash("Please log in or register to continue to checkout.", "warning")
        return redirect(url_for('login', next='checkout'))

    # address confirmation, payment, etc
    return render_template('checkout.html')

if __name__ == "__main__":
    app.run(debug=True)