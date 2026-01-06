# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance here
db = SQLAlchemy()

# Import the models AFTER db is created so they can use it
# This avoids circular imports completely
from .users import User
from .user_moods import UserMood
from .daily_quotes import DailyQuote
from .posts import Post, PostVote
from .comments import Comment, CommentVote