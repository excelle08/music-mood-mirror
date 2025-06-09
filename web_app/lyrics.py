#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random
import json
import sys
import time
from typing import Optional
from datetime import datetime

import requests
from config.settings import LRCLIB_SITE


class Song:
    """
    A class representing a song with its metadata and lyrics.
    """

    def __init__(self, title: str, artist: str,
                 album: Optional[str] = None, play_datetime: Optional[str] = None,
                 reason_start: Optional[str] = None, reason_end: Optional[str] = None,
                 shuffle: Optional[bool] = None, skipped: Optional[bool] = None):
        self.title: str = title
        self.artist: str = artist
        self.album: Optional[str] = album
        self.lyrics: Optional[str] = None
        # If play_datetime is supplied, convert it to a datetime object
        # The datetime should be in ISO format
        if play_datetime is not None:
            try:
                self.play_datetime = datetime.fromisoformat(play_datetime)
            except ValueError:
                print(f"Invalid datetime format: {play_datetime}")
                self.play_datetime = None
        self.result_title: Optional[str] = None
        self.result_artist: Optional[str] = None
        self.result_album: Optional[str] = None
        self.duration: Optional[str] = None
        self.seconds_played: Optional[str] = None
        self.music_completion_rate: Optional[str] = None
        self.synced_lyrics: Optional[str] = None
        self.reason_start: Optional[str] = reason_start
        self.reason_end: Optional[str] = reason_end
        self.shuffle: Optional[str] = shuffle
        self.skipped: Optional[str] = skipped
        self.mood_tags: Optional[list[str]] = None
        self.positivity_score: Optional[float] = None
        self.mood_tags_local: Optional[list[str]] = None
        self.positivity_score_local: Optional[float] = None
        self.positivity_score_local_wghted: Optional[float] = None
        self.repeats_this_week: Optional[int] = None
        self.week: Optional[int] = None
        self.first_occurrence_in_week: Optional[bool] = None
        self.repeats_next_7d: Optional[int] = None


    def __str__(self):
        return f"Title: {self.title}, Artist: {self.artist}, Album: {self.album}"

    def __repr__(self):
        return f"Song(title={self.title}, artist={self.artist}, album={self.album})"

    def to_dict(self):
        """
        Convert the Song object to a dictionary.
        :return: A dictionary representation of the Song object.
        """
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "play_datetime": self.play_datetime.strftime('%Y-%m-%d %H:%M:%S') if self.play_datetime else None,
            "result_title": self.result_title,
            "result_artist": self.result_artist,
            "result_album": self.result_album,
            "duration": self.duration,
            "seconds_played": self.seconds_played,
            "music_completion_rate": self.music_completion_rate,
            "lyrics": self.lyrics,
            "synced_lyrics": self.synced_lyrics,
            "reason_start": self.reason_start,
            "reason_end": self.reason_end,
            "shuffle": self.shuffle,
            "skipped": self.skipped,
            "mood_tags": self.mood_tags,
            "positivity_score": self.positivity_score,
            "mood_tags_local": self.mood_tags_local,
            "positivity_score_local": self.positivity_score_local,
            "positivity_score_local_wghted": self.positivity_score_local_wghted,
            "repeats_this_week": self.repeats_this_week,
            "week": self.week,
            "first_occurrence_in_week": self.first_occurrence_in_week,
            "repeats_next_7d": self.repeats_next_7d,
        }

    def search_lyrics(self, retry_count: int = 3) -> dict:
        """
        Search for lyrics using the lrclib API.
        :param title: The title of the song.
        :param artist: The artist of the song.
        :return: A list of lyrics dictionaries.
        """
        params = {
            "q": "",
            "track_name": self.title,
            "artist_name": self.artist,
        }
        if self.album is not None:
            params["album_name"] = self.album
        for i in range(retry_count):
            try:
                req = requests.get(f"{LRCLIB_SITE}/api/search",
                                   params=params, timeout=10)
                break
            except requests.exceptions.ConnectionError as e:
                print(("Connection error while searching for the song "
                       f"\"{self.artist} - {self.title}\": {e}. "
                       f"Retrying ({i + 1}/{retry_count})..."),
                     file=sys.stderr)
                time.sleep(i + 1)
                if i == retry_count - 1:
                    print("Failed to connect after multiple attempts.", file=sys.stderr)
                    return {}

        search_results = json.loads(req.text)
        if len(search_results) == 0:
            return {}
        res = search_results[0]
        self.result_title = res["trackName"]
        self.result_artist = res["artistName"]
        self.result_album = res["albumName"]
        self.duration = res["duration"]
        self.lyrics = res["plainLyrics"]
        self.synced_lyrics = res["syncedLyrics"]
        if self.seconds_played is not None and self.duration > 0:
            self.music_completion_rate = round(100 * self.seconds_played / self.duration, 2)
        else:
            self.music_completion_rate = 0
        return res

    @classmethod
    def from_youtube(cls, song: dict):
        """
        Create a Song object from a YouTube music listening history entry.
        :param song: A dictionary representing a YouTube music history entry.
        :return: A Song object if creation is successful, or None.
        """
        # Check validity: "header" is "Youtube Music"
        if "header" not in song or song["header"] != "YouTube Music":
            return None
        # Extract title
        title = song["title"]
        if "Watched" in title:
            title = title[8:]
        # Extract artist: the field "subtitles" should exist, is a list of dicts,
        # has at least one entry, the first entry has a field "name" which is the artist name.
        # It should end with "Topic" and we should remove it.
        if "subtitles" not in song or len(song["subtitles"]) < 1:
            return None
        subtitles = song["subtitles"]
        if len(subtitles) < 1:
            return None
        name = subtitles[0]["name"]
        if name.endswith("Topic"):
            name = name[:len(name) - 8].strip()
        else:
            return None
        # Create the Song object
        return cls(title=title, artist=name, play_datetime=song["time"])

    @classmethod
    def from_spotify(cls, song: dict):
        """
        Create a Song object from a Spotify music listening history entry.
        :param song: A dictionary representing a Spotify music history entry.
        :return: A Song object if creation is successful, or None.
        """
        # Check validity: the field "spotify_track_uri" should exist
        if "spotify_track_uri" not in song:
            return None
        # Extract title, artist and album
        title = song["master_metadata_track_name"]
        artist = song["master_metadata_album_artist_name"]
        album = song["master_metadata_album_album_name"]
        # Create the Song object
        obj = cls(title=title, artist=artist, album=album, play_datetime=song["ts"],
                  reason_start=song.get("reason_start"),
                  reason_end=song.get("reason_end"), shuffle=song.get("shuffle"),
                  skipped=song.get("skipped"))
        # Extract "ms_played" and calculate the completion rate
        if "ms_played" in song:
            obj.seconds_played = song["ms_played"] / 1000
        return obj

    @classmethod
    def from_dict(cls, song_dict: dict):
        """
        Create a Song object from a dictionary.
        :param song_dict: A dictionary representing a song.
        :return: A Song object if creation is successful, or None.
        """
        try:
            s = cls(
                title=song_dict["title"],
                artist=song_dict["artist"],
                album=song_dict.get("album"),
                play_datetime=song_dict.get("play_datetime"),
                reason_start=song_dict.get("reason_start"),
                reason_end=song_dict.get("reason_end"),
                shuffle=song_dict.get("shuffle"),
                skipped=song_dict.get("skipped")
            )
            s.result_title = song_dict.get("result_title")
            s.result_artist = song_dict.get("result_artist")
            s.result_album = song_dict.get("result_album")
            s.duration = song_dict.get("duration")
            s.seconds_played = song_dict.get("seconds_played")
            s.music_completion_rate = song_dict.get("music_completion_rate")
            s.lyrics = song_dict.get("lyrics")
            s.synced_lyrics = song_dict.get("synced_lyrics")
            s.mood_tags = song_dict.get("mood_tags")
            s.positivity_score = song_dict.get("positivity_score")
            s.mood_tags_local = song_dict.get("mood_tags_local")
            s.positivity_score_local = song_dict.get("positivity_score_local")
            s.positivity_score_local_wghted = song_dict.get("positivity_score_local_wghted")
            s.repeats_this_week = song_dict.get("repeats_this_week")
            s.week = song_dict.get("week")
            s.first_occurrence_in_week = song_dict.get("first_occurrence_in_week")
            s.repeats_next_7d = song_dict.get("repeats_next_7d")
            return s
        except KeyError as e:
            print(f"Missing key in song dictionary: {e}", file=sys.stderr)
            return None


