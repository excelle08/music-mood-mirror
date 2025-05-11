#!/usr/bin/env python3

import requests
import sys
import random
import json
from typing import Optional
from datetime import datetime


class Song:
    """
    A class representing a song with its metadata and lyrics.
    """
    def __init__(self, title: str, artist: str, album: Optional[str] = None, play_datetime: Optional[str] = None):
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
        req = requests.get("https://lrclib.net/api/search", params=params, timeout=10)
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
            name = name[:len(name)-8].strip()
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
        return cls(title=title, artist=artist, album=album, play_datetime=song["ts"])


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


def sample(song_list: list[dict], num_samples: int = 20, outfile: str = "samples.json", verbose: bool = False):
    res = []
    N = len(song_list)
    while len(res) < num_samples:
        i = random.randint(0, N)
        print(i)
        song = search(song_list[i])
        if song is not None and song.lyrics is not None:
            if verbose:
                print("="*80)
                print("Title: " + song.result_title)
                print("Artist Name: " + song.result_artist)
                print("Album Name: " + song.result_album)
                print(f"Duration: {song.duration}s")
                print("Lyrics: ")
                print(song.lyrics)

            #lyrics["lyrics"] = lyrics["lyrics"].encode("raw_unicode_escape").decode("utf-8")
            res.append(song.to_dict())

    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    return len(res)


def demo():
    if len(sys.argv) < 2:
        print("Please specify a music history json file.")
        exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        history = json.load(f)

    N = len(history)
    song = history[random.randint(0, N)]

    lyrics = search(song)

    print(f"Search criteria: {lyrics['search_title']}, {lyrics['search_artist']}")

    if lyrics["found"]:
        print("="*80)
        print("Title: " + lyrics["result_title"])
        print("Artist Name: " + lyrics["result_artist"])
        print("Album Name: " + lyrics["result_album"])
        print(f"Duration: {lyrics['duration']}s")
        print("Lyrics: ")
        print(lyrics["lyrics"])


def demo2():
    if len(sys.argv) < 2:
        print("Please specify a music history json file.")
        exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        history = json.load(f)

    sample(history, verbose=True)


if __name__ == "__main__":
    demo2()
