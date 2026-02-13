# participant_page.py
# ============================================
# PARTICIPANT INTERFACE (PART 2)
# Interface for participants to listen and respond
# ============================================

import streamlit as st
import os
from config import *
from state_manager import *
from csv_handler import save_all_data


def render_participant_page(participant_id):
    """
    Renders the participant interface (Part 2).
    
    Args:
        participant_id: The participant's ID from URL parameter
    """
    st.title("🎧 Participant Interface - Part 2")
    
    # Show back button if in local debrief mode
    if st.session_state.get('show_local_debrief', False):
        if st.button("⬅️ Back to Part 1 (Experimenter)", key="back_to_part1"):
            st.session_state.show_local_debrief = False
            st.session_state.participant_episode_index = 0
            st.rerun()
    
    st.markdown("---")
    
    # ============================================
    # LOAD PARTICIPANT DATA
    # ============================================
    
    # Set participant ID in session state
    if st.session_state.participant_id != participant_id:
        st.session_state.participant_id = participant_id
    
    # Get active episodes (episodes with data from Part 1)
    active_episodes = get_active_episodes()
    
    if len(active_episodes) == 0:
        st.error("No episodes found for this participant. Please check the participant ID.")
        return
    
    # Initialize current episode index for participant navigation
    if 'participant_episode_index' not in st.session_state:
        st.session_state.participant_episode_index = 0
    
    current_index = st.session_state.participant_episode_index
    current_episode = active_episodes[current_index]
    
    # ============================================
    # PROGRESS INDICATOR
    # ============================================
    
    st.info(f"**Participant ID:** {participant_id}")
    st.progress((current_index + 1) / len(active_episodes))
    st.subheader(f"Episode {current_index + 1} of {len(active_episodes)}")
    st.markdown("---")
    
    # ============================================
    # AUDIO 1 SECTION
    # ============================================
    
    if current_episode.get('audio1_path') and os.path.exists(current_episode['audio1_path']):
        st.subheader("🎵 Audio 1")
        st.info(AUDIO_INSTRUCTION_TEXT)
        
        # Audio player
        st.audio(current_episode['audio1_path'])
        
        # Text response
        st.markdown(f"**{TEXT_RESPONSE_PROMPT}**")
        current_episode['audio1_text_response'] = st.text_area(
            "Text Response (Audio 1)",
            value=current_episode.get('audio1_text_response', ''),
            height=100,
            key=f"audio1_text_{current_index}",
            label_visibility="collapsed"
        )
        
        # Likert questions for Audio 1
        st.markdown("**Please answer the following questions:**")
        for q_idx, question in enumerate(PART2_AUDIO1_LIKERT_QUESTIONS):
            current_episode['audio1_likert_answers'][q_idx] = st.select_slider(
                question,
                options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
                value=current_episode['audio1_likert_answers'][q_idx] or LIKERT_MIN,
                key=f"audio1_likert_{current_index}_q{q_idx}"
            )
        
        st.markdown("---")
    
    # ============================================
    # AUDIO 2 SECTION
    # ============================================
    
    if current_episode.get('audio2_path') and os.path.exists(current_episode['audio2_path']):
        st.subheader("🎵 Audio 2")
        st.info(AUDIO_INSTRUCTION_TEXT)
        
        # Audio player
        st.audio(current_episode['audio2_path'])
        
        # Text response
        st.markdown(f"**{TEXT_RESPONSE_PROMPT}**")
        current_episode['audio2_text_response'] = st.text_area(
            "Text Response (Audio 2)",
            value=current_episode.get('audio2_text_response', ''),
            height=100,
            key=f"audio2_text_{current_index}",
            label_visibility="collapsed"
        )
        
        # Likert questions for Audio 2
        st.markdown("**Please answer the following questions:**")
        for q_idx, question in enumerate(PART2_AUDIO2_LIKERT_QUESTIONS):
            current_episode['audio2_likert_answers'][q_idx] = st.select_slider(
                question,
                options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
                value=current_episode['audio2_likert_answers'][q_idx] or LIKERT_MIN,
                key=f"audio2_likert_{current_index}_q{q_idx}"
            )
        
        st.markdown("---")
    
    # ============================================
    # NAVIGATION BUTTONS
    # ============================================
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Previous button
        if current_index > 0:
            if st.button("⬅️ Previous Episode", use_container_width=True):
                st.session_state.participant_episode_index -= 1
                st.rerun()
    
    with col2:
        # Next or Finish button
        if current_index < len(active_episodes) - 1:
            if st.button("➡️ Next Episode", type="primary", use_container_width=True):
                st.session_state.participant_episode_index += 1
                st.rerun()
        else:
            if st.button("✅ Finish Survey", type="primary", use_container_width=True):
                # Save all data to CSV
                try:
                    csv_path = save_all_data(participant_id, st.session_state.episodes)
                    st.session_state.survey_completed = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving data: {str(e)}")
    
    # ============================================
    # COMPLETION MESSAGE
    # ============================================
    
    if st.session_state.survey_completed:
        st.success("🎉 Survey completed successfully!")
        st.balloons()
        st.info("Thank you for your participation. You may now close this window.")