def search(song: dict) -> Song:
    """
    Search for lyrics using the lrclib API.
    :param song: A dictionary representing a youtube or spotify listening history entry.
    :return: A Song object if creation is successful, or None.
    """
    if "header" in song and song["header"] == "YouTube Music":
        s = Song.from_youtube(song)
    elif "spotify_track_uri" in song:
        s = Song.from_spotify(song)
    else:
        s = None

    if s is not None:
        s.search_lyrics()

    return s


def sample(song_list: list[dict], num_samples: int = 20,
           outfile: str = "samples.json", verbose: bool = False):
    """
    Sample a number of songs from the song list and save their lyrics to a file.
    :param song_list: A list of dictionaries representing songs.
    :param num_samples: The number of samples to take.
    :param outfile: The output file to save the lyrics.
    :param verbose: If True, print the lyrics to the console.
    :return: The number of successful samples.
    """
    res = []
    N = len(song_list)
    while len(res) < num_samples:
        i = random.randint(0, N)
        print(i)
        song = search(song_list[i])
        if song is not None and song.lyrics is not None:
            if verbose:
                print("=" * 80)
                print("Title: " + song.result_title)
                print("Artist Name: " + song.result_artist)
                print("Album Name: " + song.result_album)
                print(f"Duration: {song.duration}s")
                print("Lyrics: ")
                print(song.lyrics)

            # lyrics["lyrics"] = lyrics["lyrics"].encode("raw_unicode_escape").decode("utf-8")
            res.append(song.to_dict())

    sorted_res = sorted(res, key=lambda x: x["play_datetime"])
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(sorted_res, f, indent=2, ensure_ascii=False)
    return len(res)


