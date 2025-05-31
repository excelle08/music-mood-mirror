from dataclasses import dataclass
import json
import re
from pathlib import Path
import os

'''
# sample_songs_3 = [
#   {
#     "album": "In Rainbows",
#     "artist": "Radiohead",
#     "duration": 255.0,
#     "first_occurrence_in_week": True,
#     "lyrics": "Don't get any big ideas\nThey're not gonna happen\n\nYou paint yourself white\nAnd fill up with noise\nBut there'll be something missing\n\nNow that you found it\nIt's gone\n\nNow that you feel it\nYou don't\nYou've gone off the rails\n\nSo don't get any big ideas\nThey're not gonna happen\n\nYou'll go to Hell\nFor what your dirty mind\nIs thinking",
#     "music_completion_rate": 81.08,
#     "play_datetime": "2019-01-02 02:14:44",
#     "reason_end": "logout",
#     "reason_start": "remote",
#     "repeats_next_7d": 5,
#     "result_album": "In Rainbows",
#     "result_artist": "Radiohead",
#     "result_title": "Nude",
#     "seconds_played": 206.75,
#     "shuffle": False,
#     "skipped": False,
#     "synced_lyrics": "[00:47.01] Don't get any big ideas\n[00:58.07] They're not gonna happen\n[01:05.58] \n[01:09.01] You paint yourself white\n[01:20.06] And fill up with noise\n[01:26.08] But there'll be something missing\n[01:34.08] \n[01:40.09] Now that you found it\n[01:47.07] It's gone\n[01:51.00] Now that you feel it\n[01:58.03] You don't\n[02:03.01] You've gone off the rails\n[02:07.18] \n[02:15.01] So don't get any big ideas\n[02:27.08] They're not gonna happen\n[02:35.24] \n[02:43.00] You'll go to Hell\n[02:50.05] For what your dirty mind\n[02:58.05] Is thinking\n[03:06.25] ",
#     "title": "Nude",
#     "week": 1
#   },
#   {
#     "album": "In Rainbows",
#     "artist": "Radiohead",
#     "duration": 255.0,
#     "first_occurrence_in_week": False,
#     "lyrics": "Don't get any big ideas\nThey're not gonna happen\n\nYou paint yourself white\nAnd fill up with noise\nBut there'll be something missing\n\nNow that you found it\nIt's gone\n\nNow that you feel it\nYou don't\nYou've gone off the rails\n\nSo don't get any big ideas\nThey're not gonna happen\n\nYou'll go to Hell\nFor what your dirty mind\nIs thinking",
#     "music_completion_rate": 107.44,
#     "play_datetime": "2019-01-02 02:19:39",
#     "reason_end": "trackdone",
#     "reason_start": "clickrow",
#     "repeats_next_7d": 4,
#     "result_album": "In Rainbows",
#     "result_artist": "Radiohead",
#     "result_title": "Nude",
#     "seconds_played": 273.962,
#     "shuffle": False,
#     "skipped": False,
#     "synced_lyrics": "[00:47.01] Don't get any big ideas\n[00:58.07] They're not gonna happen\n[01:05.58] \n[01:09.01] You paint yourself white\n[01:20.06] And fill up with noise\n[01:26.08] But there'll be something missing\n[01:34.08] \n[01:40.09] Now that you found it\n[01:47.07] It's gone\n[01:51.00] Now that you feel it\n[01:58.03] You don't\n[02:03.01] You've gone off the rails\n[02:07.18] \n[02:15.01] So don't get any big ideas\n[02:27.08] They're not gonna happen\n[02:35.24] \n[02:43.00] You'll go to Hell\n[02:50.05] For what your dirty mind\n[02:58.05] Is thinking\n[03:06.25] ",
#     "title": "Nude",
#     "week": 1
#   },
#   {
#     "album": "In Rainbows",
#     "artist": "Radiohead",
#     "duration": 229.0,
#     "first_occurrence_in_week": True,
#     "lyrics": "I'm the next step\nWaiting in the wings\n\nI'm an animal\nTrapped in your hot car\n\nI am all the days\nThat you choose to ignore\n\nYou are all I need\nYou are all I need\nI'm in the middle of your picture\nLying in the reeds\nI am a moth\nWho just wants to share your light\n\nI'm just an insect\nTrying to get out of the night\n\nI only stick with you\nBecause there are no others\n\nYou are all I need\nYou are all I need\nI am in the middle of your picture\nLying in the reeds\n\nIt's all wrong\nIt's all right\nIt's all right\nIt's all right\nIt's all wrong\nIt's all right\nIt's all right\nIt's all right\nIt's all wrong\nIt's all right\n",
#     "music_completion_rate": 99.89,
#     "play_datetime": "2019-01-02 02:23:32",
#     "reason_end": "trackdone",
#     "reason_start": "clickrow",
#     "repeats_next_7d": 2,
#     "result_album": "In Rainbows",
#     "result_artist": "Radiohead",
#     "result_title": "All I Need",
#     "seconds_played": 228.746,
#     "shuffle": False,
#     "skipped": False,
#     "synced_lyrics": "[00:35.12] I'm the next step\n[00:39.47] Waiting in the wings\n[00:44.68] \n[00:48.40] I'm an animal\n[00:53.05] Trapped in your hot car\n[00:58.10] \n[01:02.14] I am all the days\n[01:06.35] That you choose to ignore\n[01:11.93] \n[01:21.47] You are all I need\n[01:26.77] You are all I need\n[01:32.04] I'm in the middle of your picture\n[01:37.37] Lying in the reeds\n[01:43.57] I am a moth\n[01:47.28] Who just wants to share your light\n[01:53.26] \n[01:56.53] I'm just an insect\n[02:00.73] Trying to get out of the night\n[02:06.05] \n[02:10.28] I only stick with you\n[02:14.67] Because there are no others\n[02:21.22] \n[02:24.12] You are all I need\n[02:29.87] You are all I need\n[02:34.63] I am in the middle of your picture\n[02:40.26] Lying in the reeds\n[02:45.64] \n[03:12.80] It's all wrong\n[03:15.57] It's all right\n[03:18.33] It's all right\n[03:21.06] It's all right\n[03:23.86] It's all wrong\n[03:26.31] It's all right\n[03:29.19] It's all right\n[03:31.93] It's all right\n[03:34.72] It's all wrong\n[03:37.37] It's all right\n[03:39.38] ",
#     "title": "All I Need",
#     "week": 1
#   }]
'''

