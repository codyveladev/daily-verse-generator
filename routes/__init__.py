# routes/__init__.py
from flask import Blueprint

# We'll register blueprints in app.py
auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
quotes_bp = Blueprint('quotes', __name__)
community_bp = Blueprint('community', __name__)

# Import routes to register them
from . import auth, user, quotes, community