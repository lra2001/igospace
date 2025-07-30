from dotenv import load_dotenv
import os

load_dotenv()

# DB credentials
# DB_USER = 'admin'
# DB_PASSWORD = 'testpwd!'
# DB_HOST = 'localhost'
# DB_NAME = 'igospace'

# SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


# Update the SQLALCHEMY_DATABASE_URI to use environment variables
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "postgresql://admin:testpwd!@localhost/igospace"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False