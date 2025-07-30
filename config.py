from dotenv import load_dotenv
import os

load_dotenv()

# Use DATABASE_URL from environment variables
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False