
from flask import Blueprint, render_template, jsonify, session, current_app, request
from common.model import db, ListenHistory
from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy import extract
import json

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
                "avg_completion": round(avg_completion, 1)
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
        rate = min(e.music_completion_rate, 100)
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
        ListenHistory.week.isnot(None),
        ListenHistory.positivity_score_local_wghted.isnot(None),
        ListenHistory.repeats_this_week.isnot(None)
    ).all()

    week_map = defaultdict(list)
    for e in entries:
        y, w, _ = e.play_datetime.date().isocalendar()
        week_map[(y, w)].append(e)

    week_data = []
    for (year, week), songs in sorted(week_map.items()):
        total_weight = sum(e.repeats_this_week for e in songs)
        if total_weight == 0:
            continue
        weighted_sum = sum(e.positivity_score_local_wghted for e in songs)
        avg_score = round(weighted_sum / total_weight, 2)
        label = f"{year}-W{week}"
        week_data.append({"label": label, "score": avg_score})

    return jsonify(week_data)


@analysis.route('/api/weekly_tags')
def get_weekly_tags():
    year = int(request.args.get('year'))
    week = int(request.args.get('week'))

    positivity_dict = {
        'Joyful': 5, 'Melancholic': 2, 'Hopeful': 5, 'Angry': 1, 'Romantic': 4,
        'Nostalgic': 3, 'Sad': 1, 'Energetic': 4, 'Passionate': 4, 'Lonely': 1,
        'Uplifting': 5, 'Bittersweet': 3, 'Empowering': 5, 'Heartbroken': 1,
        'Reflective': 3, 'Playful': 4, 'Dark': 1, 'Calm': 4, 'Longing': 2, 'Triumphant': 5
    }

    entries = ListenHistory.query.filter(
        ListenHistory.user_id == session['user_id'],
        ListenHistory.first_occurrence_in_week == True,
        #extract('year', ListenHistory.play_datetime) == year,
        ListenHistory.week == week
    ).all()

    current_app.logger.info(f"Fetching tags for week {week} of {year}, found {len(entries)} entries.")

    tag_weights = defaultdict(float)
    for entry in entries:
        try:
            tags = json.loads(entry.mood_tags_local or '[]')
            tags = [tag for tag in tags if tag in positivity_dict.keys()]
        except Exception as e:
            current_app.logger.error(f"Failed to parse mood_tags for entry {entry.id}, skipping: {e}")
            continue
        for tag in tags:
            tag_weights[tag] += entry.repeats_this_week or 1

    sorted_tags = sorted(tag_weights.items(), key=lambda x: x[1], reverse=True)[:20]

    return jsonify(sorted_tags)
        