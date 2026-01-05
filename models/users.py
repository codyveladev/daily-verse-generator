# models/users.py
from flask_login import UserMixin
from datetime import date
from . import db
from .user_moods import UserMood  # Safe import – no circular issue anymore

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(150), nullable=False)

    # String-based relationships (safe)
    moods = db.relationship('UserMood', backref='user', lazy=True, order_by='UserMood.date.desc()')
    quotes = db.relationship('DailyQuote', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_current_mood(self):
        today = date.today()
        today_mood = UserMood.query.filter_by(user_id=self.id, date=today).first()
        if today_mood:
            return today_mood.mood

        # Fall back to most recent mood
        if self.moods:
            return self.moods[0].mood

        return None