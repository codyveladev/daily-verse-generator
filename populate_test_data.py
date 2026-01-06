# populate_test_data.py
from datetime import date, timedelta
from app import create_app
from models import db, User
from models.user_moods import UserMood
from models.daily_quotes import DailyQuote
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Clear existing data (optional – comment out if you want to keep current data)
    db.session.query(DailyQuote).delete()
    db.session.query(UserMood).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create test users
    users = [
        {"username": "alice", "email": "alice@example.com", "full_name": "Alice Johnson", "password": "test123"},
        {"username": "bob", "email": "bob@example.com", "full_name": "Bob Smith", "password": "test123"},
        {"username": "charlie", "email": "charlie@example.com", "full_name": "Charlie Brown", "password": "test123"},
    ]

    created_users = []
    for u in users:
        user = User(
            username=u["username"],
            email=u["email"],
            full_name=u["full_name"],
            password=generate_password_hash(u["password"])
        )
        db.session.add(user)
        db.session.commit()
        created_users.append(user)
        print(f"Created user: {user.username}")

    # Sample moods and verses
    moods = ["grief", "anxiety", "hope", "joy", "peace", "strength", "depression", "encouragement"]
    sample_verses = [
        ("The Lord is close to the brokenhearted and saves those who are crushed in spirit.", "Psalm 34:18"),
        ("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.", "Philippians 4:6"),
        ("May the God of hope fill you with all joy and peace as you trust in him.", "Romans 15:13"),
        ("I can do all this through him who gives me strength.", "Philippians 4:13"),
        ("Peace I leave with you; my peace I give you.", "John 14:27"),
        ("Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.", "Joshua 1:9"),
        ("Cast all your anxiety on him because he cares for you.", "1 Peter 5:7"),
        ("The joy of the Lord is your strength.", "Nehemiah 8:10"),
    ]

    # Generate data for the last 30 days for each user
    today = date.today()  # Will be around January 2026
    for user in created_users:
        for i in range(30):  # 30 days of history
            past_date = today - timedelta(days=i+1)  # Skip today to avoid duplicate
            mood = moods[i % len(moods)]  # Rotate moods

            # Set mood for that day
            mood_entry = UserMood(user_id=user.id, date=past_date, mood=mood)
            db.session.add(mood_entry)

            # Add quote for that day
            text, ref = sample_verses[i % len(sample_verses)]
            quote = DailyQuote(
                user_id=user.id,
                date=past_date,
                topic=mood,
                reference=ref,
                text=text
            )
            db.session.add(quote)

        db.session.commit()
        print(f"Populated 30 days of data for {user.username}")

    print("\nTest data population complete!")
    print("You can now log in with:")
    for u in users:
        print(f"   Username: {u['username']}  Password: test123")