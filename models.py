from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    cart_items = db.relationship('CartItem', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product id={self.id} name={self.name} price={self.price}>"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref='cart_items')

    def __repr__(self):
        return f"<CartItem id={self.id} user_id={self.user_id} product_id={self.product_id} quantity={self.quantity}>"