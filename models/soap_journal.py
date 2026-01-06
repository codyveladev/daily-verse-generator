# models/soap_journal.py
from datetime import date
from . import db
from models.daily_quotes import DailyQuote

class SOAPJournal(db.Model):
    __tablename__ = 'soap_journal'

    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('daily_quote.id'), nullable=False, unique=True)  # One journal per quote
    observation = db.Column(db.Text, nullable=True)
    application = db.Column(db.Text, nullable=True)
    prayer = db.Column(db.Text, nullable=True)

    # Relationship back to quote
    quote = db.relationship('DailyQuote', backref='soap_journal', uselist=False)

    def __repr__(self):
        return f'<SOAPJournal for Quote {self.quote_id}>'