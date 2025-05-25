# music-mood-mirror
Music-Mood Mirror - An LLM-powered Emotional Wellness Companion by GinkoGreenAI
🎵 Project Idea: "Music-Mood Mirror" – An LLM-powered Emotional Wellness Companion

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



🔧 Architecture Sketch:

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

## Try out lyrics finding tool



## Setting up the Web UI

### Install prerequisites

```bash
sudo apt install mariadb-server python3.11 virtualenv
```

### Create MySQL database

```bash
$ mysql -uroot -p                                           
Enter password:                                                                
Welcome to the MariaDB monitor.  Commands end with ; or \g.                    
Your MariaDB connection id is 7                                                
Server version: 10.6.21-MariaDB-0ubuntu0.22.04.2 Ubuntu 22.04
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MariaDB [(none)]> create database music;                                       
Query OK, 1 row affected (0.002 sec)

MariaDB [(none)]> exit
Bye
```

### Set up virtual environment and install dependencies

```bash
virtualenv -p python3.10 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Check settings

Please open `config/settings.py` and check if the config variables are right for your
system, especially the MySQL password.

If you choose to deploy LRCLIB locally (by following this [instruction](https://github.com/tranxuanthang/lrclib)),
you can change the value of `LRCLIB_SITE` to `http://127.0.0.1:3306`.

### Start the website

Run the following command to start the web server:

```bash
python app.py
```

You can now open the webpage by visiting `http://127.0.0.1:8081` in your browser.
