# csv_handler.py
# ============================================
# CSV GENERATION AND WRITING
# Handles creating CSV files with survey responses
# ============================================

import csv
import os
from config import *

# ============================================
# HEADER GENERATION
# ============================================

def generate_csv_header():
    """
    Generates the CSV header row based on config settings.
    
    Structure for each episode:
    - Participant info: participant_id, Exp (experiment type)
    - Part 1: audio1_path, likert1, choice1, audio2_path, likert2, choice2
    - Part 2: audio1_text_response, audio1_likert_q1, audio1_likert_q2, ...,
              audio2_text_response, audio2_likert_q1, audio2_likert_q2, ...
    """
    header = [PARTICIPANT_ID_COL, "Exp"]  # Add Exp column after participant_id
    
    # Generate columns for each episode
    for episode_num in range(1, MAX_EPISODES + 1):
        episode_prefix = f"{EPISODE_PREFIX}{episode_num}"
        
        # ----- Episode Time (before Part 1) -----
        header.append(f"Time_{episode_prefix}")
        
        # ----- Part 1 columns (Experimenter) -----
        header.extend([
            f"{episode_prefix}{AUDIO1_PATH_SUFFIX}",
            f"{episode_prefix}{LIKERT1_SUFFIX}",
            f"{episode_prefix}{CHOICE1_SUFFIX}",
            f"{episode_prefix}{AUDIO2_PATH_SUFFIX}",
            f"{episode_prefix}{LIKERT2_SUFFIX}",
            f"{episode_prefix}{CHOICE2_SUFFIX}",
        ])
        
        # ----- Part 2 columns (Participant - Audio 1) -----
        header.append(f"{episode_prefix}{AUDIO1_TEXT_SUFFIX}")
        header.append(f"{episode_prefix}{AUDIO1_GRAMMAR_SUFFIX}")  # Grammar question
        for q_num in range(len(PART2_AUDIO1_LIKERT_QUESTIONS)):
            header.append(f"{episode_prefix}{AUDIO1_LIKERT_PREFIX}{q_num + 1}")
        for q_num in range(len(PART2_AUDIO1_YESNO_QUESTIONS)):
            header.append(f"{episode_prefix}{AUDIO1_YESNO_PREFIX}{q_num + 1}")
        header.append(f"{episode_prefix}_A1_remarks")   # Free text remarks
        
        # ----- Part 2 columns (Participant - Audio 2) -----
        header.append(f"{episode_prefix}{AUDIO2_TEXT_SUFFIX}")
        header.append(f"{episode_prefix}{AUDIO2_GRAMMAR_SUFFIX}")  # Grammar question
        for q_num in range(len(PART2_AUDIO2_LIKERT_QUESTIONS)):
            header.append(f"{episode_prefix}{AUDIO2_LIKERT_PREFIX}{q_num + 1}")
        for q_num in range(len(PART2_AUDIO2_YESNO_QUESTIONS)):
            header.append(f"{episode_prefix}{AUDIO2_YESNO_PREFIX}{q_num + 1}")
        header.append(f"{episode_prefix}_A2_remarks")   # Free text remarks
    
    return header


# ============================================
# DATA FLATTENING
# ============================================

def flatten_episodes_to_row(participant_id: str, experiment_type: str, episodes: list):
    """
    Converts episode data into a single CSV row.
    
    Args:
        participant_id: The participant's unique ID
        experiment_type: Experiment type code (DM or MW)
        episodes: List of episode dictionaries
    
    Returns:
        List of values representing one CSV row
    """
    row = [participant_id, experiment_type]  # Add experiment type
    
    # Process each episode
    for episode in episodes:
        # ----- Episode Time -----
        row.append(episode.get('episode_time', ''))
        
        # ----- Part 1 data -----
        row.extend([
            episode.get('audio1_path', ''),
            episode.get('likert1', ''),
            episode.get('choice1', ''),
            episode.get('audio2_path', ''),
            episode.get('likert2', ''),
            episode.get('choice2', ''),
        ])
        
        # ----- Part 2 data: Audio 1 -----
        row.append(episode.get('audio1_text_response', ''))
        row.append(episode.get('audio1_grammar_response', ''))  # Grammar question
        audio1_likert = episode.get('audio1_likert_answers', [])
        for i in range(len(PART2_AUDIO1_LIKERT_QUESTIONS)):
            row.append(audio1_likert[i] if i < len(audio1_likert) else '')
        audio1_yesno = episode.get('audio1_yesno_answers', [])
        for i in range(len(PART2_AUDIO1_YESNO_QUESTIONS)):
            row.append(audio1_yesno[i] if i < len(audio1_yesno) else '')
        row.append(episode.get('audio1_remarks', ''))           # Free text remarks
        
        # ----- Part 2 data: Audio 2 -----
        row.append(episode.get('audio2_text_response', ''))
        row.append(episode.get('audio2_grammar_response', ''))  # Grammar question
        audio2_likert = episode.get('audio2_likert_answers', [])
        for i in range(len(PART2_AUDIO2_LIKERT_QUESTIONS)):
            row.append(audio2_likert[i] if i < len(audio2_likert) else '')
        audio2_yesno = episode.get('audio2_yesno_answers', [])
        for i in range(len(PART2_AUDIO2_YESNO_QUESTIONS)):
            row.append(audio2_yesno[i] if i < len(audio2_yesno) else '')
        row.append(episode.get('audio2_remarks', ''))           # Free text remarks
    
    return row


# ============================================
# CSV WRITING
# ============================================

def write_participant_csv(participant_id: str, experiment_type: str, episodes: list):
    """
    Writes participant data to their individual CSV file.
    
    Args:
        participant_id: The participant's unique ID
        experiment_type: Experiment type code (DM or MW)
        episodes: List of episode dictionaries
    """
    csv_path = get_participant_csv_path(participant_id, experiment_type)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(generate_csv_header())
        writer.writerow(flatten_episodes_to_row(participant_id, experiment_type, episodes))
    
    return csv_path


def append_to_global_csv(participant_id: str, experiment_type: str, episodes: list):
    """
    Appends participant data to the global CSV file (all participants).
    Creates the file with headers if it doesn't exist.
    
    Args:
        participant_id: The participant's unique ID
        experiment_type: Experiment type code (DM or MW)
        episodes: List of episode dictionaries
    """
    file_exists = os.path.exists(GLOBAL_CSV_PATH)
    
    with open(GLOBAL_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header if file is new
        if not file_exists:
            writer.writerow(generate_csv_header())
        
        # Append participant data
        writer.writerow(flatten_episodes_to_row(participant_id, experiment_type, episodes))


def save_all_data(participant_id: str, experiment_type: str, episodes: list):
    """
    Saves data to both participant CSV and global CSV.
    
    Args:
        participant_id: The participant's unique ID
        experiment_type: Experiment type code (DM or MW)
        episodes: List of episode dictionaries
    
    Returns:
        Path to the participant's CSV file
    """
    # Ensure folders exist
    ensure_participant_folders(participant_id)
    
    # Write to participant's CSV
    csv_path = write_participant_csv(participant_id, experiment_type, episodes)
    
    # Append to global CSV
    append_to_global_csv(participant_id, experiment_type, episodes)
    
    return csv_path