@dataclass
class SongEntry:
    album: str
    artist: str
    duration: float
    first_occurrence_in_week: bool
    lyrics: str
    music_completion_rate: float
    play_datetime: str
    reason_end: str
    reason_start: str
    repeats_next_7d: int
    result_album: str
    result_artist: str
    result_title: str
    seconds_played: float
    shuffle: bool
    skipped: bool
    synced_lyrics: str
    title: str
    week: int
    mood_tags: list[str] = None  # Optional field for mood tags
    positivity_score: float = None  # Optional field for positivity score
    mood_tags_local: list[str] = None  # Optional field for mood tags
    positivity_score_local: float = None  # Optional field for positivity score

    @staticmethod
    def from_dict(data: dict) -> "SongEntry":
        return SongEntry(
            album=data["album"],
            artist=data["artist"],
            duration=data["duration"],
            first_occurrence_in_week=data["first_occurrence_in_week"],
            lyrics=data["lyrics"],
            music_completion_rate=data["music_completion_rate"],
            play_datetime=data["play_datetime"],
            reason_end=data["reason_end"],
            reason_start=data["reason_start"],
            repeats_next_7d=data["repeats_next_7d"],
            result_album=data["result_album"],
            result_artist=data["result_artist"],
            result_title=data["result_title"],
            seconds_played=data["seconds_played"],
            shuffle=data["shuffle"],
            skipped=data["skipped"],
            synced_lyrics=data["synced_lyrics"],
            title=data["title"],
            week=data["week"]
        )
    

