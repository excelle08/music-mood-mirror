import os

from yearly_data_preprocessing import batch_preprocess_yearly_data

from openai import OpenAI

# from lyrics_positivity_analyzer import get_avg_positivity_score
import random
import pickle

# temporary fix for the llamacpp import
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
# Exmaple usage of OpenAI client
# client = OpenAI(
#   api_key=os.environ.get("OPENAI_API_KEY")
# )

# # completion = client.chat.completions.create(
# #   model="o3-mini",
# #   store=True,
# #   messages=[
# #     {"role": "user", "content": "write a haiku about nature"},
# #   ]
# # )


# lyrics = '''
# 敦煌天空的沙礫\n帶著我們的記憶\n我從半路看回去\n這情關漫漫好彎曲\n\n夢想穿過了西域\n包含了多少的禪意\n愛情像一本遊記\n我會找尋它的謎語\n\n看 月牙灣下的淚光\n在絲路之上被遺忘\n是誰的心啊 孤單的留下\n他還好嗎 我多想愛他\n拿永恆的淚 凝固的一句話\n也許可能蒸發\n\n是誰的愛啊 比淚水堅強\n輕聲呼喚 就讓我融化\n每一滴雨水 演化成我翅膀\n向著我愛的人 追吧\n\n夢想穿過了西域\n包含了多少的禪意\n愛情像一本遊記\n我會找尋它的謎語\n看 月牙灣下的淚光\n在絲路之上被遺忘\n\n是誰的心啊 孤單的留下\n他還好嗎 我多想愛他\n拿永恆的淚 凝固的一句話\n也許可能蒸發\n\n是誰的愛啊 比淚水堅強\n輕聲呼喚 就讓我融化\n每一滴雨水 演化成我翅膀\n向著我愛的人 追吧\n\n是誰的心啊 孤單的留下\n他還好嗎 我多想愛他\n拿永恆的淚 凝固的一句話\n也許可能蒸發\n\n是誰的愛啊 比淚水堅強\n輕聲呼喚 就讓我融化\n每一滴雨水 演化成我翅膀\n向著我愛的人 追吧
# '''

# prompt = """
#     Analyze the following song lyrics and return exactly 3 emotion tags that best summarize the emotions conveyed by the song. Only output the tags, in this format: #tag1 #tag2 #tag3.
#     The tags must be adjectives and strictly chosen from the following list: Joyful, Melancholic, Hopeful, Angry, Romantic, Nostalgic, Sad, Energetic, Passionate, Lonely, Uplifting, Bittersweet, Empowering, Heartbroken, Reflective, Playful, Dark, Calm, Longing, Triumphant
# '''{lyrics}'''
# """
# completion = client.chat.completions.create(
#     model="o3-mini",
#     reasoning_effort="high",  # or "medium" or "low"
#     store=True,
#     messages=[
#         {"role": "system", "content": "You are an expert in analyzing song lyrics to determine the emotions they convey."},
#         {"role": "user", "content": prompt.format(lyrics=lyrics)}
#     ]
# )

# print(completion.choices[0].message);
# response = completion.choices[0].message.content.strip()
# mood = response.split('\n')
# tags_str = mood[0] if mood else ''
# tags = [tag.lstrip('#') for tag in tags_str.strip().split()]
# print("Tags:", tags)


# positivity_score = get_avg_positivity_score(tags)

# # # along with weights assigning to each each tag that summing up to 100%
# # response = llm(prompt.format(lyrics=lyrics), temperature=0.0, max_tokens=512, stop={"\n\n\n"})
# # mood = response['choices'][0]['text'].strip().split('\n')
# # print(response, "\n************\n")
# # print(mood[0])


# Example usage
if __name__ == "__main__":

    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    all_processed_songs_by_year = batch_preprocess_yearly_data(r'C:\Users\sarah\Documents\Github\music-mood-mirror\data\input_yearly_filtered\with_lyrics', years)

    # Set your OpenAI API key'''
    os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual key
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Load the processed song entires for 2024
    songs_2024 = all_processed_songs_by_year.get(2024, [])
    if not songs_2024:
        print("No songs found for the year 2024.")
        exit(1)
    # Filter songs to only those where first_occurrence_in_week is True
    songs_2024 = [song for song in songs_2024 if getattr(song, "first_occurrence_in_week", True)]
    # Take a random sample of 20 songs from songs_2024
    sampled_songs = random.sample(songs_2024, min(20, len(songs_2024)))


    for song in sampled_songs:
        lyrics = song.lyrics
        prompt = """
        Analyze the following song lyrics and return exactly 3 emotion tags that best summarize the emotions conveyed by the song. Only output the tags, in this format: #tag1 #tag2 #tag3.
        The tags must be adjectives and strictly chosen from the following list: Joyful, Melancholic, Hopeful, Angry, Romantic, Nostalgic, Sad, Energetic, Passionate, Lonely, Uplifting, Bittersweet, Empowering, Heartbroken, Reflective, Playful, Dark, Calm, Longing, Triumphant
        '''{lyrics}'''
        """

        completion = client.chat.completions.create(
            model="o3-mini",
            reasoning_effort="high",  # or "medium" or "low"
            store=True,
            messages=[
                {"role": "system", "content": "You are an expert in analyzing song lyrics to determine the emotions they convey."},
                {"role": "user", "content": prompt.format(lyrics=lyrics)}
            ]
        )

        print(completion.choices[0].message)
        response = completion.choices[0].message.content.strip()
        mood = response.split('\n')
        tags_str = mood[0] if mood else ''
        tags = [tag.lstrip('#') for tag in tags_str.strip().split()]
        print("Tags:", tags)
        positivity_score = get_avg_positivity_score(tags)
        print("Positivity Score:", positivity_score)
        # Assign resulting mood tags and positivity score to the song object
        song.mood_tags = tags
        song.positivity_score = positivity_score
        print("Assigned tags and positivity score to song:", song.title, "by", song.artist, ":", song.mood_tags)
        print("Tags:", song.mood_tags,"\nPositivity Score:", song.positivity_score)
        print("-"*40)
        
    # Save the sampled songs with their mood tags and positivity scores to a pickle file
    with open("sampled_songs_20_from_2024.pkl", "wb") as f:
        pickle.dump(sampled_songs, f)
        


