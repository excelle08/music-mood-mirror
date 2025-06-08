from dataclasses import dataclass
import json
from pathlib import Path
import os

# This code defines a dataclass for song entries and provides functions to preprocess yearly song data from JSON files. 
# The `SongEntry` class encapsulates the attributes of a song, and the functions handle reading, parsing, and converting the data into instances of `SongEntry`.
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
    positivity_score_local_wghted: float = None  # Optional field for weighted positivity score
    repeats_this_week: int = 0  # Optional field for repeats this week
    
    # Method to convert a dictionary to a SongEntry instance
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
            week=data["week"],
            repeats_this_week=data.get("repeats_this_week", 0)  # Default to 0 if not present
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

'''
# This function cleans the lyrics by removing timestamps and extra whitespace, and removing redundant lyrics if needed. 
# It is not implemented yet, but the basic structure is provided here for future use.
def clean_lyrics(lyrics: str) -> str:
    """
    Cleans the lyrics by removing timestamps and extra whitespace.
    
    Args:
        lyrics (str): The raw lyrics string.
        
    Returns:
        str: Cleaned lyrics string.
    """
    # Remove timestamps like [00:47.01] In the input song history json file, the field "lyrics" does not contain timestamps, whereas synced_lyrics does, we don't need to clean the lyrics field
    cleaned_lyrics = re.sub(r'\[\d{2}:\d{2}\.\d{2}\]', '', lyrics)
    # Remove extra whitespace
    cleaned_lyrics = re.sub(r'\s+', ' ', cleaned_lyrics).strip()
    # TODO: clean up redundant lyrics to save tokens in LLM calls -- this is not implemented yet
    return cleaned_lyrics
'''
# Example usage
if __name__ == "__main__":
    # Example usage of the batch preprocessing function
    # This is just a placeholder path, you should replace it with the actual path to your data folder
    # r'C:\Users\sarah\Documents\Github\music-mood-mirror\data\input_yearly_filtered\with_lyrics'
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    all_processed_songs_by_year = batch_preprocess_yearly_data(r'C:\Users\sarah\Documents\Github\music-mood-mirror\data\input_yearly_filtered\with_lyrics', years)


