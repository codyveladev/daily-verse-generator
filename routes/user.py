# routes/user.py
from datetime import date
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models.users import User, db
from models.user_moods import UserMood
from . import user_bp

from models.daily_quotes import DailyQuote
from models.users import db
from models.soap_journal import SOAPJournal

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    current_mood = current_user.get_current_mood()

    today_quote = None
    if current_mood:
        from models.daily_quotes import DailyQuote
        today_quote = DailyQuote.query.filter_by(
            user_id=current_user.id,
            date=today,
            topic=current_mood
        ).first()

        if not today_quote:
            from .quotes import auto_generate_quote
            auto_generate_quote(current_user.id, current_mood)
            today_quote = DailyQuote.query.filter_by(
                user_id=current_user.id,
                date=today,
                topic=current_mood
            ).first()

    return render_template('dashboard.html', current_mood=current_mood, today_quote=today_quote)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form['full_name']
        current_user.email = request.form['email']
        current_user.preferred_translation = request.form['preferred_translation']

        if User.query.filter(User.email == current_user.email, User.id != current_user.id).first():
            flash('Email already in use by another account.', 'danger')
        else:
            db.session.commit()
            flash('Profile updated successfully!', 'success')

    return render_template('profile.html')

@user_bp.route('/set_mood', methods=['GET', 'POST'])
@login_required
def set_mood():
    moods = [
        'grief', 'depression', 'temptation', 'anxiety', 'loneliness',
        'fear', 'anger', 'discouragement', 'hope', 'strength',
        'peace', 'forgiveness', 'encouragement', 'healing', 'joy'
    ]

    today = date.today()
    current_mood_obj = UserMood.query.filter_by(user_id=current_user.id, date=today).first()
    current_mood = current_mood_obj.mood if current_mood_obj else current_user.get_current_mood()

    if request.method == 'POST':
        new_mood = request.form['mood']

        if current_mood_obj:
            current_mood_obj.mood = new_mood
        else:
            mood_entry = UserMood(user_id=current_user.id, mood=new_mood)
            db.session.add(mood_entry)

        db.session.commit()
        flash('Your current struggle has been updated! A new daily quote will be generated.', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('set_mood.html', moods=moods, current_mood=current_mood)

@user_bp.route('/clear_quotes')
@login_required
def clear_quotes():
    # Optional: Add extra protection, e.g., only allow specific users
    # if current_user.username != 'admin':  # Example
    #     flash('Access denied.', 'danger')
    #     return redirect(url_for('user.dashboard'))

    try:
        num_deleted = db.session.query(DailyQuote).delete()
        db.session.commit()
        flash(f'Cleared {num_deleted} daily quotes from the database.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error clearing quotes. Try again.', 'danger')

    return redirect(url_for('user.dashboard'))

@user_bp.route('/journal/<int:quote_id>', methods=['GET', 'POST'])
@login_required
def soap_journal(quote_id):
    quote = DailyQuote.query.get_or_404(quote_id)

    # Security: only allow editing own quotes
    if quote.user_id != current_user.id:
        abort(403)

    journal = quote.soap_journal or SOAPJournal(quote_id=quote.id)

    if request.method == 'POST':
        journal.observation = request.form['observation']
        journal.application = request.form['application']
        journal.prayer = request.form['prayer']

        if not quote.soap_journal:
            db.session.add(journal)

        db.session.commit()
        flash('Your SOAP journal entry has been saved!', 'success')
        return redirect(url_for('user.soap_journal', quote_id=quote_id))

    return render_template('soap_journal.html', quote=quote, journal=journal)

@user_bp.route('/journal')
@login_required
def journal_history():
    # Get all quotes that have a journal entry, ordered newest first
    journal_quotes = DailyQuote.query.filter(
        DailyQuote.user_id == current_user.id,
        DailyQuote.soap_journal != None
    ).order_by(DailyQuote.date.desc()).all()

    return render_template('journal_history.html', journal_quotes=journal_quotes)