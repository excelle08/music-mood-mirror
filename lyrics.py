#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random
import json
from typing import Optional
from datetime import datetime

import requests
from config.settings import LRCLIB_SITE


class Song:
    """
    A class representing a song with its metadata and lyrics.
    """

    def __init__(self, title: str, artist: str,
                 album: Optional[str] = None, play_datetime: Optional[str] = None):
        self.title = title
        self.artist = artist
        self.album = album
        self.lyrics = None
        # If play_datetime is supplied, convert it to a datetime object
        # The datetime should be in ISO format
        if play_datetime is not None:
            try:
                self.play_datetime = datetime.fromisoformat(play_datetime)
            except ValueError:
                print(f"Invalid datetime format: {play_datetime}")
                self.play_datetime = None
        self.result_title = None
        self.result_artist = None
        self.result_album = None
        self.duration = None
        self.seconds_played = None
        self.music_completion_rate = None
        self.synced_lyrics = None

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
            "synced_lyrics": self.synced_lyrics
        }

    def search_lyrics(self) -> dict:
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
        req = requests.get(f"{LRCLIB_SITE}/api/search",
                           params=params, timeout=10)
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
        if self.seconds_played is not None:
            self.music_completion_rate = round(100 * self.seconds_played / self.duration, 2)
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
        obj = cls(title=title, artist=artist, album=album, play_datetime=song["ts"])
        # Extract "ms_played" and calculate the completion rate
        if "ms_played" in song:
            obj.seconds_played = song["ms_played"] / 1000
        return obj


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