# Example input music listening history in a json file
'''
Input music listening history example of 2 songs in a json file:
[
  {
    "title": "My Sweet Lord",
    "artist": "George Harrison",
    "album": "All Things Must Pass",
    "play_datetime": "2015-11-23 19:09:24",
    "result_title": "My Sweet Lord",
    "result_artist": "George Harrison",
    "result_album": "All Things Must Pass",
    "duration": 281.0,
    "seconds_played": 281.226,
    "music_completion_rate": 100.08,
    "lyrics": "My sweet Lord\nMy Lord\nMmm, my Lord\n\nI really want to see you\nReally want to be with you\nReally want to see you, Lord\nBut it takes so long, my Lord\n\nMy sweet Lord\nMy Lord\nMy Lord\n\nI really want to know you\nReally want to go with you\nReally want to show you, Lord\nBut it won't take long, my Lord (Hallelujah)\n\nMy sweet Lord (Hallelujah)\nMy Lord (Hallelujah)\nMy sweet Lord (Hallelujah)\n\nReally want to see you\nReally want to see you\nReally want to see you, Lord\nReally want to see you, Lord\nBut it takes so long, my lord (Hallelujah)\n\nMy sweet Lord (Hallelujah)\nMy Lord (Hallelujah)\nMy Lord (Hallelujah)\n\nI really want to know you (Hallelujah)\nReally want to go with you (Hallelujah)\nReally want to show you, Lord (Ah, ah)\nBut it won't take long, my Lord (Ah, ah, hallelujah)\n\nMm, mm, mm (Hallelujah)\nMy sweet Lord (Hallelujah)\nMy, my Lord (Hallelujah)\n\nMm, mm, my Lord (Hare Krishna)\nMy, my, my Lord (Hare Krishna)\nOh, oh my sweet Lord (Krishna Krishna)\nOoh, ooh, ooh (Hare Hare)\n\nNow, I really want to see you (Hare Rama)\nReally want to be with you (Hare Rama)\nReally want to see you, Lord (Ah, ah)\nBut it takes so long, my Lord (Ah, ah, hallelujah)\n\nMm, my Lord (Hallelujah)\nMy, my, my Lord (Hare Krishna)\nMy sweet Lord (Hare Krishna)\nMy sweet Lord (Krishna Krishna)\nMy lord (Hare Hare)\n\nMm, mm (Gurur Brahma)\nMm, mm (Gurur Vishnu)\nMm, mm (Gurur Devo)\nMm, mm (Maheshwarah)\n\nMy sweet Lord (Guru Sakshata)\nMy sweet Lord (Parabrahma)\nMy, my, my Lord (Tasmayi Shree)\nMy, my, my, my Lord (Guruve namah)\n\nMy sweet Lord (Hare Rama)\n(Hare Krishna)\nMy sweet Lord (Hare Krishna)\nMy sweet Lord (Krishna Krishna)\nMy lord (Hare Hare)",
    "synced_lyrics": "[00:30.36] My sweet Lord\n[00:34.44] My Lord\n[00:38.11] Mmm, my Lord\n[00:42.33] I really want to see you\n[00:46.47] Really want to be with you\n[00:49.75] Really want to see you, Lord\n[00:50.95] But it takes so long, my Lord\n[00:53.56] \n[00:58.50] My sweet Lord\n[01:02.36] My Lord\n[01:07.01] My Lord\n[01:10.19] I really want to know you\n[01:14.66] Really want to go with you\n[01:18.69] Really want to show you, Lord\n[01:21.38] But it won't take long, my Lord (Hallelujah)\n[01:26.63] \n[01:30.33] My sweet Lord (Hallelujah)\n[01:32.03] My Lord (Hallelujah)\n[01:34.37] My sweet Lord (Hallelujah)\n[01:38.07] Really want to see you\n[01:42.45] Really want to see you\n[01:46.06] Really want to see you, Lord\n[01:49.61] Really want to see you, Lord\n[01:52.87] But it takes so long, my lord (Hallelujah)\n[01:56.79] My sweet Lord (Hallelujah)\n[02:01.86] My Lord (Hallelujah)\n[02:05.66] My Lord (Hallelujah)\n[02:10.53] I really want to know you (Hallelujah)\n[02:14.35] Really want to go with you (Hallelujah)\n[02:18.11] Really want to show you, Lord (Ah, ah)\n[02:21.28] But it won't take long, my Lord (Ah, ah, hallelujah)\n[02:25.65] Mm, mm, mm (Hallelujah)\n[02:30.10] My sweet Lord (Hallelujah)\n[02:33.68] \n[02:35.94] My, my Lord (Hallelujah)\n[02:39.61] \n[02:54.89] Mm, mm, my Lord (Hare Krishna)\n[02:58.02] My, my, my Lord (Hare Krishna)\n[03:02.46] Oh, oh my sweet Lord (Krishna Krishna)\n[03:06.45] Ooh, ooh, ooh (Hare Hare)\n[03:10.07] Now, I really want to see you (Hare Rama)\n[03:14.32] Really want to be with you (Hare Rama)\n[03:18.55] Really want to see you, Lord (Ah, ah)\n[03:23.83] But it takes so long, my Lord (Ah, ah, hallelujah)\n[03:27.03] Mm, my Lord (Hallelujah)\n[03:29.44] My, my, my Lord (Hare Krishna)\n[03:33.21] My sweet Lord (Hare Krishna)\n[03:38.31] My sweet Lord (Krishna Krishna)\n[03:41.22] My lord (Hare Hare)\n[03:45.62] Mm, mm (Gurur Brahma)\n[03:50.53] Mm, mm (Gurur Vishnu)\n[03:53.89] Mm, mm (Gurur Devo)\n[03:58.18] Mm, mm (Maheshwarah)\n[04:03.17] My sweet Lord (Guru Sakshata)\n[04:06.15] My sweet Lord (Parabrahma)\n[04:09.70] My, my, my Lord (Tasmayi Shree)\n[04:13.53] My, my, my, my Lord (Guruve namah)\n[04:16.85] My sweet Lord (Hare Rama)\n[04:21.87] (Hare Krishna)\n[04:25.69] My sweet Lord (Hare Krishna)\n[04:28.28] My sweet Lord (Krishna Krishna)\n[04:32.20] My lord (Hare Hare)\n[04:33.07] ",
    "reason_start": "clickrow",
    "reason_end": "trackdone",
    "shuffle": false,
    "skipped": false,
    "repeats_next_7d": 0,
    "first_occurrence_in_week": true,
    "week": 48,
    "repeats_this_week": 1
  },
  {
    "title": "Where Do You Go To (My Lovely) [Re-Recorded]",
    "artist": "Peter Sarstedt",
    "album": "The Lost Album",
    "play_datetime": "2015-11-23 19:14:12",
    "result_title": "Where Do You Go To (My Lovely) (Re-Recorded)",
    "result_artist": "Peter Sarstedt",
    "result_album": "The Lost Album",
    "duration": 288.0,
    "seconds_played": 287.72,
    "music_completion_rate": 99.9,
    "lyrics": "You talk like Marlene Dietrich\nAnd you dance like Zizi Jeanmaire\nYour clothes are all made by Balmain\nAnd there's diamonds and pearls in your hair, yes there are.\n\nYou live in a fancy apartment\nOff the Boulevard of St. Michel\nWhere you keep your Rolling Stones records\nAnd a friend of Sacha Distel, yes you do.\n\nYou go to the embassy parties\nWhere you talk in Russian and Greek\nAnd the young men who move in your circles\nThey hang on every word you speak, yes they do.\n\nBut where do you go to my lovely\nWhen you're alone in your bed\nTell me the thoughts that surround you\nI want to look inside your head, yes I do.\n\nI've seen all your qualifications\nYou got from the Sorbonne\nAnd the painting you stole from Picasso\nYour loveliness goes on and on, yes it does.\n\nWhen you go on your summer vacation\nYou go to Juan-les-Pines\nWith your carefully designed topless swimsuit\nYou get an even suntan, on your back and on your legs.\n\nAnd when the snow falls you're found in St. Moritz\nWith the others of the jet-set\nAnd you sip your Napoleon Brandy\nBut you never get your lips wet, no you don't.\n\nBut where do you go to my lovely\nWhen you're alone in your bed\nTell me the thoughts that surround you\nI want to look inside your head, yes I do.\n\nYou're in between 20 and 30\nA very desirable age\nYour body is firm and inviting\nBut you live on a glittering stage, yes you do, yes you do.\n\nYour name is heard in high places\nYou know the Aga Khan\nHe sent you a racehorse for Christmas\nAnd you keep it just for fun, for a laugh ha-ha-ha\n\nThey say that when you get married\nIt'll be to a millionaire\nBut they don't realize where you came from\nAnd I wonder if they really care, or give a damn\n\nBut where do you go to my lovely\nWhen you're alone in your bed\nTell me the thoughts that surround you\nI want to look inside your head, yes i do.\n\nI remember the back streets of Naples\nTwo children begging in rags\nBoth touched with a burning ambition\nTo shake off their lowly-borne tags, they try\n\nSo look into my face Marie-Claire\nAnd remember just who you are\nThen go and forget me forever\nBut I know you still bear\nthe scar, deep inside, yes you do\n\nI know where you go to my lovely\nWhen you're alone in your bed\nI know the thoughts that surround you\n'Cause I can look inside your head.",
    "synced_lyrics": "[00:04.54] You talk like Marlene Dietrich\n[00:08.09] And you dance like Zizi Jeanmaire\n[00:11.82] Your clothes are all made by Balmain\n[00:15.64] And there's diamonds and pearls in your hair, yes there are.\n[00:21.88] You live in a fancy apartment\n[00:25.65] Off the Boulevard of St. Michel\n[00:29.53] Where you keep your Rolling Stones records\n[00:33.33] And a friend of Sacha Distel, yes you do.\n[00:39.78] You go to the embassy parties\n[00:43.45] Where you talk in Russian and Greek\n[00:47.05] And the young men who move in your circles\n[00:51.37] They hang on every word you speak, yes they do.\n[00:57.22] But where do you go to my lovely\n[01:01.31] When you're alone in your bed\n[01:05.11] Tell me the thoughts that surround you\n[01:08.74] I want to look inside your head, yes I do.\n[01:14.97] I've seen all your qualifications\n[01:18.62] You got from the Sorbonne\n[01:22.62] And the painting you stole from Picasso\n[01:26.33] Your loveliness goes on and on, yes it does.\n[01:32.01] When you go on your summer vacation\n[01:36.57] You go to Juan-les-Pines\n[01:40.12] With your carefully designed topless swimsuit\n[01:43.93] You get an even suntan, on your back and on your legs.\n[01:50.43] And when the snow falls you're found in St. Moritz\n[01:54.08] With the others of the jet-set\n[01:57.85] And you sip your Napoleon Brandy\n[02:01.79] But you never get your lips wet, no you don't.\n[02:07.84] But where do you go to my lovely\n[02:12.00] When you're alone in your bed\n[02:15.77] Tell me the thoughts that surround you\n[02:19.68] I want to look inside your head, yes I do.\n[02:25.88] You're in between 20 and 30\n[02:29.61] A very desirable age\n[02:33.23] Your body is firm and inviting\n[02:37.98] But you live on a glittering stage, yes you do, yes you do.\n[02:42.86] Your name is heard in high places\n[02:47.36] You know the Aga Khan\n[02:51.11] He sent you a racehorse for Christmas\n[02:54.84] And you keep it just for fun, for a laugh ha-ha-ha\n[03:01.22] They say that when you get married\n[03:04.87] It'll be to a millionaire\n[03:08.21] But they don't realize where you came from\n[03:12.55] And I wonder if they really care, or give a damn\n[03:18.78] But where do you go to my lovely\n[03:22.53] When you're alone in your bed\n[03:26.19] Tell me the thoughts that surround you\n[03:29.85] I want to look inside your head, yes i do.\n[03:36.26] I remember the back streets of Naples\n[03:40.21] Two children begging in rags\n[03:44.38] Both touched with a burning ambition\n[03:47.97] To shake off their lowly-borne tags, they try\n[03:53.99] So look into my face Marie-Claire\n[03:57.71] And remember just who you are\n[04:01.30] Then go and forget me forever\n[04:05.42] But I know you still bear\n[04:09.09] the scar, deep inside, yes you do\n[04:12.26] I know where you go to my lovely\n[04:15.42] When you're alone in your bed\n[04:18.83] I know the thoughts that surround you\n[04:23.15] 'Cause I can look inside your head.\n[04:27.50] ",
    "reason_start": "trackdone",
    "reason_end": "trackdone",
    "shuffle": false,
    "skipped": false,
    "repeats_next_7d": 0,
    "first_occurrence_in_week": true,
    "week": 48,
    "repeats_this_week": 1
  }
]
'''