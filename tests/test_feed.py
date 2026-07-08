"""
tests/test_feed.py — Mixtape

Tests for the "Friends Listening Now" feed logic.
"""

import pytest
from datetime import datetime, timedelta, timezone
from app import create_app, db
from models import User, Song, ListeningEvent, friendships
from services.feed_service import get_friends_listening_now


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def seed_friends(app):
    """A user with one friend who listened yesterday evening and one who listened today."""
    with app.app_context():
        user = User(username="nova", email="nova@example.com")
        friend_yesterday = User(username="darius", email="darius@example.com")
        friend_today = User(username="simone", email="simone@example.com")
        db.session.add_all([user, friend_yesterday, friend_today])
        db.session.flush()

        db.session.execute(friendships.insert().values(user_id=user.id, friend_id=friend_yesterday.id))
        db.session.execute(friendships.insert().values(user_id=user.id, friend_id=friend_today.id))

        song = Song(title="Track", artist="Someone", shared_by=user.id)
        db.session.add(song)
        db.session.flush()

        now = datetime.now(timezone.utc)
        today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)

        # Listened at 11pm yesterday, well within a rolling 24h window — should NOT appear
        db.session.add(ListeningEvent(
            user_id=friend_yesterday.id, song_id=song.id,
            listened_at=today_start - timedelta(hours=1),
        ))
        # Listened just after midnight today — should appear
        db.session.add(ListeningEvent(
            user_id=friend_today.id, song_id=song.id,
            listened_at=today_start + timedelta(minutes=5),
        ))

        db.session.commit()
        yield {"user": user, "friend_yesterday": friend_yesterday, "friend_today": friend_today}


def test_excludes_friend_who_listened_yesterday(app, seed_friends):
    """A listen from before today's midnight should not appear, even if under 24 hours old."""
    with app.app_context():
        feed = get_friends_listening_now(seed_friends["user"].id)
        usernames = [entry["friend"]["username"] for entry in feed]
        assert "darius" not in usernames


def test_includes_friend_who_listened_today(app, seed_friends):
    """A listen from earlier today should appear."""
    with app.app_context():
        feed = get_friends_listening_now(seed_friends["user"].id)
        usernames = [entry["friend"]["username"] for entry in feed]
        assert "simone" in usernames


def test_no_friends_returns_empty_list(app):
    """A user with no friends should get an empty feed without error."""
    with app.app_context():
        user = User(username="loner", email="loner@example.com")
        db.session.add(user)
        db.session.commit()
        assert get_friends_listening_now(user.id) == []
