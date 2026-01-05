# routes/quotes.py
import requests
from datetime import date
from flask import current_app
from models.daily_quotes import DailyQuote
from models.users import db

def auto_generate_quote(user_id, mood):
    grok_key = current_app.config.get('GROK_API_KEY')
    today = date.today()

    # Avoid duplicates
    existing = DailyQuote.query.filter_by(user_id=user_id, date=today, topic=mood).first()
    if existing:
        return

    if not grok_key:
        # Fallback
        fallback_text = "The Lord is close to the brokenhearted and saves those who are crushed in spirit."
        fallback_ref = "Psalm 34:18"
        new_quote = DailyQuote(user_id=user_id, topic=mood, reference=fallback_ref, text=fallback_text)
        db.session.add(new_quote)
        db.session.commit()
        return

    prompt = f"""Suggest ONE specific Bible verse (book, chapter, verse) that is most encouraging and relevant for someone feeling {mood}.
Focus on comfort, hope, or strength from God.
Output ONLY the reference in format: Book Chapter:Verse
Example: Psalm 34:18"""

    try:
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {grok_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'grok-4',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.5,
                'max_tokens': 50
            },
            timeout=15
        )
        response.raise_for_status()
        reference = response.json()['choices'][0]['message']['content'].strip()

        if ':' not in reference:
            reference = 'Psalm 23:1'

    except Exception:
        reference = 'Philippians 4:13'

    # Fetch verse text
    ref_url = reference.replace(' ', '+').lower()
    try:
        verse_resp = requests.get(f'https://bible-api.com/{ref_url}', timeout=10)
        verse_resp.raise_for_status()
        data = verse_resp.json()
        verse_text = data['text'].strip()
        full_reference = data['reference']
    except Exception:
        verse_text = "I can do all this through him who gives me strength."
        full_reference = reference

    new_quote = DailyQuote(
        user_id=user_id,
        date=today,
        topic=mood,
        reference=full_reference,
        text=verse_text
    )
    db.session.add(new_quote)
    db.session.commit()