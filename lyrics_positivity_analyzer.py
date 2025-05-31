from llama_cpp import Llama
import os

from huggingface_hub import hf_hub_download

# Download the GGUF file to the current directory
hf_hub_download(
    repo_id="codegood/gemma-2b-it-Q4_K_M-GGUF",
    filename="gemma-2b-it.Q4_K_M.gguf",
    local_dir=".",
)

llm = Llama(
    model_path="./gemma-2b-it.Q4_K_M.gguf",
    # n_gpu_layers=35,# or 0 for CPU-only
    n_gpu_layers=35,
    n_ctx=8192, # maximum prompt + response tokens
    # use_mlock=True,          # optional: prevent swap
    verbose=False,
)

# ---------------- Context window size ----------------
# 'gemma.context_length' = Max tokens the model supports (prompt + output)
# This is the maximum number of tokens the model can process at once.

# n_ctx (in llama-cpp)	The number of tokens you allow during inference. It controls maximum prompt + response tokens
print("Context window size (n_ctx):", llm.n_ctx())
# ---------------- Model parameters ----------------
max_tokens = 512 # max number of tokens to generate in the output
# ---------------- Run model  ----------------
# output = llm("What is retrieval-augmented generation?", max_tokens=max_tokens)
# print(output["choices"][0]["text"])

lyrics = '''
敦煌天空的沙礫\n帶著我們的記憶\n我從半路看回去\n這情關漫漫好彎曲\n\n夢想穿過了西域\n包含了多少的禪意\n愛情像一本遊記\n我會找尋它的謎語\n\n看 月牙灣下的淚光\n在絲路之上被遺忘\n是誰的心啊 孤單的留下\n他還好嗎 我多想愛他\n拿永恆的淚 凝固的一句話\n也許可能蒸發\n\n是誰的愛啊 比淚水堅強\n輕聲呼喚 就讓我融化\n每一滴雨水 演化成我翅膀\n向著我愛的人 追吧\n\n夢想穿過了西域\n包含了多少的禪意\n愛情像一本遊記\n我會找尋它的謎語\n看 月牙灣下的淚光\n在絲路之上被遺忘\n\n是誰的心啊 孤單的留下\n他還好嗎 我多想愛他\n拿永恆的淚 凝固的一句話\n也許可能蒸發\n\n是誰的愛啊 比淚水堅強\n輕聲呼喚 就讓我融化\n每一滴雨水 演化成我翅膀\n向著我愛的人 追吧\n\n是誰的心啊 孤單的留下\n他還好嗎 我多想愛他\n拿永恆的淚 凝固的一句話\n也許可能蒸發\n\n是誰的愛啊 比淚水堅強\n輕聲呼喚 就讓我融化\n每一滴雨水 演化成我翅膀\n向著我愛的人 追吧
'''




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
    
def from_lyrics_to_positivity(lyrics: str) -> float:
    """
    Analyze the lyrics and return the average positivity score.
    
    Args:
        lyrics (str): The lyrics to analyze.
        
    Returns:
        float: The average positivity score of the lyrics.
    """
    prompt = """
    You are an expert in analyzing song lyrics to determine the emotions they convey.
        Analyze the following song lyrics and return exactly 3 emotion tags that best summarize the emotions conveyed by the song. Only list the tags, separated by commas.
        The tags must be adjectives and strictly chosen from the following list: Joyful, Melancholic, Hopeful, Angry, Romantic, Nostalgic, Sad, Energetic, Passionate, Lonely, Uplifting, Bittersweet, Empowering, Heartbroken, Reflective, Playful, Dark, Calm, Longing, Triumphant
    '''{lyrics}'''
    """
    
    response = llm(prompt.format(lyrics=lyrics), temperature=0.0, max_tokens=512, stop={"\n\n\n"})
    mood = response['choices'][0]['text'].strip().split('\n')
    
    tags_str = mood[0] if mood else ''
    tags = [tag.lstrip('#') for tag in tags_str.strip().split()]
    
    return get_avg_positivity_score(tags)