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
from data_persistence import load_experiment_data, experiment_data_exists


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
    # LOAD PARTICIPANT DATA FROM DISK
    # ============================================
    
    # If this is a remote participant (not local debrief), load data from disk
    if not st.session_state.get('show_local_debrief', False):
        # Check if data exists
        if not experiment_data_exists(participant_id):
            st.error(f"❌ No questionnaire data found for participant '{participant_id}'")
            st.info("**Instructions:**")
            st.markdown("""
            1. The experimenter needs to complete Part 1 first
            2. The experimenter should click **'🔗 Prepare for Remote Participant'**
            3. Once ready, click the button below to start
            """)
            
            if st.button("🔄 Check if Ready / Start Questionnaire", type="primary", use_container_width=True):
                st.rerun()
            
            return
        
        # Data exists - show "Start" or "Refresh" button
        if 'participant_data_loaded' not in st.session_state or not st.session_state.participant_data_loaded:
            st.info("✅ Questionnaire data is ready!")
            
            if st.button("▶️ Start Questionnaire", type="primary", use_container_width=True):
                # Load the data
                loaded_data = load_experiment_data(participant_id)
                if loaded_data:
                    # Update session state with loaded episodes
                    st.session_state.participant_id = loaded_data['participant_id']
                    st.session_state.episodes = loaded_data['episodes']
                    st.session_state.participant_data_loaded = True
                    st.session_state.participant_episode_index = 0
                    st.rerun()
            
            st.markdown("---")
            st.caption("💡 If the experimenter makes changes, you can click this button again to reload the latest data.")
            return
        
        # Allow refreshing data if needed
        with st.expander("🔄 Reload Latest Data"):
            st.caption("Click here if the experimenter made changes to the questionnaire")
            if st.button("Reload Data from Experimenter", key="reload_data"):
                loaded_data = load_experiment_data(participant_id)
                if loaded_data:
                    st.session_state.participant_id = loaded_data['participant_id']
                    st.session_state.episodes = loaded_data['episodes']
                    st.session_state.participant_episode_index = 0
                    st.success("✅ Data reloaded!")
                    st.rerun()
    
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
        
        # "No answer" checkbox
        no_answer_audio1 = st.checkbox(
            "I cannot answer this audio",
            key=f"no_answer_audio1_{current_index}",
            value=(current_episode.get('audio1_text_response', '') == NO_ANSWER_VALUE)
        )
        
        if no_answer_audio1:
            # Mark as "No answer" and disable inputs
            current_episode['audio1_text_response'] = NO_ANSWER_VALUE
            st.warning("✓ Marked as 'No answer' - skipping questions for this audio")
        else:
            # Text response
            st.markdown(f"**{TEXT_RESPONSE_PROMPT}**")
            current_episode['audio1_text_response'] = st.text_area(
                "Text Response (Audio 1)",
                value=current_episode.get('audio1_text_response', '') if current_episode.get('audio1_text_response', '') != NO_ANSWER_VALUE else '',
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
        
        # "No answer" checkbox
        no_answer_audio2 = st.checkbox(
            "I cannot answer this audio",
            key=f"no_answer_audio2_{current_index}",
            value=(current_episode.get('audio2_text_response', '') == NO_ANSWER_VALUE)
        )
        
        if no_answer_audio2:
            # Mark as "No answer" and disable inputs
            current_episode['audio2_text_response'] = NO_ANSWER_VALUE
            st.warning("✓ Marked as 'No answer' - skipping questions for this audio")
        else:
            # Text response
            st.markdown(f"**{TEXT_RESPONSE_PROMPT}**")
            current_episode['audio2_text_response'] = st.text_area(
                "Text Response (Audio 2)",
                value=current_episode.get('audio2_text_response', '') if current_episode.get('audio2_text_response', '') != NO_ANSWER_VALUE else '',
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
        st.success("✅ Survey completed successfully!")
        st.info("Thank you for your participation. You may now close this window.")
        
        # Show path to saved data
        if st.session_state.participant_id:
            csv_path = get_participant_csv_path(st.session_state.participant_id)
            st.caption(f"Data saved to: {csv_path}")
