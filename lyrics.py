#!/usr/bin/env python3

import requests
import sys
import random
import json
from typing import Optional


def search_from_lrclib(title: str, artist: str) -> list:
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


def search(song: dict):
    search_title = extract_title(song)
    search_artist = extract_artist(song)
    res = {
        "search_title": search_title,
        "search_artist": search_artist,
        "found": False
    }

    lyrics_list = search_from_lrclib(search_title, search_artist)
    if len(lyrics_list) > 0:
        lyrics = lyrics_list[0]
        res.update({
            "found": True,
            "result_title": lyrics["trackName"],
            "result_artist": lyrics["artistName"],
            "result_album": lyrics["albumName"],
            "duration": lyrics["duration"],
            "lyrics": lyrics["plainLyrics"],
        })
    return res


def sample(song_list: list[dict], num_samples: int = 20, outfile: str = "samples.json", verbose: bool = False):
    res = []
    N = len(song_list)
    while len(res) < num_samples:
        i = random.randint(0, N)
        lyrics = search(song_list[i])
        if lyrics["found"] and lyrics["lyrics"] is not None:
            if verbose:
                print("="*80)
                print("Title: " + lyrics["result_title"])
                print("Artist Name: " + lyrics["result_artist"])
                print("Album Name: " + lyrics["result_album"])
                print(f"Duration: {lyrics['duration']}s")
                print("Lyrics: ")
                print(lyrics["lyrics"])

            #lyrics["lyrics"] = lyrics["lyrics"].encode("raw_unicode_escape").decode("utf-8")
            res.append(lyrics)
    with open(outfile, "w") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    return len(res)


def demo():
    if len(sys.argv) < 2:
        print("Please specify a music history json file.")
        exit(1)

    with open(sys.argv[1], "r") as f:
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

    with open(sys.argv[1], "r") as f:
        history = json.load(f)


    sample(history, verbose=True)


if __name__ == "__main__":
    demo2()
