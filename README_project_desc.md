# music-mood-mirror
 🎵Music-Mood Mirror - An LLM-powered Emotional Wellness Companion by GinkoGreenAI
--


We are developing Music Mood Mirror as part of an ongoing hackathon. The project aims to leverage the emotional signals embedded in music listening habits—particularly song lyrics and genres—to infer and track users’ emotional states over time. With the support of Large Language Models (LLMs) for sentiment and thematic analysis of lyrics, our system will provide users with a mood summary for specific periods, visualized through an interactive web dashboard.

While many individuals are naturally attuned to their emotions, this tool is designed with a specific focus on those who struggle with mental health challenges such as depression, anxiety, or bipolar disorder. For these users, emotional self-awareness can fluctuate or be difficult to articulate, making passive monitoring via music a valuable complementary perspective. The system could potentially assist therapists or psychiatrists by offering additional behavioral data points or early warning signals.

Unlike manual mood tracking features available on platforms such as iPhone Health, which rely on users’ ability and discipline to self-report, our solution reduces friction by inferring emotional states passively—based on the music they already listen to. This approach can be especially meaningful for those whose conditions make consistent journaling or self-logging difficult.

By integrating music, AI, and emotional well-being, Music Mood Mirror seeks to contribute to the Healthcare domain through a creative and empathetic lens.


🧠 Concept:
--
Collect user listening history (song titles, artists, timestamps)
Use LLM to:

Analyze lyrics for emotional content (valence, sentiment, recurring themes)
Map genre/tempo metadata to affective tone (e.g., ballads vs. upbeat pop)
Optionally, incorporate user input like journaling or self-reported mood
Output:

Visual or textual summary of emotional patterns over time
Insights like:

“You've been listening to more melancholic ballads this week, which may suggest lower mood. Want to try a calming playlist or talk to someone?”



🩺 Healthcare Tie-In:
--

Proactive mood tracking for preventative mental health care
Could link to wellness resources, breathing exercises, music therapy prompts
Optional: light journaling / chatbot check-ins to track self-perception vs. inferred mood



🔧 Architecture Sketch:
--

Frontend: Upload Spotify export or paste recent listening data
Backend:

Lyrics analysis (via Genius API + LLM sentiment/topic parsing)
Genre-to-affect mapping (via Spotify API or heuristic table)
HP AI Studio LLMs for summarizing emotional arcs or recommending interventions


🎵 MusicMood Mirror – Track Your Emotional State via Lyrics and Listening Habits



🛠️ MVP Goal (Simplest Feature)

User uploads recent music listening history (song + artist), and the app returns a summary of mood trends based on lyric and genre analysis.



✅ MVP Features (Prioritized for Feasibility)

Input: Upload CSV or paste text (e.g., Spotify export: song + artist + timestamp)
Lyric Retrieval: Use song title + artist to fetch lyrics via Genius API or pre-mocked sample
LLM-based Mood Analysis:

Run prompt like:
“What mood/emotions are most commonly expressed in these lyrics?”
Classify: happy / sad / angry / nostalgic / empowering (etc.)
Output: Generate a natural-language summary like:

“Your recent listening leans toward nostalgic and melancholic moods. You’ve also had a slight uptick in empowering tracks this week.”



📆 Suggested 4-Week Timeline
--
Weekly Goals


|| Week 1 |
Finalize dataset format (Spotify export or mock CSV)
Pick 10–20 songs to hardcode for dev/test
Setup basic web UI (upload CSV + submit button)

| | Week 2 |
Implement lyric fetcher (or pre-fetch and cache locally for MVP)
Design simple prompt templates for LLM mood inference via HP AI Studio
Create mapping from genre (pop, rock, lo-fi) to broad emotional tone

| | Week 3 |
Analyze mood from lyrics → tag each song
Compute mood distribution over time
Generate summary via LLM (e.g., “This week vs. last week”)

| | Week 4 |
Polish frontend: show mood pie chart or sentence summary
Add optional journaling input or playlist suggestion
Final testing + submission



