# config.py
# ============================================
# SURVEY CONFIGURATION
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
PART1_CHOICE_OPTIONS = ["PP", "PS", "Off-voice"]

# ============================================
# PART 2: PARTICIPANT QUESTIONS
# ============================================

# Instruction text shown above each audio for participants
AUDIO_INSTRUCTION_TEXT = "Écoutez attentivement l'enregistrement audio et essayez de répondre aux questions suivantes."

# Prompt for text response field
# TEXT_RESPONSE_PROMPT = "Type your response here:"

# Special value for "No answer" option
NO_ANSWER_VALUE = "No answer"  # This will be saved in CSV when participant chooses not to answer

# --------------------------------------------
# Audio 1 Questions (Part 2)
# --------------------------------------------

# Text response prompt (what they heard)
AUDIO1_TEXT_RESPONSE_LABEL = "Qu'avez vous dit/entendu dans l'enregistrement ?"

# Grammar correction question (open text)
# {dream_word} will be replaced with "rêve" (DM) or "rêverie" (MW) in participant interface
AUDIO1_GRAMMAR_QUESTION = "Est-ce que la dernière réplique dite ou entendue pendant le {dream_word} est grammaticalement correcte pour vous ? Sinon, quelle aurait été la formulation correcte ?"

# Likert scale questions for Audio 1
# ADD/REMOVE questions by editing this list
PART2_AUDIO1_LIKERT_QUESTIONS = [
    "Pendant le {dream_word}, à quel point la dernière réplique vous a-t-elle surpris·e ? Evaluez votre niveau de surprise sur une échelle de 1 à 6.",  # ← Edit question text here
]

# Yes/No questions for Audio 1
# ADD/REMOVE questions by editing this list
PART2_AUDIO1_YESNO_QUESTIONS = [
    "Est-ce que la dernière réplique était cohérente dans le contexte du {dream_word} ?",  # ← Edit question text here
    "Est-ce que la dernière réplique serait cohérente dans votre vie réelle ?",  # ← Edit question text here
]

# --------------------------------------------
# Audio 2 Questions (Part 2)
# --------------------------------------------

# Text response prompt (what they heard)
AUDIO2_TEXT_RESPONSE_LABEL = "Qu'avez vous dit/entendu dans l'enregistrement ?"

# Grammar correction question (open text)
# {dream_word} will be replaced with "rêve" (DM) or "rêverie" (MW) in participant interface
AUDIO2_GRAMMAR_QUESTION = "Est-ce que l'avant-dernière réplique dite ou entendue pendant le {dream_word} est grammaticalement correcte pour vous ? Sinon, quelle aurait été la formulation correcte ?"

# Likert scale questions for Audio 2
# ADD/REMOVE questions by editing this list
PART2_AUDIO2_LIKERT_QUESTIONS = [
    "Pendant le {dream_word}, à quel point la dernière réplique vous a-t-elle surpris·e ? Evaluez votre niveau de surprise sur une échelle de 1 à 6.",  # ← Edit question text here
]

# Yes/No questions for Audio 2
# ADD/REMOVE questions by editing this list
PART2_AUDIO2_YESNO_QUESTIONS = [
    "Est-ce que l'avant-dernière réplique était cohérente dans le contexte du {dream_word} ?",  # ← Edit question text here
    "Est-ce que l'avant-dernière réplique serait cohérente dans votre vie réelle ?",  # ← Edit question text here
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
AUDIO1_PATH_SUFFIX = "_A1_path"
LIKERT1_SUFFIX = "_A1_control"
CHOICE1_SUFFIX = "_A1_personnage"
AUDIO2_PATH_SUFFIX = "_A2_path"
LIKERT2_SUFFIX = "A2_control"
CHOICE2_SUFFIX = "_A2_personnage"

# Part 2 column suffixes
AUDIO1_TEXT_SUFFIX = "_A1_text_response"
AUDIO1_GRAMMAR_SUFFIX = "_A1_grammar_response"
AUDIO1_LIKERT_PREFIX = "_A1_surprise"
AUDIO1_YESNO_PREFIX = "_A1_coherence"

AUDIO2_TEXT_SUFFIX = "_A2_text_response"
AUDIO2_GRAMMAR_SUFFIX = "_A2_grammar_response"
AUDIO2_LIKERT_PREFIX = "_A2_surprise"
AUDIO2_YESNO_PREFIX = "_A2_coherence"

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
