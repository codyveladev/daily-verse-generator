# models/comments.py
from datetime import datetime
from . import db

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='comments')
    votes = db.relationship('CommentVote', backref='comment', lazy=True, cascade='all, delete-orphan')

    @property
    def score(self):
        return sum(vote.value for vote in self.votes)

class CommentVote(db.Model):
    __tablename__ = 'comment_vote'
    __table_args__ = (db.UniqueConstraint('user_id', 'comment_id', name='unique_comment_vote'),)

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # +1 or -1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)