🧪 Sample Prompt for HP AI Studio





textCopyEditSong Title: Someone Like You  
Artist: Adele  
Lyrics: I heard that you're settled down...  

Analyze the emotional tone of this song. List the 2-3 most dominant emotions and provide a 1-sentence summary of how this song might make a listener feel.

# Project_Story
## Inspiration
 🎵Music-Mood Mirror - An LLM-powered Emotional Wellness Companion by GinkoGreenAI

We are developing Music Mood Mirror as part of an ongoing hackathon. The project aims to leverage the emotional signals embedded in music listening habits—particularly song lyrics and genres—to infer and track users’ emotional states over time. With the support of Large Language Models (LLMs) for sentiment and thematic analysis of lyrics, our system will provide users with a mood summary for specific periods, visualized through an interactive web dashboard.

While many individuals are naturally attuned to their emotions, this tool is designed with a specific focus on those who struggle with mental health challenges such as depression, anxiety, or bipolar disorder. For these users, emotional self-awareness can fluctuate or be difficult to articulate, making passive monitoring via music a valuable complementary perspective. The system could potentially assist therapists or psychiatrists by offering additional behavioral data points or early warning signals.

Unlike manual mood tracking features available on platforms such as iPhone Health, which rely on users’ ability and discipline to self-report, our solution reduces friction by inferring emotional states passively—based on the music they already listen to. This approach can be especially meaningful for those whose conditions make consistent journaling or self-logging difficult.

By integrating music, AI, and emotional well-being, Music Mood Mirror seeks to contribute to the Healthcare domain through a creative and empathetic lens.
## What it does
🧠 Concept:
Collect user listening history (song titles, artists, timestamps)
Use LLM to:

Analyze lyrics for emotional content (valence, sentiment, recurring themes)
Map genre/tempo metadata to affective tone (e.g., ballads vs. upbeat pop)
Optionally, incorporate user input like journaling or self-reported mood
Output:

Visual or textual summary of emotional patterns over time
Insights like:

“You've been listening to more melancholic ballads this week, which may suggest lower mood. Want to try a calming playlist or talk to someone?”



🩺 Healthcare Tie-In:


Proactive mood tracking for preventative mental health care
Could link to wellness resources, breathing exercises, music therapy prompts
Optional: light journaling / chatbot check-ins to track self-perception vs. inferred mood


## How we built it

This project analyzes users' Spotify listening history to infer mood trends and emotional patterns using AI. By uploading Spotify data, users can visualize weekly mood trends, tag clouds, and playlist statistics. The system leverages the Gemma-2B large language model (LLM) running locally via `llama-cpp-python` to extract emotional tags from song lyrics and compute positivity scores.

We built a Python web application that processes Spotify JSON exports, cleans and filters the data, and identifies significant songs each week. The app uses the Gemma-2B LLM to analyze lyrics and assign emotional tags, which are mapped to positivity scores. The results are visualized through interactive charts and statistics. The app runs in a WSL2 environment, with dependencies managed in a virtual environment, and supports both pre-processed and raw Spotify datasets.
## Challenges we ran into
Below is a brief summary of challenges we ran into; please find the [detailed documentation HERE](./FEEDBACKS.md).
- Data loss can occur if notebooks are saved outside the `local` or `shared` folders in AI Studio; clearer warnings and state preservation are needed.
- Model registration and deployment documentation lacks critical details, such as the need for a `predict` method and proper model initialization.
- Deployment failure messages are too generic and do not provide actionable logs for debugging.
- Installing and running models from the Model Catalog is challenging due to dependency conflicts and unclear compatibility requirements.
- Workspace container images have various issues, including missing dependencies, lack of root access, and disabled features (e.g., Git extension in NeMo).
- AI-Blueprint sample projects do not provide enough guidance on selecting workspace images or managing dependencies.
- Occasional reliability issues, such as workspace freezing, were observed.

## Accomplishments that we're proud of

## What we learned

## What's next for GinkgoGreen


