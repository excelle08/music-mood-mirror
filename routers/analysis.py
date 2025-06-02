
from flask import Blueprint, render_template, jsonify, session
from common.model import db, ListenHistory
from collections import defaultdict
from datetime import datetime, timedelta

analysis = Blueprint('analysis', __name__)

@analysis.route('/analysis')
def analysis_page():
    if 'user_id' not in session:
        return "Unauthorized", 401
    return render_template("analysis.html")

@analysis.route('/api/top_repeats_weekly')
def top_repeats_weekly():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    entries = ListenHistory.query.filter(
        ListenHistory.user_id == session['user_id'],
        ListenHistory.week.isnot(None)
    ).all()

    week_map = defaultdict(lambda: defaultdict(list))
    for entry in entries:
        date = entry.play_datetime.date()
        iso_year, iso_week, _ = date.isocalendar()
        key = (entry.title, entry.artist)
        week_map[(iso_year, iso_week)][key].append(entry)

    result = []
    for (year, week), song_groups in sorted(week_map.items()):
        top_songs = sorted(song_groups.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        start_date = datetime.strptime(f"{year}-W{week}-1", "%G-W%V-%u").date()
        end_date = start_date + timedelta(days=6)
        label = f"{year}-W{week}"

        for rank, (song_key, plays) in enumerate(top_songs, start=1):
            avg_completion = sum(e.music_completion_rate for e in plays if e.music_completion_rate) / len(plays)
            result.append({
                "label": label,
                "rank": rank,
                "week_start": start_date.isoformat(),
                "week_end": end_date.isoformat(),
                "repeat_count": len(plays),
                "title": song_key[0],
                "artist": song_key[1],
                "avg_completion": round(avg_completion * 100, 1)
            })

    return jsonify(result)
