"""
tests/test_notifications.py — Mixtape

Tests for notification creation logic.
"""

import pytest
from app import create_app, db
from models import User, Song, Notification
from services.notification_service import rate_song


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def seed_song(app):
    """A song shared by one user, to be rated by another."""
    with app.app_context():
        sharer = User(username="aaliya", email="aaliya@example.com")
        rater = User(username="kenji", email="kenji@example.com")
        db.session.add_all([sharer, rater])
        db.session.flush()

        song = Song(title="Golden Hour", artist="Solange K", shared_by=sharer.id)
        db.session.add(song)
        db.session.commit()

        yield {"sharer": sharer, "rater": rater, "song": song}


def test_rating_a_song_notifies_the_sharer(app, seed_song):
    """Rating someone else's song should create a notification for the sharer."""
    with app.app_context():
        sharer_id = seed_song["sharer"].id
        rater_id = seed_song["rater"].id
        song_id = seed_song["song"].id

        rate_song(rater_id, song_id, 5)

        notifications = db.session.query(Notification).filter_by(user_id=sharer_id).all()
        assert len(notifications) == 1
        assert notifications[0].notification_type == "song_rated"


def test_rating_your_own_song_does_not_notify_yourself(app, seed_song):
    """Rating your own shared song should not create a self-notification."""
    with app.app_context():
        sharer_id = seed_song["sharer"].id
        song_id = seed_song["song"].id

        rate_song(sharer_id, song_id, 4)

        notifications = db.session.query(Notification).filter_by(user_id=sharer_id).all()
        assert notifications == []
