from dotenv import load_dotenv
import os

load_dotenv()

# Use DATABASE_URL from environment variables or default to local db on dev
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///igospace.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False