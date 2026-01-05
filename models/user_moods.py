from datetime import date
from models.users import db

class UserMood(db.Model):
    __tablename__ = 'user_mood'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    mood = db.Column(db.String(100), nullable=False)  # e.g., "grief", "anxiety", "hope"

    # Ensure only one mood entry per user per day
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='unique_daily_mood'),)

    def __repr__(self):
        return f'<UserMood {self.mood} on {self.date} for User {self.user_id}>'