#!/usr/bin/env python3

import requests
import sys
import random
import json
from typing import Optional


def search(title: str, artist: str) -> list:
    params = {
        "q": "",
        "track_name": title,
        "artist_name": artist,
    }
    req = requests.get("https://lrclib.net/api/search", params=params)
    return json.loads(req.text)


def extract_title(song: dict):
    # Strip "Watched" prefix
    orig_title = song["title"]
    if orig_title.startswith("Watched"):
        title = orig_title[8:]
    else:
        title = orig_title

    return title.strip()


def extract_artist(song: dict):
    if "subtitles" not in song:
        return ""
    subtitles = song["subtitles"]
    if len(subtitles) < 1:
        return ""
    name = subtitles[0]["name"]
    if name.endswith("Topic"):
        return name[:len(name)-8].strip()
    return name


def demo():
    if len(sys.argv) < 2:
        print("Please specify a music history json file.")
        exit(1)

    with open(sys.argv[1], "r") as f:
        history = json.load(f)

    N = len(history)
    song = history[random.randint(0, N)]

    title = extract_title(song)
    artist = extract_artist(song)

    print("Title: " + title)
    print("Artist: " + artist)

    lyrics_list = search(title, artist)

    for lyrics in lyrics_list:
        print("="*80)
        print("Track Name: " + lyrics["trackName"])
        print("Artist Name: " + lyrics["artistName"])
        print("Album Name: " + lyrics["albumName"])
        print(f"Duration: {lyrics['duration']}s")
        print("Lyrics: ")
        print(lyrics["plainLyrics"])



if __name__ == "__main__":
    demo()
