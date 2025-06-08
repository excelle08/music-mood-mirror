
import threading
import traceback
import time
import json
import pandas as pd
from flask import Blueprint, request, session, jsonify, current_app
from common.model import db, ListenHistory, RequestProgress
from datetime import datetime, timedelta
from collections import defaultdict
from common import llm 


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
        ListenHistory.music_completion_rate >= 50,
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


def get_avg_positivity_score(tags: list) -> float:
    """
    Calculate the average positivity score based on the provided tags.
    
    Args:
        tags (list): A list of tags representing emotions.
        
    Returns:
        float: The average positivity score.
    """
    positivity_dict = {
        'Joyful': 5, 'Melancholic': 2, 'Hopeful': 5, 'Angry': 1, 'Romantic': 4,
        'Nostalgic': 3, 'Sad': 1, 'Energetic': 4, 'Passionate': 4, 'Lonely': 1,
        'Uplifting': 5, 'Bittersweet': 3, 'Empowering': 5, 'Heartbroken': 1,
        'Reflective': 3, 'Playful': 4, 'Dark': 1, 'Calm': 4, 'Longing': 2, 'Triumphant': 5
    }
    scores = [positivity_dict.get(tag, 0) for tag in tags]
    valid_scores = [score for score in scores if score > 0]
    
    if valid_scores:
        return sum(valid_scores) / len(valid_scores)
    else:
        return 0.0


def from_lyrics_to_positivity(lyrics: str) -> [list[str], float]:
    """
    Analyze the lyrics and return the average positivity score.
    
    Args:
        lyrics (str): The lyrics to analyze.
        
    Returns:
        float: The average positivity score of the lyrics.
    """
    prompt = """
        You are an expert in analyzing song lyrics to determine the emotions they convey.
        Analyze the following song lyrics and return exactly 3 emotion tags that best summarize the emotions conveyed by the song. Only output the tags, in this format: #tag1 #tag2 #tag3.
        The tags must be adjectives and strictly chosen from the following list: Joyful, Melancholic, Hopeful, Angry, Romantic, Nostalgic, Sad, Energetic, Passionate, Lonely, Uplifting, Bittersweet, Empowering, Heartbroken, Reflective, Playful, Dark, Calm, Longing, Triumphant
    '''{lyrics}'''
    """
    # along with weights assigning to each each tag that summing up to 100%
    # input = pd.DataFrame({
    #     'query': [''],
    #     'prompt': [prompt.format(lyrics=lyrics)],
    #     'document': ['']
    # })
    # response = llm.loaded_model.predict(input)
    # mood = response['output'].strip().split('\n')
    response = llm.loaded_model(prompt.format(lyrics=lyrics), temperature=0.0, max_tokens=512, stop={"\n\n\n"})
    mood = response['choices'][0]['text'].strip().split('\n')
    tags_str = mood[0] if mood else ''
    tags = [tag.lstrip('#') for tag in tags_str.strip().split()]
    
    return tags, get_avg_positivity_score(tags)


@analyze_api.route('/api/analyze_emotion', methods=['POST'])
def analyze_emotion():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    if llm.loaded_model is None:
        return jsonify({'error': 'LLM model not loaded. Feature not available.'}), 503

    progress = RequestProgress(user_id=session['user_id'])
    db.session.add(progress)
    db.session.commit()

    thread = threading.Thread(
        target=_run_emotion_analysis,
        args=(current_app.app_context(), progress.id, session['user_id'])
    )
    thread.start()

    return jsonify({'request_id': progress.id})


def _run_emotion_analysis(app_context, request_id, user_id):
    app_context.push()

    try:
        entries = ListenHistory.query.filter(
            ListenHistory.user_id == user_id,
            bool(ListenHistory.first_occurrence_in_week) is True,
            ListenHistory.lyrics.isnot(None),
            ListenHistory.mood_tags_local.is_(None),
            ListenHistory.positivity_score_local.is_(None)
        ).all()

        total = len(entries)
        processed = 0
        success = 0

        progress = db.session.get(RequestProgress, request_id)
        progress.num_total = total
        db.session.commit()

        for i, entry in enumerate(entries):
            try:
                mood_tags, score = from_lyrics_to_positivity(entry.lyrics)
                entry.mood_tags_local = json.dumps(mood_tags)
                entry.positivity_score_local = score
                entry.positivity_score_local_wghted = score * (entry.repeats_this_week or 1)
                db.session.add(entry)
                success += 1
            except Exception as e:
                current_app.logger.error(f"Error processing entry {i}: {e}. \nDetailed traceback:")
                current_app.logger.error(traceback.format_exc())

            processed += 1
            if processed % 50 == 0 or i == total - 1:
                progress = db.session.get(RequestProgress, request_id)
                progress.num_processed = processed
                progress.num_successful = success
                db.session.commit()

    except Exception as e:
        current_app.logger.error(f"Error during emotion analysis: {e}. \nDetailed traceback:")
        current_app.logger.error(traceback.format_exc())
    finally:
        if progress:
            db.session.delete(progress)
            db.session.commit()