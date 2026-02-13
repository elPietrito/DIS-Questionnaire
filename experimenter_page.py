# experimenter_page.py
# ============================================
# EXPERIMENTER INTERFACE (PART 1)
# Interface for uploading audio and setting up episodes
# ============================================

import streamlit as st
import os
from config import *
from state_manager import *
from data_persistence import save_experiment_data

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
    # SHOW PARTICIPANT LINK (always visible once ID is set)
    # ============================================
    
    st.success(f"**Participant ID:** {st.session_state.participant_id}")
    
    # Get the participant link
    # Use a simpler approach that works across different Streamlit versions
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    participant_url = f"http://{local_ip}:8501/?participant={st.session_state.participant_id}"
    
    with st.expander("🔗 **Participant Link** (Click to expand)", expanded=False):
        st.code(participant_url, language=None)
        st.caption("📱 Share this link with the participant to access Part 2")
        st.caption("💡 Make sure both devices are on the same WiFi/hotspot")
    
    if st.button("🔄 Change Participant ID", key="change_participant"):
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
        
        # Likert scale for Audio 1 (only if audio exists)
        current_episode['likert1'] = st.select_slider(
            f"{PART1_LIKERT_1_LABEL} (Audio 1)",
            options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
            value=current_episode.get('likert1') or LIKERT_MIN,
            key=f"likert1_{episode_num}"
        )
        
        # Multiple choice for Audio 1 (only if audio exists)
        choice1_value = current_episode.get('choice1')
        choice1_index = PART1_CHOICE_OPTIONS.index(choice1_value) if choice1_value in PART1_CHOICE_OPTIONS else 0
        current_episode['choice1'] = st.selectbox(
            "Personnage (Audio 1)",
            options=PART1_CHOICE_OPTIONS,
            index=choice1_index,
            key=f"choice1_{episode_num}"
        )
    else:
        # No audio uploaded - clear any saved values
        current_episode['likert1'] = None
        current_episode['choice1'] = None
        st.info("⬆️ Upload Audio 1 to answer questions")
    
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
        
        # Likert scale for Audio 2 (only if audio exists)
        current_episode['likert2'] = st.select_slider(
            f"{PART1_LIKERT_2_LABEL} (Audio 2)",
            options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
            value=current_episode.get('likert2') or LIKERT_MIN,
            key=f"likert2_{episode_num}"
        )
        
        # Multiple choice for Audio 2 (only if audio exists)
        choice2_value = current_episode.get('choice2')
        choice2_index = PART1_CHOICE_OPTIONS.index(choice2_value) if choice2_value in PART1_CHOICE_OPTIONS else 0
        current_episode['choice2'] = st.selectbox(
            "Personnage (Audio 2)",
            options=PART1_CHOICE_OPTIONS,
            index=choice2_index,
            key=f"choice2_{episode_num}"
        )
    else:
        # No audio uploaded - clear any saved values
        current_episode['likert2'] = None
        current_episode['choice2'] = None
        st.info("⬆️ Upload Audio 2 to answer questions")
    
    st.markdown("---")
    
    # ============================================
    # START PART 2 SECTION
    # ============================================
    
    st.subheader("✅ Ready to Start Part 2?")
    
    active_episodes = get_active_episodes()
    st.info(f"**{len(active_episodes)} episode(s)** ready for participant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Remote Participant")
        st.caption("Participant will access via the link above on their device (tablet/phone)")
        if st.button("🔗 Prepare for Remote Participant", type="primary", use_container_width=True):
            if len(active_episodes) == 0:
                st.error("Please fill at least one episode before preparing for participant")
            else:
                # Save data to disk so participant can load it
                save_experiment_data(st.session_state.participant_id, st.session_state.episodes)
                st.session_state.data_saved_for_participant = True
                st.rerun()
    
    with col2:
        st.markdown("#### 💻 Local Debrief")
        st.caption("Do Part 2 on this same computer (for testing or in-person)")
        if st.button("👤 Start Local Debrief", type="secondary", use_container_width=True):
            if len(active_episodes) == 0:
                st.error("Please fill at least one episode before starting debrief")
            else:
                # Save data to disk (just in case)
                save_experiment_data(st.session_state.participant_id, st.session_state.episodes)
                # Show Part 2 interface on the same computer
                st.session_state.show_local_debrief = True
                st.rerun()
    
    # Show success message if data was saved
    if st.session_state.get('data_saved_for_participant', False):
        st.success("✅ **Data saved successfully!**")
        st.info("""
        **Next steps:**
        1. Share the participant link (shown above) with the participant
        2. Participant opens the link and clicks **'Start Questionnaire'**
        3. They can start even if you haven't finished all episodes - just click 'Prepare' again to update
        """)
        
        if st.button("✏️ Continue Editing Episodes"):
            st.session_state.data_saved_for_participant = False
            st.rerun()
