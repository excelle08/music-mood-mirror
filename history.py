#!/usr/bin/env python3
import numpy as np
import json
import datetime
import glob

from typing import Optional
from copy import deepcopy
from lyrics import Song


total_history = []
yearly_history = {}
all_years = set()


def load_history(dir_pattern: str):
    global total_history, yearly_history
    filepaths = glob.glob(dir_pattern)
    sorted_filepaths = sorted(filepaths)
    for filepath in sorted_filepaths:
        try:
            count = 0
            with open(filepath, 'r') as file:
                raw_history = json.load(file)
            for i, entry in enumerate(raw_history):
                song = Song.from_spotify(entry)
                res = song.search_lyrics()
                if res:
                    count += 1
                    total_history.append(song.to_dict())
                    year = song.play_datetime.year
                    if year not in yearly_history:
                        yearly_history[year] = []
                    yearly_history[year].append(song.to_dict())
                    if year not in all_years:
                        all_years.add(year)
                print(f"Processed entry {i+1}/{len(raw_history)} from {filepath}, {count} found lyrics", end='\r')
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {filepath}")
        finally:
            print(f"Finished processing file: {filepath}")


def iterate_history(years: Optional[list[int]] = None,
                    reasons: Optional[list[str]] = None,
                    min_completion_rate: float = 50,
                    min_seconds_played: int = 90,
                    yield_year: bool = False):
    if years is None:
        years = all_years
    for y in years:
        if y not in yearly_history:
            continue
        for entry in yearly_history[y]:
            if entry["music_completion_rate"] is None:
                continue
            if entry["music_completion_rate"] < min_completion_rate:
                continue
            if entry["seconds_played"] < min_seconds_played:
                continue
            if reasons is not None and entry["reason_start"] not in reasons:
                continue
            if yield_year:
                yield y, entry
            else:
                yield entry


def calculate_weekly_repeats(years: Optional[list[int]] = None,
                      reasons: Optional[list[str]] = None):
    filtered_history = [deepcopy(entry) for entry in iterate_history(years, reasons)]
    weekly_summary = {}
    new_history = {}

    for i in range(len(filtered_history)):
        song = filtered_history[i]
        play_dt = datetime.datetime.strptime(song["play_datetime"], "%Y-%m-%d %H:%M:%S")
        # Calculate the week key: {year}_{week_number}
        weeknum = play_dt.isocalendar().week
        week_key = f"{play_dt.year}_{weeknum}"
        if week_key not in weekly_summary:
            weekly_summary[week_key] = {}
      
        first_occurrence_in_week = False
        if song["title"] not in weekly_summary[week_key]:
            first_occurrence_in_week = True
            weekly_summary[week_key][song["title"]] = {
                "album": song["album"],
                "artist": song["artist"],
                "duration": song["duration"],
                "lyrics": song["lyrics"],
                "music_completion_rates": [song["music_completion_rate"]],
                "reasons_start": [song["reason_start"]],
                "reasons_end": [song["reason_end"]],
                "repeats_this_week": 1,
                "seconds_played": [song["seconds_played"]],
                "times_in_shuffle": 1 if song["shuffle"] else 0,
                "times_skipped": 1 if song["skipped"] else 0,
                "timestamps_played": [song["play_datetime"]],
                "idx_first_encounter": i,
            }
        else:
            weekly_summary[week_key][song["title"]]["music_completion_rates"].append(song["music_completion_rate"])
            weekly_summary[week_key][song["title"]]["reasons_start"].append(song["reason_start"])
            weekly_summary[week_key][song["title"]]["reasons_end"].append(song["reason_end"])
            weekly_summary[week_key][song["title"]]["repeats_this_week"] += 1
            weekly_summary[week_key][song["title"]]["seconds_played"].append(song["seconds_played"])
            if song["shuffle"]:
                weekly_summary[week_key][song["title"]]["times_in_shuffle"] += 1
            if song["skipped"]:
                weekly_summary[week_key][song["title"]]["times_skipped"] += 1
            weekly_summary[week_key][song["title"]]["timestamps_played"].append(song["play_datetime"])
        # Count repeats in the next 7 days
        j = i + 1
        repeats = 0
        while j < len(filtered_history):
            curr_play_dt = datetime.datetime.strptime(filtered_history[j]["play_datetime"], "%Y-%m-%d %H:%M:%S")
            timediff = curr_play_dt - play_dt
            if timediff.days > 7:
                break
            # Compare "title" of filtered_history[i] and filtered_history[j]
            if filtered_history[i]["title"] == filtered_history[j]["title"]:
                repeats += 1
            j += 1

        song["repeats_next_7d"] = repeats
        song["first_occurrence_in_week"] = first_occurrence_in_week
        song["week"] = weeknum
        song["repeats_this_week"] = None
    
    for week_key, songs in weekly_summary.items():
        for title, song_data in songs.items():
            i = song_data["idx_first_encounter"]
            filtered_history[i]["repeats_this_week"] = song_data["repeats_this_week"]

    return filtered_history, weekly_summary


def main():
    # Example usage
    load_history("/home/wsu/my_spotify_data/Spotify Extended Streaming History/Streaming_History_Audio_*.json")
    for year in all_years:
        processed_history, weekly_summary = calculate_weekly_repeats(years=[year])
        print(f"Processed history for {year}: {len(processed_history)} entries")
        with open(f"data/yearly/weekly_summary/{year}.json", 'w') as file:
            json.dump(weekly_summary, file, indent=2, sort_keys=False, ensure_ascii=False)
        with open(f"data/yearly/processed_history/{year}.json", 'w') as file:
            json.dump(processed_history, file, indent=2, sort_keys=False, ensure_ascii=False)
    

if __name__ == "__main__":
    main()
