# iGo Space Travel

## Description

iGo Space Travel is a shop aimed for space adventurers who would like to explore space and get the latest space gear. iGo Space Travel brings excitement, fun and adventure on a different number of activities designed for families, team building, solo explorers or simply commute. We can't wait to have you on board.

This website is available in [Render](https://igospace.onrender.com)

## Website contents
This website includes the following pages:
- Base
- Home
- Login
- Register
- Shop
- Cart
- Checkout
- Order History
- Order Confirmation

## Technologies Used

### Languages and Frameworks
- Python
- HTML
- CSS
- JavaScript

### Backend
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Bcrypt

### Frontend
- Jinja2 (Flask templating)
- Font Awesome (icons)
- Bootstrap (for layout and responsiveness)

### Tools
- Visual Studio Code
- GitHub Desktop
- pgAdmin
- PostgreSQL

### Create Project
- Set up the Flask Environment:
  - Initialize a virtual environment by running the command: python -m venv venv
  - Activate the virtual environment on Windows: venv\Scripts\activate
  - Install Flask by running the command: pip install flask.
- Create Flask Application Files:
  - Create a new Python file named app.py
- Update Python
  - python.exe -m pip install --upgrade pip
- Install Dependencies
  - pip install Flask Flask-SQLAlchemy psycopg2-binary Flask-Bcrypt python-dotenv
- Run Application
  - python app.py

### Deploy on render
- Create an account in [render](https://render.com/) and connect to your GitHub account
- Create a New Workspace
- Create new service and select Postgres to create the database
- Create new service, select Web Services and your GitHub repository
  - Make sure your Build Command is pip install -r requirements.txt
  - Make sure your start command is gunicorn app:app
- Click the 3 dots next to your Web Service and Settings
- Click Environment under Manage
- Create a new Environment Variable with the key DATABASE_URL. You can get the values needed on the Postgres service

### Templating: Jinja2
Jinja2 is Flask’s templating engine used to embed logic in HTML.
| Feature                  | Usage                                               |
| ------------------------ | --------------------------------------------------- |
| `{{ variable }}`         | Output variables like `{{ current_user.username }}` |
| `{% if / for %}`         | Control flow like `{% for item in cart_items %}`    |
| `{% extends / block %}`  | Template inheritance                                |
| `url_for()`              | Generates dynamic URLs                              |
| `get_flashed_messages()` | Displays flash messages                             |

[Jinja2 Docs](https://jinja.palletsprojects.com/en/3.1.x/templates/)

### Javascript
JavaScript handles interactivity and DOM updates.
Example uses:
- Updating the cart UI dynamically
- Form validation
- Interactive buttons
[JavaScript Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### Bootstrap
Bootstrap helps build responsive layouts with utility classes and components.
Example:
```html
<button class="btn btn-primary">Checkout</button>
<div class="row">
  <div class="col-md-6">Product Info</div>
</div>
```
To include in project:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
``

### Software
- Visual Studio Code
- GitHub Desktop
- pgAdmin
- PostgreSQL

### References
- [Download Visual Studio Code](https://code.visualstudio.com/download)
- [Download GitHub Desktop](https://desktop.github.com/download/)
- [Download pgAdmin](https://www.pgadmin.org/download/)
- [Download PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [Download Python](https://www.python.org/downloads/)
- [Flask Installation](https://flask.palletsprojects.com/en/stable/installation/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Templates](https://flask.palletsprojects.com/en/stable/tutorial/templates/)
- [SQL Alchemy - Installation Guide](https://docs.sqlalchemy.org/en/20/intro.html#installation)
- [python-dotenv 1.1.1](https://pypi.org/project/python-dotenv/)

### Images
- [Convert image type to WebP](https://www.freeconvert.com/webp-converter)
- [Image Resizer](https://imageresizer.com/)
- [Create Logo](https://www.canva.com/)
- [Convert to favicon](https://favicon.io/favicon-converter/)
- [AI Image Generator](https://deepai.org/)

### Errors
- [Import "flask_sqlalchemy" could not be resolved](https://stackoverflow.com/questions/64981804/importerror-flask-sqlalchemy-could-not-be-resolved)
- [ModuleNotFoundError: No module named 'psycopg2'](https://blog.finxter.com/fixed-modulenotfounderror-no-module-named-psycopg2/)