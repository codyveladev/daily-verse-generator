# routes/community.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models.posts import Post, PostVote
from models.comments import Comment, CommentVote
from models.users import db
from . import community_bp

@community_bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@community_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not title or not body:
            flash('Title and body are required.', 'danger')
        else:
            post = Post(title=title, body=body, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', 'success')
            return redirect(url_for('community.index'))
    return render_template('new_post.html')

@community_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        body = request.form['body']
        if body:
            comment = Comment(body=body, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added.', 'success')
        return redirect(url_for('community.view_post', post_id=post_id))
    return render_template('view_post.html', post=post)

def handle_vote(model, vote_model, item_id):
    item = model.query.get_or_404(item_id)
    existing_vote = vote_model.query.filter_by(user_id=current_user.id, **{f'{model.__name__.lower()}_id': item_id}).first()
    value = int(request.form['value'])  # +1 or -1

    if existing_vote:
        if existing_vote.value == value:
            db.session.delete(existing_vote)  # Remove vote
        else:
            existing_vote.value = value  # Flip vote
    else:
        vote = vote_model(value=value, user_id=current_user.id, **{f'{model.__name__.lower()}_id': item_id})
        db.session.add(vote)
    db.session.commit()
    return redirect(request.referrer or url_for('community.index'))

@community_bp.route('/community/vote/post/<int:post_id>', methods=['POST'])
@login_required
def vote_post(post_id):
    return handle_vote(Post, PostVote, post_id)

@community_bp.route('/community/vote/comment/<int:comment_id>', methods=['POST'])
@login_required
def vote_comment(comment_id):
    return handle_vote(Comment, CommentVote, comment_id)