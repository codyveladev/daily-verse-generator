# models/daily_quotes.py
from datetime import date
from . import db

class DailyQuote(db.Model):
    __tablename__ = 'daily_quote'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    reference = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'date', 'topic', name='unique_daily_quote'),)

    def __repr__(self):
        return f'<DailyQuote {self.reference} for {self.topic} on {self.date}>'