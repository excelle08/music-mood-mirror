
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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

            for entry in history_data:
                s = Song.from_spotify(entry)
                if not s:
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
            flash(f"{added} entries added to your listening history.")
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
    pagination = ListenHistory.query.filter_by(user_id=session['user_id']) \
        .order_by(ListenHistory.play_datetime.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'view_history.html',
        history=pagination.items,
        pagination=pagination,
        page=page,
        per_page=per_page
    )
