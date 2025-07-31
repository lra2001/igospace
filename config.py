from dotenv import load_dotenv
import os

load_dotenv()

# Use DATABASE_URL from environment variables or local db
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://admin:testpwd!@localhost:5432/igospace")
SQLALCHEMY_TRACK_MODIFICATIONS = False