def iterate_all(song_list: list[dict], outfile: str = "all_history.json"):
    """
    Iterate through all songs in the song list and save their lyrics to a file.
    :param song_list: A list of dictionaries representing songs.
    :param outfile: The output file to save the lyrics.
    :return: None
    """
    num_songs = len(song_list)
    num_successful = 0
    num_invalid = 0
    num_no_result = 0
    res = []

    for i, history_entry in enumerate(song_list):
        print(
            (f"Processing {i} / {num_songs}, ",
             f"successful: {num_successful}, ",
             f"invalid: {num_invalid}, ",
             f"no result: {num_no_result}"
            ),
            end="\r"
        )
        song = search(history_entry)
        if song is None:
            num_invalid += 1
            continue
        song.search_lyrics()
        if song.lyrics is None:
            num_no_result += 1
            continue

        res.append(song.to_dict())
        num_successful += 1

    print(f"Total songs: {num_songs}")
    print(f"Successfully found lyrics: {num_successful} ({100 * num_successful / num_songs:.2f}%)")
    print(f"Invalid data points: {num_invalid} ({100 * num_invalid / num_songs:.2f}%)")
    print(f"No results: {num_no_result} ({100 * num_no_result / num_songs:.2f}%)")

    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


def demo(input_file: str = "music_history.json", outfile: str = "one_sample.json"):
    """
    A demo function to test the sample functionality.
    :param input_file: The input file containing music history.
    :return: None
    """
    with open(input_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    sample(history, 1, outfile, verbose=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lyrics search and sampling tool.")
    parser.add_argument("action", choices=["demo", "sample", "iterate_all"],
                        help=("Action to perform: 'demo' for a single random search, ",
                              "'sample' for sampling N songs,",
                              "'iterate_all' for processing all songs.")
    )
    parser.add_argument("--input-file", "-i", type=str, default="music_history.json",
                        help="Input file containing music history (default: music_history.json).")
    parser.add_argument("--num-samples", "-n", type=int, default=20,
                        help="Number of samples to take (only for 'sample' action).")
    parser.add_argument("--outfile", "-o", type=str, default="samples.json",
                        help="Output file for the results (default: samples.json).")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="If set, print the song information and lyrics to the console.")
    args = parser.parse_args()

    if args.action == "demo":
        demo(args.input_file, args.outfile)
    elif args.action == "sample":
        with open(args.input_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        sample(history, num_samples=args.num_samples, outfile=args.outfile, verbose=args.verbose)
    elif args.action == "iterate_all":
        with open(args.input_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        iterate_all(history, outfile=args.outfile)
