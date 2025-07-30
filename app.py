from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("home"))
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
    products = Product.query.all()
    return render_template('shop.html', products=products, active_page='shop')

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items, active_page='cart')

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    # Parse quantities from form inputs named like quantities[<item_id>]
    for key in request.form:
        if key.startswith('quantities[') and key.endswith(']'):
            item_id = key[11:-1]  # Extract item id inside the brackets
            quantity = request.form.get(key, type=int)
            cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
            if cart_item:
                if quantity and quantity > 0:
                    cart_item.quantity = quantity
                else:
                    # Remove item if quantity <= 0
                    db.session.delete(cart_item)

    # Remove items explicitly checked for removal
    remove_ids = request.form.getlist('remove')
    for item_id in remove_ids:
        cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
        if cart_item:
            db.session.delete(cart_item)

    db.session.commit()
    flash("Cart updated successfully!", "success")
    return redirect(url_for('cart'))

@app.context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        count = CartItem.query.filter_by(user_id=current_user.id).count()
    else:
        count = 0
    return dict(cart_count=count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('shop'))

# if __name__ == "__main__":
#     app.run(debug=True)