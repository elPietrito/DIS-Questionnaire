# experimenter_page.py
# ============================================
# EXPERIMENTER INTERFACE (PART 1)
# Interface for uploading audio and setting up episodes
# ============================================

import streamlit as st
import os
from config import *
from state_manager import *

def save_uploaded_audio(uploaded_file, participant_id, episode_num, audio_num):
    """
    Saves an uploaded audio file to the participant's audio folder.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        participant_id: Participant's ID
        episode_num: Episode number (1-based)
        audio_num: Audio number (1 or 2)
    
    Returns:
        Tuple of (full_path, filename)
    """
    if uploaded_file is None:
        return None, None
    
    # Create filename: episode1_audio1.wav
    extension = os.path.splitext(uploaded_file.name)[1]
    filename = f"episode{episode_num}_audio{audio_num}{extension}"
    
    # Full path to save the file
    audio_folder = get_audio_folder(participant_id)
    full_path = os.path.join(audio_folder, filename)
    
    # Save the file
    with open(full_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return full_path, uploaded_file.name


def render_experimenter_page():
    """
    Renders the main experimenter interface (Part 1).
    """
    st.title("🎙️ Experimenter Interface - Part 1")
    st.markdown("---")
    
    # ============================================
    # PARTICIPANT ID SECTION
    # ============================================
    
    if st.session_state.participant_id is None:
        st.subheader("Step 1: Enter Participant ID")
        
        participant_input = st.text_input(
            "Participant ID:",
            placeholder="e.g., P001, ABC123",
            key="participant_input"
        )
        
        if st.button("Start Survey", type="primary"):
            if participant_input.strip():
                st.session_state.participant_id = participant_input.strip()
                ensure_participant_folders(st.session_state.participant_id)
                st.rerun()
            else:
                st.error("Please enter a participant ID")
        
        return
    
    # ============================================
    # SHOW PARTICIPANT ID AND PROGRESS
    # ============================================
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"**Participant ID:** {st.session_state.participant_id}")
    with col2:
        if st.button("🔄 Change Participant", key="change_participant"):
            reset_session()
            st.rerun()
    
    st.markdown("---")
    
    # ============================================
    # EPISODE NAVIGATION
    # ============================================
    
    st.subheader(f"📝 Episode {st.session_state.current_episode_index + 1} of {len(st.session_state.episodes)}")
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=(st.session_state.current_episode_index == 0)):
            navigate_to_episode(st.session_state.current_episode_index - 1)
            st.rerun()
    
    with col2:
        if st.button("➡️ Next", disabled=(st.session_state.current_episode_index >= len(st.session_state.episodes) - 1)):
            navigate_to_episode(st.session_state.current_episode_index + 1)
            st.rerun()
    
    with col3:
        if st.button("➕ Add Episode", disabled=(len(st.session_state.episodes) >= MAX_EPISODES)):
            if add_new_episode():
                st.rerun()
            else:
                st.warning(f"Maximum {MAX_EPISODES} episodes allowed")
    
    with col4:
        if st.button("🗑️ Delete", disabled=(len(st.session_state.episodes) <= 1)):
            delete_episode(st.session_state.current_episode_index)
            st.rerun()
    
    st.markdown("---")
    
    # ============================================
    # CURRENT EPISODE FORM
    # ============================================
    
    current_episode = get_current_episode()
    episode_num = st.session_state.current_episode_index + 1
    
    # -------- AUDIO 1 SECTION --------
    st.subheader("🎵 Audio 1")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        audio1_file = st.file_uploader(
            "Upload Audio 1",
            type=['wav', 'mp3', 'ogg'],
            key=f"audio1_upload_{episode_num}"
        )
        
        # Save uploaded file
        if audio1_file is not None:
            path, filename = save_uploaded_audio(
                audio1_file,
                st.session_state.participant_id,
                episode_num,
                1
            )
            current_episode['audio1_path'] = path
            current_episode['audio1_filename'] = filename
    
    # Show current audio and player if exists
    if current_episode.get('audio1_path') and os.path.exists(current_episode['audio1_path']):
        st.success(f"✅ Audio 1 loaded: {current_episode.get('audio1_filename', 'audio1')}")
        st.audio(current_episode['audio1_path'])
    
    # Likert scale for Audio 1
    current_episode['likert1'] = st.select_slider(
        f"{PART1_LIKERT_1_LABEL} (Audio 1)",
        options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
        value=current_episode.get('likert1') or LIKERT_MIN,
        key=f"likert1_{episode_num}"
    )
    
    # Multiple choice for Audio 1
    current_episode['choice1'] = st.selectbox(
        "Personnage (Audio 1)",
        options=PART1_CHOICE_OPTIONS,
        index=PART1_CHOICE_OPTIONS.index(current_episode.get('choice1', PART1_CHOICE_OPTIONS[0])),
        key=f"choice1_{episode_num}"
    )
    
    st.markdown("---")
    
    # -------- AUDIO 2 SECTION --------
    st.subheader("🎵 Audio 2")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        audio2_file = st.file_uploader(
            "Upload Audio 2",
            type=['wav', 'mp3', 'ogg'],
            key=f"audio2_upload_{episode_num}"
        )
        
        # Save uploaded file
        if audio2_file is not None:
            path, filename = save_uploaded_audio(
                audio2_file,
                st.session_state.participant_id,
                episode_num,
                2
            )
            current_episode['audio2_path'] = path
            current_episode['audio2_filename'] = filename
    
    # Show current audio and player if exists
    if current_episode.get('audio2_path') and os.path.exists(current_episode['audio2_path']):
        st.success(f"✅ Audio 2 loaded: {current_episode.get('audio2_filename', 'audio2')}")
        st.audio(current_episode['audio2_path'])
    
    # Likert scale for Audio 2
    current_episode['likert2'] = st.select_slider(
        f"{PART1_LIKERT_2_LABEL} (Audio 2)",
        options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
        value=current_episode.get('likert2') or LIKERT_MIN,
        key=f"likert2_{episode_num}"
    )
    
    # Multiple choice for Audio 2
    current_episode['choice2'] = st.selectbox(
        "Personnage (Audio 2)",
        options=PART1_CHOICE_OPTIONS,
        index=PART1_CHOICE_OPTIONS.index(current_episode.get('choice2', PART1_CHOICE_OPTIONS[0])),
        key=f"choice2_{episode_num}"
    )
    
    st.markdown("---")
    
    # ============================================
    # FINISH PART 1 SECTION
    # ============================================
    
    st.subheader("✅ Ready to Start Participant Session?")
    
    active_episodes = get_active_episodes()
    st.info(f"**{len(active_episodes)} episode(s)** ready for participant")
    
    if st.button("🚀 Generate Participant Link", type="primary", use_container_width=True):
        if len(active_episodes) == 0:
            st.error("Please fill at least one episode before generating link")
        else:
            st.session_state.part1_completed = True
            st.rerun()
    
    # ============================================
    # SHOW PARTICIPANT LINK IF READY
    # ============================================
    
    if st.session_state.part1_completed:
        st.success("✅ Experimenter part completed!")
        st.markdown("### 🔗 Participant Link")
        
        # Get current URL and add participant parameter
        participant_url = f"{st.runtime.config.get_option('browser.serverAddress')}:{st.runtime.config.get_option('server.port')}/?participant={st.session_state.participant_id}"
        
        st.code(participant_url, language=None)
        st.info("👆 Share this link with the participant. They will use it to complete Part 2.")
        
        if st.button("🔄 Edit Episodes (Restart Part 1)"):
            st.session_state.part1_completed = False
            st.rerun()
