## Codebase orientation 
## Fix at least 3 of the 5 bugs
- fix each bug 
- write a complete root cause analysis entry covering all 5 fields 
## One commit per fis 
- Each bug must have own commit on the bugfix/mixtape branch 
- using conventional commit format with a descriptive message

## Fix 4th Bug 
- Fix fourth issue with a complete root cause analysis entry 
## Fix all 5 bugs
- Fix the remaining fifth issue with a complete root cause analysis


## codebase map
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

 
|Patterns| Description | 
|-----|----| 
|  Patterns of the folders lead directly to the services folder and to the database. 
| Pattern I noticed: every route delegates immediately to a service function. The routes do input parsing and response formatting; all business logic lives in services/.




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
The root cause was found in service/ folder streak_service. First went to services and then to streak_service to see what was causing the streak to resent. 
4. The root cause 
The root cause was the user streak was not adding up to the music days listened to. 
5. Fix and side-effect check 
Removed elif last day equals 6 in `update_listening_streak()` which ultimately resets the streak. Checked test_streaks.py for functionally. 
---

1. Issue number and title 
Bug Issue #2  with title "Friends Listening Now shows people from yesterday"
2. Reproduce the bug
Verified the bug existed with the mixtape database.  `today.weekday() != 6` was searched to see why the bug was resetting. This what was triggering the behavior of the bug.  
3. Found the root cause
The root cause was found in service/ folder streak_service. First went to services and then to streak_service to see what was causing the streak to resent. 
4. The root cause 
The root cause was the user streak was not adding up to the music days listened to. 
5. Fix and side-effect check 
---

1. Issue number and title 
Bug Issue #3  with title "The same song keeps showing up twice in search"
2. Reproduce the bug
Verified the bug existed with the mixtape database.  `today.weekday() != 6` was searched to see why the bug was resetting. This what was triggering the behavior of the bug.  
3. Found the root cause
The root cause was found in service/ folder streak_service. First went to services and then to streak_service to see what was causing the streak to resent. 
4. The root cause 
The root cause was the user streak was not adding up to the music days listened to. 
5. Fix and side-effect check 
---

1. Issue number and title 
Bug Issue #4  with title "I got notified when a friend added my song to a playlist but not when they rated it"
2. Reproduce the bug
Verified the bug existed with the mixtape database.  `today.weekday() != 6` was searched to see why the bug was resetting. This what was triggering the behavior of the bug.  
3. Found the root cause
The root cause was found in service/ folder streak_service. First went to services and then to streak_service to see what was causing the streak to resent. 
4. The root cause 
The root cause was the user streak was not adding up to the music days listened to. 
5. Fix and side-effect check 
---

1. Issue number and title 
Bug Issue #5  with title "The last song in a playlist never shows up"
2. Reproduce the bug
Verified the bug existed with the mixtape database.  `today.weekday() != 6` was searched to see why the bug was resetting. This what was triggering the behavior of the bug.  
3. Found the root cause
The root cause was found in service/ folder streak_service. First went to services and then to streak_service to see what was causing the streak to resent. 
4. The root cause 
The root cause was the user streak was not adding up to the music days listened to. 
5. Fix and side-effect check 



## AI
<!-- Used copilot for codebase mapping suggestions -->
<!-- used Claude to fully understand milestone 2 - -->
