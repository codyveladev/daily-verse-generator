# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Secret key for session security and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-secret-key-change-in-production'

    # Database configuration
    # Uses SQLite by default; stored in the Flask instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Grok API key (from xAI) – used for intelligent verse selection
    GROK_API_KEY = os.environ.get('GROK_API_KEY')

    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')