
import threading
import time
from flask import Blueprint, request, session, jsonify, current_app
from common.model import db, ListenHistory, RequestProgress
from datetime import datetime, timedelta
from collections import defaultdict

analyze_api = Blueprint('analyze_api', __name__)

@analyze_api.route('/api/analyze_history', methods=['POST'])
def analyze_history():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    progress = RequestProgress(user_id=session['user_id'])
    db.session.add(progress)
    db.session.commit()

    thread = threading.Thread(
        target=_run_analysis,
        args=(current_app.app_context(), progress.id, session['user_id'])
    )
    thread.start()

    return jsonify({'request_id': progress.id})


def _run_analysis(app_context, request_id, user_id):
    app_context.push()

    entries = ListenHistory.query.filter(
        ListenHistory.user_id == user_id,
        ListenHistory.music_completion_rate >= 0.5,
        ListenHistory.seconds_played >= 90,
        ListenHistory.play_datetime.isnot(None)
    ).order_by(ListenHistory.play_datetime.asc()).all()

    current_app.logger.info(f"Found {len(entries)} entries for analysis.")
    num_entries = len(entries)
    total = len(entries) * 3
    processed = 0

    progress = db.session.get(RequestProgress, request_id)
    progress.num_total = total
    db.session.commit()

    prev_time = time.time()
    week_map = defaultdict(list)
    for i, entry in enumerate(entries):
        date = entry.play_datetime.date()
        iso_year, iso_week, _ = date.isocalendar()
        key = (entry.artist, entry.title)
        entry.week = iso_week
        week_map[(key, iso_year, iso_week)].append(entry)
        processed += 1

        if time.time() - prev_time > 1 or i == num_entries - 1:
            current_app.logger.info(f"Processed {i + 1} / {num_entries} entries for week map...")
            progress.num_processed = processed
            db.session.commit()
            prev_time = time.time()

    by_song = defaultdict(list)
    for entry in entries:
        key = (entry.artist, entry.title)
        by_song[key].append(entry)

    for k, song_list in enumerate(by_song.values()):
        for i, current in enumerate(song_list):
            count = 0
            end_time = current.play_datetime + timedelta(days=7)
            for later in song_list[i+1:]:
                if later.play_datetime > end_time:
                    break
                count += 1
            current.repeats_next_7d = count
            processed += 1
        
        if time.time() - prev_time > 1 or k == len(by_song) - 1:
            current_app.logger.info(f"Processed {k + 1} / {len(by_song)} songs for next 7 days repeats...")
            progress.num_processed = processed
            db.session.commit()
            prev_time = time.time()

    for i, ((key, year, week), week_entries) in enumerate(week_map.items()):
        seen = set()
        for entry in week_entries:
            entry.repeats_this_week = len(week_entries)
            song_id = (entry.artist, entry.title)
            if song_id not in seen:
                entry.first_occurrence_in_week = True
                seen.add(song_id)
            else:
                entry.first_occurrence_in_week = False

            processed += len(week_entries)
        
        if time.time() - prev_time > 1 or i == len(week_map) - 1:
            current_app.logger.info(f"Processed {i + 1} / {len(week_map)} weeks for first occurrence...")
            progress.num_processed = processed
            db.session.commit()
            prev_time = time.time()

    current_app.logger.info("Analysis completed, committing changes to the database.")
    db.session.delete(progress)
    db.session.commit()
