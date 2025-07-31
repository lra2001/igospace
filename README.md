# iGo Space Travel

## Description

iGo Space Travel is a shop aimed for space adventurers who would like to explore space and get the latest space gear. iGo Space Travel brings excitement, fun and adventure on a different number of activities designed for families, team building, solo explorers or simply commute. We can't wait to have you on board.

## Website contents
This website includes the following pages:
- Base
- Home
- Login
- Register
- Shop
- Cart
- Checkout

And uses the languages/modules below:
- Python
- HTML
- CSS
- JavaScript
- PostgreSQL
- Flask
- SQLAlchemy

### Create Project
- Set up the Flask Environment:
  - Initialize a virtual environment by running the command: python -m venv venv
  - Activate the virtual environment on Windows: venv\Scripts\activate
  - Install Flask by running the command: pip install flask.
- Create Flask Application Files:
  - Create a new Python file named app.py
- Update Python
  - python.exe -m pip install --upgrade pip
- Install SQLAlchemy
  - pip install SQLAlchemy
  - pip install flask_sqlalchemy, sqlalchemy.orm

### Deploy in render
- Create an account in [render](https://render.com/) and connect to your GitHub account
- Create a New Workspace
- Create new service and select Postgres to create the database
- Create new service, select Web Services and your GitHub repository
  - Make sure your Build Command is pip install -r requirements.txt
  - Make sure your start command is gunicorn app:app
- Click the 3 dots next to your Web Service and Settings
- Click Environment under Manage
- Create a new Environment Variable with the key DATABASE_URL. You can get the values needed on the Postgres service


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