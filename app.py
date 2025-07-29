from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)