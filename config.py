# config.py
# ============================================
# SURVEY CONFIGURATION
# Easy-to-edit settings for your experiment
# ============================================

import os

# ============================================
# EXPERIMENT SETTINGS
# ============================================

MAX_EPISODES = 5  # Maximum number of episodes experimenter can create

LIKERT_MIN = 1    # Minimum Likert scale value
LIKERT_MAX = 6    # Maximum Likert scale value

# ============================================
# PART 1: EXPERIMENTER QUESTIONS
# ============================================

# Labels shown next to Likert scales in experimenter interface
PART1_LIKERT_1_LABEL = "Control"  # Label for first audio's Likert scale
PART1_LIKERT_2_LABEL = "Control"  # Label for second audio's Likert scale

# Options for the "Personnage" dropdown (add/remove options here)
PART1_CHOICE_OPTIONS = ["PP", "PS"]

# ============================================
# PART 2: PARTICIPANT QUESTIONS
# ============================================

# Instruction text shown above each audio for participants
AUDIO_INSTRUCTION_TEXT = "Please listen carefully and try writing what you heard."

# Prompt for text response field
TEXT_RESPONSE_PROMPT = "Type your response here:"

# --------------------------------------------
# Audio 1 Likert Questions
# ADD/REMOVE questions by editing this list
# --------------------------------------------
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Audio 1 – Likert question 1",  # ← Edit question text here
    "Audio 1 – Likert question 2",  # ← Edit question text here
    # To add more questions, copy a line above and paste here
    # Example: "Audio 1 – Likert question 3",
]

# --------------------------------------------
# Audio 2 Likert Questions  
# ADD/REMOVE questions by editing this list
# --------------------------------------------
PART2_AUDIO2_LIKERT_QUESTIONS = [
    "Audio 2 – Likert question 1",  # ← Edit question text here
    "Audio 2 – Likert question 2",  # ← Edit question text here
    # To add more questions, copy a line above and paste here
]

# ============================================
# FILE PATHS AND FOLDERS
# ============================================

PARTICIPANT_ROOT_FOLDER = "participants"  # Main folder for all participant data
AUDIO_FOLDER_NAME = "audio_files"        # Subfolder for audio files
CSV_FILENAME = "responses.csv"            # Name of the output CSV file

# Global CSV that aggregates all participants (optional)
GLOBAL_CSV_PATH = "all_participants_data.csv"

# ============================================
# CSV HEADER CUSTOMIZATION
# ============================================

# Base column labels (you can edit these)
PARTICIPANT_ID_COL = "participant_id"
EPISODE_PREFIX = "E"  # Episode prefix in column names (E1, E2, etc.)

# Part 1 column suffixes
AUDIO1_PATH_SUFFIX = "_audio1_path"
LIKERT1_SUFFIX = "_likert1"
CHOICE1_SUFFIX = "_choice1"
AUDIO2_PATH_SUFFIX = "_audio2_path"
LIKERT2_SUFFIX = "_likert2"
CHOICE2_SUFFIX = "_choice2"

# Part 2 column suffixes
AUDIO1_TEXT_SUFFIX = "_audio1_text_response"
AUDIO1_LIKERT_PREFIX = "_audio1_likert_q"
AUDIO2_TEXT_SUFFIX = "_audio2_text_response"
AUDIO2_LIKERT_PREFIX = "_audio2_likert_q"

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_participant_folder(participant_id: str) -> str:
    """Returns the full path to a participant's folder."""
    return os.path.join(PARTICIPANT_ROOT_FOLDER, participant_id)

def get_audio_folder(participant_id: str) -> str:
    """Returns the full path to a participant's audio folder."""
    return os.path.join(get_participant_folder(participant_id), AUDIO_FOLDER_NAME)

def get_participant_csv_path(participant_id: str) -> str:
    """Returns the full path to a participant's CSV file."""
    return os.path.join(get_participant_folder(participant_id), CSV_FILENAME)

def ensure_participant_folders(participant_id: str):
    """Creates participant folders if they don't exist."""
    os.makedirs(get_participant_folder(participant_id), exist_ok=True)
    os.makedirs(get_audio_folder(participant_id), exist_ok=True)
