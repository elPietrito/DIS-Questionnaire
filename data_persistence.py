# data_persistence.py
# ============================================
# DATA PERSISTENCE
# Saves and loads experiment data between sessions
# ============================================

import json
import os
from config import get_participant_folder

def get_experiment_data_path(participant_id: str) -> str:
    """Returns the path to the experiment data JSON file."""
    return os.path.join(get_participant_folder(participant_id), "experiment_data.json")


def save_experiment_data(participant_id: str, episodes: list):
    """
    Saves experiment data (Part 1) to a JSON file.
    This allows the participant to load the data when they open the link.
    
    Args:
        participant_id: Participant's ID
        episodes: List of episode dictionaries
    """
    data_path = get_experiment_data_path(participant_id)
    
    # Convert episodes to JSON-serializable format
    data = {
        'participant_id': participant_id,
        'episodes': episodes
    }
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data_path


def load_experiment_data(participant_id: str) -> dict:
    """
    Loads experiment data from JSON file.
    
    Args:
        participant_id: Participant's ID
    
    Returns:
        Dictionary with 'participant_id' and 'episodes', or None if not found
    """
    data_path = get_experiment_data_path(participant_id)
    
    if not os.path.exists(data_path):
        return None
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def experiment_data_exists(participant_id: str) -> bool:
    """
    Checks if experiment data exists for a participant.
    
    Args:
        participant_id: Participant's ID
    
    Returns:
        True if data exists, False otherwise
    """
    data_path = get_experiment_data_path(participant_id)
    return os.path.exists(data_path)
