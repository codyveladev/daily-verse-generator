from datetime import date
from models.users import db

class DailyQuote(db.Model):
    __tablename__ = 'daily_quote'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    topic = db.Column(db.String(100), nullable=False)  # matches the mood, e.g., "grief"
    reference = db.Column(db.String(100), nullable=False)  # e.g., "Psalm 34:18"
    text = db.Column(db.Text, nullable=False)

    # One quote per user per day per topic (mood)
    __table_args__ = (db.UniqueConstraint('user_id', 'date', 'topic', name='unique_daily_quote'),)

    def __repr__(self):
        return f'<DailyQuote {self.reference} for {self.topic} on {self.date}>'