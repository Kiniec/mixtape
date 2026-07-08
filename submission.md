## AI
<!-- - Section describes at least 2 specific uses of AI tools during codebase navigation or debugging — what was asked and what the tool helped explain or trace.
- Section is honest about the collaboration — describes at least one instance where the student verified something the AI explained, or where the AI's output was incomplete and the student had to course-correct.
- Descriptions are specific enough to distinguish real AI collaboration from generic statements like "I used AI to help with code." -->
 In this project Copilot was asked to show a sample codebase mapping suggestions for the projects entry of a codebase map. Claude code was asked to explain how to fully reproduce a bug professional and effectively. Claude Code was also instructed to review code, determine what may have been a cause and make suggestions. It was also asked to add suggestions for regression testing.   

 ---

## Codebase map
```
mixtape/
├── app.py                      # Flask application factory; configures SQLAlchemy, registers blueprints, and initializes the application
├── routes/                     # API endpoints organized into Flask blueprints
│   ├── songs.py                # Song sharing, search, and rating routes
│   ├── playlists.py            # Playlist creation and song management
│   ├── users.py                # User profiles, streaks, notifications
│   └── feed.py                 # Friends listening now, activity feed
├── services/
│   ├── streak_service.py       # Listening streak logic
│   ├── feed_service.py         # Friends listening now feed logic
│   ├── search_service.py       # Song search logic
│   ├── notification_service.py # Notification creation and retrieval
│   └── playlist_service.py     # Playlist retrieval logic
├── tests/
│   ├── test_streaks.py         # Tests for streak functionality
│   ├── test_search.py          # Tests for search functionality
│   └── test_playlists.py       # Tests for playlist functionality

├── seed_data.py                # Populates DB with test data
|__ models.py                   # SQLAlchemy database models and schema definitions
├── requirements.txt            # Project dependencies
|__ submission.md               # Contains submission for project
└── .gitignore                  # Files and directories excluded from version control

```

| Component| Description 
|--------|-------- 
| app.py |  Creates a Flask app factory and database setup using a SQLALCHEMY database retrieving blueprints of songs, users, playlists, and feeds
| routes |  Endpoints into each database blueprint are handled by routes 
|songs.py|   Song sharing, searching, and rating requests are handled through search services and returned as a jsonify document.
| playlist.py | Handles playlist creation, updates, and song management requests.
| users.py | Handles user profile, streak, and notification requests.
| feed.py | Handles activity feed and friend listening requests.
| services/ | Contains business logic used by route handlers.
| streak_service.py | Calculates and updates user listening streaks.
| feed_services.py | Handles activity feed and friend listening requests. 
| search_service.py | 
notification_service.py | 
playlist_service.py \ |
models.py |
tests/ |
seed_data.py |
requirements.txt |
submission.md |
.gitignore |





## How you reproduced it
<!-- what inputs, what sequence of actions, or what data condition triggered the behavior -->

### Issue #1 -  My listening streak keeps resetting
- To reproduce bug: 
    - the error code line is in streak_service.py at line 73, `today.weekday() != 6`
    - the data condition that triggers the behavior is`Sunday date`. 
    - call update_listening_streak(user, saturday_dt) then update_listening_streak(user, sunday_dt) with fixed datetime objects and assert the streak.
    - pytest tests/test_streaks.py -v — this test fails today (1 == 2 assertion error)
- Expected: streak goes from 12 to 13. 
- Actual: streak shows 1.
 
### Issue #2 — Friends Listening Now shows people from yesterday
- To reproduce bug: 
    - the error code is in feed_service.py, `RECENT_THRESHOLD = timedelta(hours=24)`
    -  the data condition that triggers the behavior  `2+ tag join fan-out`
1. Find nova's id: sqlite3 mixtape.db "select id from user where username='nova';"
2. GET /feed/<nova>/listening-now
3. Observe friends whose only event is the 10h/18h-ago one still show up as "listening now" — those easily correspond to "yesterday evening" depending on when you run it, matching the report. 
- Expected: only genuinely-today listens should appear.
- Actual: friends whose last listen was yesterday evening still show up the next morning.

### Issue #3 — The same song keeps showing up twice in search
- To reproduce bug:
    - the error code is in search_service.py, .outerjoin(song_tags, ...) with no `.distinct()`
    -  the data condition that triggers the behavior `multi-tag song`
1. GET /songs/search?q=Anthem
2. Count entries for "Crown Heights Anthem" in results — expect 1, the join fans out one row per tag so a 3-tag song returns 3 identical entries. A song with 0 or 1 tags won't duplicate (only 1 join row), which is exactly the "inconsistent" behavior described — worth confirming the count yourself since it depends on how many tags the matched song has.
- Expected: each matching song appears exactly once. 
- Actual: some songs appear once, others two or three times, for a single-song match.



### Issue #4 - I got notified when a friend added my song to a playlist but not when they rated it
- To reproduce bug:
    - the error code is in notification_service.py
    - the data condition that triggers the behavior `rating vs. playlist-add code path`
1. Get a seeded song shared by nova and nova's id (recipient), plus another user's id (e.g. darius) as rater.
2. POST /songs/<song_id>/rate {"user_id": darius_id, "score": 5} — confirm 201 and the rating is saved.
3. GET /users/<nova_id>/notifications — expect a new rating notification; you'll only see the pre-seeded "song_added_to_playlist" one (seed_data plants exactly one working notification as your control/baseline for comparison — see its comment # so students can see the correct pattern when investigating Issue #4).
- Expected: a notification for the rating, same as for the playlist add. 
- Actual: rating is saved (it shows on the song), but no notification is ever created.


