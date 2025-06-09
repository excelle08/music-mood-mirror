
import threading
import time
from flask import Blueprint, request, session, jsonify, current_app
from common.model import db, ListenHistory, RequestProgress
from lyrics import Song

enrich_api = Blueprint('enrich_api', __name__)

@enrich_api.route('/api/enrich_lyrics', methods=['POST'])
def enrich_lyrics():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    user_id = session['user_id']

    # Create request progress record
    progress = RequestProgress(user_id=user_id, num_total=0, num_processed=0, num_successful=0)
    db.session.add(progress)
    db.session.commit()

    # Launch background worker
    thread = threading.Thread(target=_run_enrichment,
                              args=(current_app.app_context(), progress.id, user_id),
                              daemon=True)
    thread.start()

    return jsonify({'request_id': progress.id})


@enrich_api.route('/api/request_progress', methods=['GET'])
def request_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    request_id = request.args.get('request_id', type=int)
    if not request_id:
        return jsonify({'error': 'missing request_id'}), 400

    record = RequestProgress.query.filter_by(id=request_id, user_id=session['user_id']).first()
    if not record:
        return jsonify({'error': 'not found'}), 404

    return jsonify({
        'num_total': record.num_total,
        'num_processed': record.num_processed,
        'num_successful': record.num_successful
    })


def _run_enrichment(app_context, request_id, user_id):
    app_context.push()
    with db.session.begin():
        entries = ListenHistory.query.filter_by(user_id=user_id, lyrics=None).all()
        progress = db.session.get(RequestProgress, request_id)
        progress.num_total = len(entries)

    num_processed = 0
    num_successful = 0

    prev_time = time.time()
    for i, entry in enumerate(entries):
        try:
            s = Song(title=entry.title, artist=entry.artist, album=entry.album)
            result = s.search_lyrics()

            if result and s.lyrics:
                entry.lyrics = s.lyrics
                entry.synced_lyrics = s.synced_lyrics
                entry.result_title = s.result_title
                entry.result_artist = s.result_artist
                entry.result_album = s.result_album
                entry.duration = s.duration
                if s.duration and entry.seconds_played:
                    entry.music_completion_rate = s.music_completion_rate
                num_successful += 1
            if i % 100 == 0 or i == len(entries) - 1:
                db.session.commit()
        except Exception as e:
            print(f"Enrichment error: {e}")
            db.session.rollback()

        num_processed += 1

        curr_time = time.time()
        if curr_time - prev_time > 1:
            prev_time = curr_time
            progress = db.session.get(RequestProgress, request_id)
            progress.num_total = len(entries)
            progress.num_processed = num_processed
            progress.num_successful = num_successful

    # Remove progress record after completion
    progress = db.session.get(RequestProgress, request_id)
    db.session.delete(progress)
    db.session.commit()
