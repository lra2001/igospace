from flask import Flask, render_template, send_from_directory
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db

# create the app
app = Flask(__name__)
# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# initialize the app with the extension
db.init_app(app)

# create routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def home():
    return render_template('home.html', active_page='home')

@app.route('/register')
def register():
    return render_template('register.html', active_page='register')

@app.route('/login')
def login():
    return render_template('login.html', active_page='login')

# Create tables for models
@app.before_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)