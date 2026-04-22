# data_persistence.py
# ============================================
# DATA PERSISTENCE
# Saves and loads experiment data between sessions
# ============================================

import json
import os
from config import get_participant_folder

def get_experiment_data_path(participant_id: str, experiment_type: str = None) -> str:
    """
    Returns the path to the experiment data JSON file.
    
    Args:
        participant_id: Participant ID
        experiment_type: Experiment type (DM or MW). If None, returns default path.
    """
    if experiment_type:
        filename = f"experiment_data_{experiment_type}.json"
    else:
        filename = "experiment_data.json"
    return os.path.join(get_participant_folder(participant_id), filename)


def save_experiment_data(participant_id: str, experiment_type: str, episodes: list):
    """
    Saves experiment data (Part 1) to a JSON file.
    This allows the participant to load the data when they open the link.
    
    Args:
        participant_id: Participant's ID
        experiment_type: Experiment type code (DM or MW)
        episodes: List of episode dictionaries
    """
    data_path = get_experiment_data_path(participant_id, experiment_type)
    
    # Convert episodes to JSON-serializable format
    data = {
        'participant_id': participant_id,
        'experiment_type': experiment_type,
        'episodes': episodes
    }
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data_path


def load_experiment_data(participant_id: str, experiment_type: str = None) -> dict:
    """
    Loads experiment data from JSON file.
    
    Args:
        participant_id: Participant's ID
        experiment_type: Experiment type (DM or MW). If None, tries default path first.
    
    Returns:
        Dictionary with 'participant_id', 'experiment_type', and 'episodes', or None if not found
    """
    data_path = get_experiment_data_path(participant_id, experiment_type)
    
    if not os.path.exists(data_path):
        return None
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle old data format (backward compatibility)
    if 'experiment_type' not in data:
        data['experiment_type'] = 'DM'  # Default to DM for old data
    
    return data


def experiment_data_exists(participant_id: str, experiment_type: str = None) -> bool:
    """
    Checks if experiment data exists for a participant.
    
    Args:
        participant_id: Participant's ID
        experiment_type: Experiment type (DM or MW). If None, checks default path.
    
    Returns:
        True if data exists, False otherwise
    """
    data_path = get_experiment_data_path(participant_id, experiment_type)
    return os.path.exists(data_path)
