
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from markupsafe import Markup
from common.model import db, ListenHistory
from lyrics import Song

history = Blueprint('history', __name__)

@history.route('/upload_history', methods=['GET', 'POST'])
def upload_history():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        file = request.files.get('history_file')
        if not file:
            flash('No file uploaded.')
            return redirect(url_for('history.upload_history'))

        try:
            history_data = json.load(file)
            added = 0
            ignored = 0
            failed = 0

            for entry in history_data:
                s = Song.from_spotify(entry)
                if not s:
                    failed += 1
                    continue
                # Skip duplicates
                existing = ListenHistory.query.filter_by(
                    user_id=session['user_id'],
                    title=s.title,
                    artist=s.artist,
                    play_datetime=s.play_datetime
                ).first()
                if existing:
                    ignored += 1
                    continue

                row = ListenHistory(
                    user_id=session['user_id'],
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
                added += 1

            db.session.commit()
            end_message = (f"{added} new entries added, {ignored} ignored, {failed} failed to process. "
                           "<a href='/view_history' class='alert-link'>View History</a>")
            flash(Markup(end_message))
        except Exception as e:
            flash(f"Failed to process file: {str(e)}")

        return redirect(url_for('history.upload_history'))

    return render_template('upload_history.html')


@history.route('/view_history')
def view_history():
    if 'user_id' not in session:
        flash('Please log in to view your history.')
        return redirect(url_for('auth.login'))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    only_lyrics = request.args.get('only_lyrics', '0') == '1'
    min_seconds = request.args.get('min_seconds', 90, type=int)
    min_completion = request.args.get('min_completion', 50, type=int) / 100.0

    query = ListenHistory.query.filter_by(user_id=session['user_id'])

    if only_lyrics:
        query = query.filter(ListenHistory.lyrics.isnot(None))
    query = query.filter(ListenHistory.seconds_played >= min_seconds)
    query = query.filter(ListenHistory.music_completion_rate >= min_completion)

    pagination = query.order_by(ListenHistory.play_datetime.desc())\
                      .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'view_history.html',
        history=pagination.items,
        pagination=pagination,
        page=page,
        per_page=per_page,
        only_lyrics=only_lyrics,
        min_seconds=min_seconds,
        min_completion=int(min_completion * 100)
    )