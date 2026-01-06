# populate_test_data.py
from datetime import date, timedelta, datetime
from app import create_app
from models import db, User
from models.user_moods import UserMood
from models.daily_quotes import DailyQuote
from models.soap_journal import SOAPJournal
from models.posts import Post, PostVote
from models.comments import Comment, CommentVote
from werkzeug.security import generate_password_hash
import random

app = create_app()

with app.app_context():
    print("Clearing all existing data...")
    # Clear everything in correct order
    db.session.query(SOAPJournal).delete()
    db.session.query(CommentVote).delete()
    db.session.query(PostVote).delete()
    db.session.query(Comment).delete()
    db.session.query(Post).delete()
    db.session.query(DailyQuote).delete()
    db.session.query(UserMood).delete()
    db.session.query(User).delete()
    db.session.commit()

    print("Creating test users...")
    users_data = [
        {"username": "alice", "email": "alice@example.com", "full_name": "Alice Johnson"},
        {"username": "bob", "email": "bob@example.com", "full_name": "Bob Smith"},
        {"username": "charlie", "email": "charlie@example.com", "full_name": "Charlie Brown"},
        {"username": "diana", "email": "diana@example.com", "full_name": "Diana Prince"},
    ]

    users = []
    for u in users_data:
        user = User(
            username=u["username"],
            email=u["email"],
            full_name=u["full_name"],
            password=generate_password_hash("test123")
        )
        db.session.add(user)
        db.session.commit()
        users.append(user)
        print(f"   Created: {user.username}")

    # === Daily verses + moods (30 days) ===
    moods = ["grief", "anxiety", "joy", "peace", "hope", "strength", "depression", "encouragement", "fear", "loneliness"]
    verses = [
        ("The Lord is close to the brokenhearted and saves those who are crushed in spirit.", "Psalm 34:18"),
        ("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.", "Philippians 4:6-7"),
        ("May the God of hope fill you with all joy and peace as you trust in him.", "Romans 15:13"),
        ("I can do all this through him who gives me strength.", "Philippians 4:13"),
        ("Peace I leave with you; my peace I give you.", "John 14:27"),
        ("Be strong and courageous. Do not be afraid; do not be discouraged.", "Joshua 1:9"),
        ("Cast all your anxiety on him because he cares for you.", "1 Peter 5:7"),
        ("The joy of the Lord is your strength.", "Nehemiah 8:10"),
    ]

    today = date.today()
    quotes_by_user = {}

    print("Generating verse history and SOAP journals...")
    for user in users:
        user_quotes = []
        for i in range(30):
            past_date = today - timedelta(days=i + 1)
            mood = moods[i % len(moods)]
            text, ref = verses[i % len(verses)]

            # Mood
            mood_entry = UserMood(user_id=user.id, date=past_date, mood=mood)
            db.session.add(mood_entry)

            # Quote
            quote = DailyQuote(user_id=user.id, date=past_date, topic=mood, reference=ref, text=text)
            db.session.add(quote)
            db.session.flush()  # Get quote.id
            user_quotes.append(quote)

            # 60% chance of having a SOAP journal entry
            if random.random() < 0.6:
                journal = SOAPJournal(
                    quote_id=quote.id,
                    observation=random.choice([
                        "God feels near even in suffering.",
                        "This verse reminds me to bring everything to God in prayer.",
                        "Hope is not based on circumstances but on who God is.",
                        "My strength comes from Christ, not myself."
                    ]),
                    application=random.choice([
                        "I will pray instead of worry today.",
                        "I’ll reach out to someone who’s hurting.",
                        "I’ll rest in God’s presence instead of striving.",
                        "I’ll choose joy even when things are hard."
                    ]),
                    prayer=random.choice([
                        "Lord, help me trust You more today.",
                        "Thank You for Your peace that passes understanding.",
                        "Give me strength for what’s ahead.",
                        "Draw near to me as I draw near to You."
                    ])
                )
                db.session.add(journal)

        quotes_by_user[user.id] = user_quotes

        db.session.commit()
        print(f"   {user.username}: 30 days of verses + journals")

    # === Community Posts & Comments ===
    print("Creating community posts, comments, and votes...")

    sample_posts = [
        {"title": "How has God spoken to you this week?", "body": "I’ve been going through a tough season, but today’s verse about strength in Philippians really hit home. What about you?"},
        {"title": "Prayer Request", "body": "Please pray for my family — we’re facing some health challenges. Grateful for this community."},
        {"title": "Favorite Verse for Anxiety?", "body": "Mine is Philippians 4:6-7. What verse helps you when anxiety creeps in?"},
        {"title": "Grateful Today", "body": "Just wanted to say I’m thankful for this app and all of you. It’s been a lifeline on hard days."},
    ]

    for post_data in sample_posts:
        poster = random.choice(users)
        post = Post(title=post_data["title"], body=post_data["body"], user_id=poster.id)
        db.session.add(post)
        db.session.flush()

        # Each post gets 2–5 comments
        num_comments = random.randint(2, 5)
        for _ in range(num_comments):
            commenter = random.choice([u for u in users if u.id != poster.id])  # Not the poster
            comment = Comment(body=random.choice([
                "Thank you for sharing this. Praying for you.",
                "That verse has carried me through hard times too.",
                "So encouraging — needed this today.",
                "Amen! God is faithful.",
                "Beautiful reminder. Thank you."
            ]), user_id=commenter.id, post_id=post.id)
            db.session.add(comment)
            db.session.flush()

            # Random upvotes/downvotes on comment
            for voter in random.sample(users, random.randint(1, len(users)-1)):
                if random.random() < 0.7:  # 70% chance to vote
                    vote_val = 1 if random.random() < 0.9 else -1  # Mostly upvotes
                    vote = CommentVote(user_id=voter.id, comment_id=comment.id, value=vote_val)
                    db.session.add(vote)

        # Votes on the post itself
        for voter in random.sample(users, random.randint(2, len(users))):
            vote_val = 1 if random.random() < 0.85 else -1
            vote = PostVote(user_id=voter.id, post_id=post.id, value=vote_val)
            db.session.add(vote)

    db.session.commit()
    print("   Community posts, comments, and votes created")

    print("\n🎉 All test data populated successfully!")
    print("Login credentials:")
    for u in users_data:
        print(f"   Username: {u['username']} | Password: test123")
    print("\nFeatures now populated:")
    print("   • 30 days of personalized verses + moods")
    print("   • SOAP journal entries for many days")
    print("   • Active community with posts, comments, and votes")