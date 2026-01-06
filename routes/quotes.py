# routes/quotes.py
import requests
from datetime import date
from flask import current_app
from models.daily_quotes import DailyQuote
from models.users import db
from google import genai


def auto_generate_quote(user_id, mood):
    client = genai.Client()
    today = date.today()

    # Avoid duplicates
    existing = DailyQuote.query.filter_by(
        user_id=user_id, date=today, topic=mood
    ).first()

    if existing:
        return

    prompt = f"""Suggest ONE specific Bible verse (book, chapter, verse) that is most encouraging and relevant for someone feeling {mood}.
Focus on comfort, hope, or strength from God.
Output ONLY the reference in format: Book Chapter:Verse
Example: Psalm 34:18"""

    try:
        # 1. Check your model name (ensure it's a valid version like 'gemini-1.5-flash')
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        print(response, response.text)

        # 2. Access the text attribute directly
        reference = response.text.strip()

        if ":" not in reference:
            reference = "Psalm 23:1"

    except Exception as e:
        print(f"AI Error: {e}")
        reference = "Philippians 4:13"

        # Fetch verse text
    ref_url = reference.replace(" ", "+").lower()

    try:
        verse_resp = requests.get(f"https://bible-api.com/{ref_url}", timeout=10)
        verse_resp.raise_for_status()
        data = verse_resp.json()
        verse_text = data["text"].strip()
        full_reference = data["reference"]
    except Exception:
        verse_text = "I can do all this through him who gives me strength."
        full_reference = reference

    new_quote = DailyQuote(
        user_id=user_id,
        date=today,
        topic=mood,
        reference=full_reference,
        text=verse_text,
    )
    db.session.add(new_quote)
    db.session.commit()