def preprocess_yearly_data(songs: list[dict]) -> list[SongEntry]:
    """
    Preprocesses a list of song entries into a list of SongEntry dataclass instances.
    
    Args:
        songs (list[dict]): List of song entries in dictionary format.
        
    Returns:
        list[SongEntry]: List of SongEntry instances.
    """
    return [SongEntry.from_dict(song) for song in songs]

def batch_preprocess_yearly_data(folder_path:Path, years: list[int]) -> dict[int, list[SongEntry]]:
    # Batch processing of songs from different years
    # years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    all_processed_songs_by_year = {} # dictionary to hold processed songs for each year

    for year in years:
        # folder_path = r'C:\Users\sarah\Documents\Github\music-mood-mirror\data\input_yearly_filtered\with_lyrics'
        file_path = os.path.join(folder_path, f'{year}.json')
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: # C:\\Users\\sarah\\Documents\\Github\\music-mood-mirror\\data\\input_yearly_filtered\\with_lyrics\\
                yearly_songs = json.load(f)
                processed_yearly_songs = preprocess_yearly_data(yearly_songs)
                all_processed_songs_by_year[year] = processed_yearly_songs # list of SongEntry instances
                print(f"Processed {len(processed_yearly_songs)} songs from {year}.")
        except FileNotFoundError:
            print(f"No data file found for the year {year}.")
    return all_processed_songs_by_year

def clean_lyrics(lyrics: str) -> str:
    """
    Cleans the lyrics by removing timestamps and extra whitespace.
    
    Args:
        lyrics (str): The raw lyrics string.
        
    Returns:
        str: Cleaned lyrics string.
    """
    # Remove timestamps like [00:47.01] lyrics does not contain timestamps, whereas synced_lyrics does
    cleaned_lyrics = re.sub(r'\[\d{2}:\d{2}\.\d{2}\]', '', lyrics)
    # Remove extra whitespace
    cleaned_lyrics = re.sub(r'\s+', ' ', cleaned_lyrics).strip()
    return cleaned_lyrics




# TODO: clean up redundant lyrics to save tokens in LLM calls




# Example usage
if __name__ == "__main__":

    '''
        # with open('C:\\Users\\sarah\\Documents\\Github\\music-mood-mirror\\data\\input_yearly_filtered\\with_lyrics\\2016.json', 'r', encoding='utf-8', errors='ignore') as f:
        #     sample_songs_2016 = json.load(f)


        # # Preprocess the sample songs
        # processed_songs = preprocess_yearly_data(sample_songs_2016)
        # for song in processed_songs:
        #     print(song)
        #     print(f"Title: {song.title}, Artist: {song.artist}, Album: {song.album}, Duration: {song.duration} seconds")
        #     print(f"Play DateTime: {song.play_datetime}, Lyrics: {song.lyrics[:50]}...")  # Print first 50 characters of lyrics
        #     print("-" * 40) # Separator for readability 

        # print(f"Total songs processed: {len(processed_songs)}")            

        # # Accessing lyrics of the first processed song as an example
        # if processed_songs:
        #     first_song_lyrics = processed_songs[0].lyrics
        #     print("Lyrics of the first song:")
        #     print(first_song_lyrics)
        #     print("First occurrence in week:", processed_songs[0].first_occurrence_in_week)


        # Batch processing of songs from different years
        # years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        # all_processed_songs = {} # dictionary to hold processed songs for each year
        # for year in years:
        #     try:
        #         with open(f'C:\\Users\\sarah\\Documents\\Github\\music-mood-mirror\\data\\input_yearly_filtered\\with_lyrics\\{year}.json', 'r', encoding='utf-8', errors='ignore') as f:
        #             yearly_songs = json.load(f)
        #             processed_yearly_songs = preprocess_yearly_data(yearly_songs)
        #             all_processed_songs[year] = processed_yearly_songs # list of SongEntry instances
        #             print(f"Processed {len(processed_yearly_songs)} songs from {year}.")
        #     except FileNotFoundError:
        #         print(f"No data file found for the year {year}.")
    '''

    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    all_processed_songs_by_year = batch_preprocess_yearly_data(r'C:\Users\sarah\Documents\Github\music-mood-mirror\data\input_yearly_filtered\with_lyrics', years)