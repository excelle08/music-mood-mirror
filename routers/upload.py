
import os
import json
import time
import tempfile
import threading
from flask import Blueprint, request, session, jsonify, current_app
from werkzeug.utils import secure_filename
from common.model import db, ListenHistory, RequestProgress
from lyrics import Song

upload_api = Blueprint('upload_api', __name__)

@upload_api.route('/api/upload_history', methods=['POST'])
def upload_history_async():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    file = request.files.get('history_file')
    if not file:
        return jsonify({'error': 'no file'}), 400

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    file.save(temp.name)

    progress = RequestProgress(user_id=session['user_id'])
    db.session.add(progress)
    db.session.commit()

    thread = threading.Thread(
        target=_run_history_upload,
        args=(current_app.app_context(), temp.name, progress.id, session['user_id'])
    )
    thread.start()

    return jsonify({'request_id': progress.id})


def _run_history_upload(app_context, filepath, request_id, user_id):
    app_context.push()

    current_app.logger.info(f"Processing history file: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            history_data = json.load(f)
        except Exception as e:
            current_app.logger.error("Failed to parse JSON:", e)
            return

    os.remove(filepath)

    num_total = len(history_data)
    num_added = 0
    prev_time = time.time()

    current_app.logger.info(f"Total entries to process: {num_total}")

    for i, entry in enumerate(history_data):

        if i % 100 == 0 or i == num_total - 1:
            db.session.commit()

        if time.time() - prev_time >= 1:
            progress = db.session.get(RequestProgress, request_id)
            progress.num_total = num_total
            progress.num_processed = i + 1 
            progress.num_successful = num_added
            current_app.logger.info(
                f"Progress: {i + 1}/{num_total} processed, {num_added} added"
            )
            prev_time = time.time()

        s = Song.from_spotify(entry)
        if not s:
            current_app.logger.warning(f"Failed to parse the entry {i}")
            continue

        if not s.title or not s.artist or not s.play_datetime:
            current_app.logger.warning(f"Skipping entry {i} due to missing required fields")
            continue

        exists = ListenHistory.query.filter_by(
            user_id=user_id,
            title=s.title,
            artist=s.artist,
            play_datetime=s.play_datetime
        ).first()
        if exists:
            continue

        row = ListenHistory(
            user_id=user_id,
            title=s.title,
            artist=s.artist,
            album=s.album,
            play_datetime=s.play_datetime,
            reason_start=s.reason_start,
            reason_end=s.reason_end,
            shuffle=s.shuffle,
            skipped=s.skipped,
            seconds_played=s.seconds_played,
        )
        db.session.add(row)
        num_added += 1


    current_app.logger.info(f"Finished processing {num_total} entries, {num_added} added.")
    progress = db.session.get(RequestProgress, request_id)
    db.session.delete(progress)
    db.session.commit()