### Issue #5 — The last song in a playlist never shows up
- To reproduce bug:
    - the error code is in playlist_service.py line66
    - the data condition that triggers the behavior `last-position slice`
1. sqlite3 mixtape.db "select id from playlist where name='Friday Energy';"
2. GET /playlists/<playlist_id>/songs — expect count: 7, get count: 6.
3. POST /playlists/<playlist_id>/songs {"song_id": <some_other_song_id>, "added_by": <darius_id>}
4. GET /playlists/<playlist_id>/songs again — the previously-missing 7th song now appears, and the just-added 8th is now the one missing. Confirms it's always truncating the last-by-position entry, not a specific song.


Expected: every song in the playlist is returned, including the newest. Actual: the most recently added song is always missing; adding another song "frees" the previous one and hides the new one instead.



## Root Cause Analysis 


1. Issue number and title 
Bug Issue #1  with title "My listening streak keeps resetting"
2. Reproduce the bug
Verified the bug existed with the mixtape database.  `today.weekday() != 6` was searched to see why the bug was resetting. This what was triggering the behavior of the bug.  
3. Found the root cause
The root cause was found in service/ folder streak_service.py. First went to services and then to streak_service to see what was causing the streak to resent. Reviewed docstring. 
4. The root cause 
The root cause was the user streak was not adding up to the music days listened to. 

5. Fix and side-effect check 
Removed elif last day equals 6 in `update_listening_streak()` which ultimately resets the streak. Checked test_streaks.py for functionally. 



---

1. Issue number and title 
Bug Issue #2  with title "Friends Listening Now shows people from yesterday"
2. Reproduce the bug
Verified the bug was in feed_service.py. Used user's id to get information on listening-now. Viewed what friends had listened recently.
Services/feed_service.py:13 used RECENT_THRESHOLD = timedelta(hours=24) — a rolling 24-hour window from the moment of the request, not a "since today started" boundary. An 11pm listen is still well inside a 24h window at 9am the next morning, so it kept showing up as "listening now."
3. Found the root cause
The root cause was found in service/ folder and in feed_service.py. User complained about feed issues, went to feed_services to verify. Reviewed docstring. 
4. The root cause 
The root cause of friends listening now shows people from yesterday the cutoff time was not today and included any recent listening friends.
RECENT_THRESHOLD = timedelta(hours=24) in services/feed_service.py:13 creates a rolling 24-hour window, not a "today" boundary — so an 11pm listen is still inside the window at 9am the next day (only 10 hours later). The report is explicit about the expected behavior: "only friends who have listened today appear." The fix is to cut off at the start of the current UTC calendar day instead of 24 hours back.
5. Fix and side-effect check 
 A test was added to tests - test_feed.py since there is no test for test_feed.py. Return a list of friends of today and removed recently and added a cut off time. 

---


1. Issue number and title 
Bug Issue #3  with title "The same song keeps showing up twice in search"
2. Reproduce the bug
Reproduced the bug by requesting query of "Anthem" and counting the entries for the query. Tags were not duplicating only on row joins.
3. Found the root cause
 The root cause was found in search_service.py , .outerjoin(). The current does not have a .distinct(). 
4. The root cause 
 The join to song_tags isn't used for filtering at all — no WHERE clause touches it. It's dead weight that only causes row fan-out: a song with 3 tags joins against 3 rows in song_tags, so the raw SQL returns 3 rows for that one song (I confirmed this directly — raw SQL returns 3 rows for a 3-tag song, verified with EXPLAIN-equivalent execution against an in-memory DB).
5. Fix and side-effect check 
The fix for bug was to removed the unused .outerjoin(song_tags, Song.id == song_tags.c.song_id) from search_songs() and unused Tag/song_tags imports. The query now just filters Song directly on title/artist; to_dict() still populates tags via the model's existing lazy="subquery" relationship, untouched.



---


1. Issue number and title 
Bug Issue #4  with title "I got notified when a friend added my song to a playlist but not when they rated it"
2. Reproduce the bug
 
3. Found the root cause
The root was cause was found in services/notification_services.py. User complained of not being notified. The service notification was the first location to review. 
4. The root cause 
notification_service.rate_song() (services/notification_service.py) saved/updated the Rating row but never called create_notification() — unlike add_to_playlist(), which does notify the sharer. The rating itself worked fine (visible on the song, as aaliya observed); only the notification side effect was missing.
5. Fix and side-effect check 
A verification test of tests/test_notifications.py was added to tests due to no test for notifications. The fix for the notification was to notify the song sharer after the rating was committed.

---


1. Issue number and title 
Bug Issue #5  with title "The last song in a playlist never shows up"
2. Reproduce the bug
  Reproduced the bug by querying the database and the last song played.  
3. Found the root cause
The root cause was found in  playlist.songs.append(song). The user complained of last song of the playlist never showing up fot them. 
4. The root cause 
 playlist.songs.append(song) uses SQLAlchemy's plain secondary= relationship shortcut, which only inserts the two foreign-key columns (playlist_id, song_id) into playlist_entries. That table also has position and added_by, both nullable=False with no default — so every insert failed with IntegrityError.

5. Fix and side-effect check 
Insert directly into the playlist_entries association table instead of using the relationship shortcut, computing the next position as max(existing positions) + 1 (0 if the playlist is empty) and passing added_by explicitly. Also removed the unused get_playlist_songs import that was dead code in this function.

--- 



