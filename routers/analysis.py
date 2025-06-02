
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


@analysis.route('/api/histograms')
def histograms():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    entries = ListenHistory.query.filter(
        ListenHistory.user_id == session['user_id'],
        ListenHistory.music_completion_rate.isnot(None),
        ListenHistory.seconds_played.isnot(None)
    ).all()

    # Completion rate buckets: 0-10%, 10-20%, ..., 90-100%
    completion_buckets = [0] * 11  # 10 buckets + >100% in 100%
    for e in entries:
        rate = min(e.music_completion_rate * 100, 100)
        idx = min(int(rate // 10), 10)
        completion_buckets[idx] += 1

    # Seconds played buckets: 0–30, ..., 330–360 (12 buckets)
    seconds_buckets = [0] * 13
    for e in entries:
        sec = min(e.seconds_played, 360)
        idx = min(int(sec // 30), 12)
        seconds_buckets[idx] += 1

    return jsonify({
        "completion_rate": completion_buckets,
        "seconds_played": seconds_buckets
    })


import random

@analysis.route('/analysis/mood')
def mood_page():
    if 'user_id' not in session:
        return "Unauthorized", 401
    return render_template("mood.html")

@analysis.route('/api/mood')
def mood_api():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    entries = ListenHistory.query.filter(
        ListenHistory.user_id == session['user_id'],
        ListenHistory.play_datetime.isnot(None)
    ).order_by(ListenHistory.play_datetime.asc()).all()

    if not entries:
        return jsonify([])

    # Get first and last week
    first_date = entries[0].play_datetime.date()
    last_date = entries[-1].play_datetime.date()
    start_year, start_week, _ = first_date.isocalendar()
    end_year, end_week, _ = last_date.isocalendar()

    # Create weekly range
    week_data = []
    current = datetime.strptime(f"{start_year}-W{start_week}-1", "%G-W%V-%u").date()
    end = datetime.strptime(f"{end_year}-W{end_week}-1", "%G-W%V-%u").date()

    while current <= end:
        year, week, _ = current.isocalendar()
        score = round(random.uniform(1, 5), 2)
        week_data.append({
            "label": f"{year}-W{week}",
            "score": score
        })
        current += timedelta(days=7)

    return jsonify(week_data)
