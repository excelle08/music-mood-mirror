# Project_Story
# 🎵 Music Mood Mirror – An LLM-powered Emotional Wellness Companion  
### by GinkoGreenAI

## 🧠 Inspiration  
Music often reflects our emotional state—sometimes more honestly than we can express ourselves. While many people intuitively recognize this connection, those navigating mental health challenges like depression, anxiety, or bipolar disorder may struggle with emotional awareness.  

**Music Mood Mirror** was born from the idea that our listening habits—especially lyrics and genres—can act as passive signals for emotional trends. By tapping into the music people already love, we aim to offer meaningful emotional insights without the burden of manual tracking or journaling.

### 🏥 Healthcare Relevance  
**Music Mood Mirror** is directly aligned with the healthcare theme of this hackathon, focusing on **mental wellness and emotional self-awareness**.  

- For individuals with conditions like **depression**, **anxiety**, or **bipolar disorder**, emotional self-tracking can be inconsistent or burdensome.  
- Our tool provides a **non-intrusive, passive method** for emotional monitoring, supplementing traditional mood journaling.  
- Insights from the app could potentially be shared with **therapists, psychiatrists, or wellness platforms** to offer early signals of emotional changes or relapses.  
- The use of LLMs for **emotional signal extraction from natural media (music)** adds a novel angle to digital mental health support.

## ⚙️ What It Does  
**Music Mood Mirror** is a web app that passively analyzes users’ music listening history to track emotional trends over time. It leverages Large Language Models (LLMs) to extract sentiment, positivity scores, and recurring emotional themes from song lyrics.


### ✅ Key Features

- **Input**:  
  - User-uploaded listening history (song titles, artists, timestamps)  

- **LLM-Powered Analysis**:  
  - Sentiment and thematic analysis of lyrics  
  - Emotion tagging and positivity scoring  

- **Output**:  
  - Weekly stats: play duration, reason, completion %, repeat count  
  - Mood tags and scores (when user enables “Analyze Mood with AI”)  
  - Visualizations of emotional themes by week  
### 💡 Who It’s For  
Although designed with mental health support in mind, **Music Mood Mirror** is equally valuable for anyone curious about how their music reflects their mood—turning everyday playlists into a mirror for emotional self-awareness.
Let me know if you’d like a visual diagram or flowchart to include in your submission, or if you need a shorter version for slide decks!

## 🛠️ How we built it

This project analyzes users' Spotify listening history to infer mood trends and emotional patterns using AI. By uploading Spotify data, users can visualize weekly mood trends, tag clouds, and playlist statistics. The system leverages the Gemma-2B large language model (LLM) running locally via `llama-cpp-python` to extract emotional tags from song lyrics and compute positivity scores.

We built a Python web application that processes Spotify JSON exports, cleans and filters the data, and identifies significant songs each week. The app uses the Gemma-2B LLM to analyze lyrics and assign emotional tags, which are mapped to positivity scores. The results are visualized through interactive charts and statistics. The app runs in a WSL2 environment, with dependencies managed in a virtual environment, and supports both pre-processed and raw Spotify datasets.
## 🧗 Challenges we ran into
Below is a brief summary of challenges we ran into; please find the [detailed documentation HERE](./FEEDBACKS.md).
- Data loss can occur if notebooks are saved outside the `local` or `shared` folders in AI Studio; clearer warnings and state preservation are needed.
- Model registration and deployment documentation lacks critical details, such as the need for a `predict` method and proper model initialization.
- Deployment failure messages are too generic and do not provide actionable logs for debugging.
- Installing and running models from the Model Catalog is challenging due to dependency conflicts and unclear compatibility requirements.
- Workspace container images have various issues, including missing dependencies, lack of root access, and disabled features (e.g., Git extension in NeMo).
- AI-Blueprint sample projects do not provide enough guidance on selecting workspace images or managing dependencies.
- Occasional reliability issues, such as workspace freezing, were observed.

## 🏆 Accomplishments that we're proud of

One of our proudest achievements is seeing this project come full circle. As long-time friends who first teamed up on a college entrepreneurship competition a decade ago (which we couldn’t complete at the time), building *Music Mood Mirror* represents not only technical progress, but also personal growth. Today, with one of us working as a Data Scientist/ML Engineer and the other as a Software Engineer, we were able to turn a shared vision into a functional AI-powered product — end to end.

We’re proud of:
- Designing and deploying a complete LLM-powered emotional analysis pipeline
- Creating a responsive web dashboard to visualize mood trends
- Building a product with potential real-world application in mental health and wellness

This project demonstrates not just technical execution, but a mature collaboration rooted in long-term teamwork and shared goals.

## 📚 What we learned
This hackathon challenged us to move quickly while balancing thoughtful design with practical constraints. Along the way, we:

- Strengthened our ability to integrate LLMs for domain-specific applications (sentiment analysis on lyrics)
- Gained hands-on experience translating raw data into user-facing insights through full-stack development
- Learned how to scope and execute an idea with empathy, keeping the end-user experience — especially for those with mental health challenges — at the forefront

Most of all, we learned that strong collaboration, clear communication, and mutual respect are just as critical to successful product development as the technical tools we use.

## 🚀 What's next for MusicMoodMirror, An LLM-powered Emotional Wellness Companion

- **Enhancing Personalization**  
  We plan to introduce mood trend summaries and intelligent suggestions such as:  
  > *“You've been listening to more melancholic ballads this week, which may suggest a lower mood. Want to try a calming playlist or talk to someone?”*  
  This will help users reflect on their emotional patterns and take proactive steps when needed.

- **Improving Model Accuracy and Efficiency**  
  We'll continue refining our LLM pipeline through techniques like fine-tuning, smarter data sampling, and domain-specific adjustments to improve the quality and responsiveness of *Music Mood Mirror*.

- **Growing as a Team**  
  Looking ahead, we’re excited to deepen both our product thinking and technical capabilities. Our goal is to keep building meaningful, AI-powered tools that positively impact people’s lives—starting with music and mental wellness.


<!-- ## 🏆 Accomplishments that we're proud of
One of the most meaningful accomplishments for us goes beyond the code itself. This project marks a full-circle moment in our friendship — we first teamed up for a college entrepreneur competition nearly 10 years ago but weren’t able to complete it due to coursework demands. Now, a decade later, we’ve grown into a data scientist/ML engineer and a software engineer, finally bringing a shared idea to life with *Music Mood Mirror*.

We're proud of building an end-to-end prototype within a short timeframe, combining LLM-based emotional analysis, a functional backend pipeline, and a responsive web dashboard. This wasn’t just a technical win — it was a personal one, too.

## 📚 What we learned
Through this hackathon, we learned how powerful it can be to blend friendship, creativity, and technical skill into something with the potential to make a real impact. We deepened our experience with LLMs, learned how to process and visualize emotional data from lyrics, and sharpened our ability to iterate quickly across the full stack — from ideation to deployment.

Most importantly, we were reminded that collaboration grounded in mutual respect and shared history can be a unique superpower. This project reinforced our belief in using technology with empathy — and we’re excited to keep building. -->