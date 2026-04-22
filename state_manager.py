# state_manager.py
# ============================================
# SESSION STATE MANAGEMENT
# Handles Streamlit session state for episodes
# ============================================

import streamlit as st
from config import MAX_EPISODES, PART2_AUDIO1_LIKERT_QUESTIONS, PART2_AUDIO2_LIKERT_QUESTIONS, PART2_AUDIO1_YESNO_QUESTIONS, PART2_AUDIO2_YESNO_QUESTIONS


def create_empty_episode():
    """
    Creates an empty episode dictionary with all required fields.
    
    Returns:
        Dictionary with empty/default values for all episode fields
    """
    return {
        # Episode metadata
        'episode_time': None,  # Time in HH:MM:SS format
        
        # Part 1 fields (Experimenter)
        'audio1_path': None,
        'audio1_filename': None,  # Original filename for display
        'likert1': None,
        'choice1': None,
        'audio2_path': None,
        'audio2_filename': None,
        'likert2': None,
        'choice2': None,
        
        # Part 2 fields (Participant)
        'audio1_text_response': '',
        'audio1_grammar_response': '',  # New: Grammar correction question
        'audio1_likert_answers': [None] * len(PART2_AUDIO1_LIKERT_QUESTIONS),
        'audio1_yesno_answers': [None] * len(PART2_AUDIO1_YESNO_QUESTIONS),  # New: Yes/No questions
        'audio1_remarks': '',           # Free text remarks after yes/no questions
        
        'audio2_text_response': '',
        'audio2_grammar_response': '',  # New: Grammar correction question
        'audio2_likert_answers': [None] * len(PART2_AUDIO2_LIKERT_QUESTIONS),
        'audio2_yesno_answers': [None] * len(PART2_AUDIO2_YESNO_QUESTIONS),  # New: Yes/No questions
        'audio2_remarks': '',           # Free text remarks after yes/no questions
    }


def initialize_session_state():
    """
    Initializes Streamlit session state with default values.
    Called at the start of the app.
    """
    # Participant identification
    if 'participant_id' not in st.session_state:
        st.session_state.participant_id = None
    
    # Experiment type (DM = Dreaming, MW = Mind-Wandering)
    if 'experiment_type' not in st.session_state:
        st.session_state.experiment_type = None
    
    # Episodes list (up to MAX_EPISODES)
    if 'episodes' not in st.session_state:
        st.session_state.episodes = [create_empty_episode()]
    
    # Current episode index being viewed/edited
    if 'current_episode_index' not in st.session_state:
        st.session_state.current_episode_index = 0
    
    # Flag to track if experimenter has finished Part 1
    if 'part1_completed' not in st.session_state:
        st.session_state.part1_completed = False
    
    # Flag to show local debrief (Part 2 on same computer)
    if 'show_local_debrief' not in st.session_state:
        st.session_state.show_local_debrief = False
    
    # Flag to track if data has been saved for remote participant
    if 'data_saved_for_participant' not in st.session_state:
        st.session_state.data_saved_for_participant = False
    
    # Flag to track if participant has finished Part 2
    if 'survey_completed' not in st.session_state:
        st.session_state.survey_completed = False


def add_new_episode():
    """
    Adds a new empty episode to the episodes list.
    Only allows up to MAX_EPISODES.
    
    Returns:
        True if episode was added, False if at maximum
    """
    if len(st.session_state.episodes) < MAX_EPISODES:
        st.session_state.episodes.append(create_empty_episode())
        st.session_state.current_episode_index = len(st.session_state.episodes) - 1
        return True
    return False


def delete_episode(index: int):
    """
    Deletes an episode at the specified index.
    
    Args:
        index: Index of episode to delete (0-based)
    """
    if len(st.session_state.episodes) > 1:  # Keep at least one episode
        st.session_state.episodes.pop(index)
        
        # Adjust current index if needed
        if st.session_state.current_episode_index >= len(st.session_state.episodes):
            st.session_state.current_episode_index = len(st.session_state.episodes) - 1


def get_current_episode():
    """
    Returns the currently selected episode.
    
    Returns:
        Dictionary representing the current episode
    """
    return st.session_state.episodes[st.session_state.current_episode_index]


def get_active_episodes():
    """
    Returns episodes that have at least one field filled in Part 1.
    Used to determine which episodes to show to participant.
    
    Returns:
        List of episode dictionaries that are "active"
    """
    active = []
    for episode in st.session_state.episodes:
        # Check if any Part 1 field is filled
        if any([
            episode.get('audio1_path'),
            episode.get('audio2_path'),
            episode.get('likert1') is not None,
            episode.get('likert2') is not None,
            episode.get('choice1'),
            episode.get('choice2'),
        ]):
            active.append(episode)
    
    return active


def navigate_to_episode(index: int):
    """
    Changes the current episode index.
    
    Args:
        index: Target episode index (0-based)
    """
    if 0 <= index < len(st.session_state.episodes):
        st.session_state.current_episode_index = index


def reset_session():
    """
    Clears all session state data.
    Used to start a new survey from scratch.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()
