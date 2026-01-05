# models/user_moods.py
from datetime import date
from . import db

class UserMood(db.Model):  # db comes from models/__init__.py when imported
    __tablename__ = 'user_mood'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    mood = db.Column(db.String(100), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='unique_daily_mood'),)

    def __repr__(self):
        return f'<UserMood {self.mood} on {self.date} for User {self.user_id}>'