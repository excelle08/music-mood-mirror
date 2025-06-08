# Music Mood Mirror Notebooks

This folder contains Jupyter notebooks and scripts for the Music Mood Mirror project, which analyzes song lyrics using both local and cloud-based large language models (LLMs). Below is a description of each file and setup instructions for running the project in AIStudio.

## Contents

- **run_first.sh**  
    Bash script to install all required Python libraries and dependencies for the notebooks and scripts in this folder.

- **main_Music-mood Mirror.ipynb**  
    The main notebook for the Music Mood Mirror project. It performs end-to-end lyric analysis using selected LLMs.

- **ground_truth.py**  
    Python script to generate or collect ground truth data for lyric mood analysis, used for comparison and validation.

- **verify_results.ipynb**  
    Notebook to compare lyric analysis results from the local LLM (Gemma-2B) and OpenAI's o3-mini model against the ground truth.

- **RegisterLLM2MLflow.ipynb**  
    Notebook to register the Gemma-2B model with the built-in MLflow service in AIStudio for model management and tracking.

## AI Studio Setup Steps

1. **Install Required Libraries**  
     Run the following script to install all necessary dependencies:
     ```bash
     bash run_first.sh
     ```

2. **Run the Main Project Notebook**  
     Open and execute `main_Music-mood Mirror.ipynb` to perform the core lyric analysis workflow.

3. **Compare Lyric Analysis Results**  
     - Run `ground_truth.py` to prepare ground truth data.
     - Open and execute `verify_results.ipynb` to compare results from Gemma-2B and o3-mini models.

4. **Register the Local LLM with MLflow**  
     Open and execute `RegisterLLM2MLflow.ipynb` to register the Gemma-2B model with AIStudio's MLflow service. Note that here we documented what we have explored and issues encountered when registering our models to MLflow and deploying using Swagger through AI Studio. 

---

For any issues or questions, please refer to the project documentation or contact the repository maintainer.
