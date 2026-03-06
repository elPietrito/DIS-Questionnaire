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
    st.title("🎧 Participant Interface")
    
    # Determine the correct word to use based on experiment type
    # DM (Dreaming) → "rêve"
    # MW (Mind-Wandering) → "rêverie"
    experiment_type = st.session_state.get('experiment_type', 'DM')
    dream_word = "rêve" if experiment_type == "DM" else "rêverie"
    
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
            st.error(f"❌ Aucune donnée issue du questionnaire n'a été trouvée pour le participant '{participant_id}'")
            st.info("**Instructions :**")
            st.markdown("""
            1. L'expérimentateur doit d'abord remplir la partie 1
            2. L'expérimentateur doit cliquer **'🔗 Prepare for Remote Participant'**
            3. Une fois prêt, cliquez sur le bouton ci-dessous pour commencer
            """)
            
            if st.button("🔄 Vérifier si prêt / Commencer le questionnaire", type="primary", use_container_width=True):
                st.rerun()
            
            return
        
        # Data exists - show "Start" or "Refresh" button
        if 'participant_data_loaded' not in st.session_state or not st.session_state.participant_data_loaded:
            st.info("✅ Les données du questionnaire sont prêtes !")
            
            if st.button("▶️ Commencer le questionnaire", type="primary", use_container_width=True):
                # Load the data
                loaded_data = load_experiment_data(participant_id)
                if loaded_data:
                    # Update session state with loaded episodes
                    st.session_state.participant_id = loaded_data['participant_id']
                    st.session_state.experiment_type = loaded_data.get('experiment_type', 'DM')  # Load experiment type
                    st.session_state.episodes = loaded_data['episodes']
                    st.session_state.participant_data_loaded = True
                    st.session_state.participant_episode_index = 0
                    st.rerun()
            
            st.markdown("---")
            st.caption("💡 Si l'expérimentateur apporte des modifications, vous pouvez cliquer à nouveau sur ce bouton pour recharger les dernières données.")
            return
        
        # Allow refreshing data if needed
        with st.expander("🔄 Recharger les dernières données"):
            st.caption("Cliquez ici si l'expérimentateur a apporté des modifications au questionnaire.")
            if st.button("Recharger les données depuis Experimenter", key="reload_data"):
                loaded_data = load_experiment_data(participant_id)
                if loaded_data:
                    st.session_state.participant_id = loaded_data['participant_id']
                    st.session_state.experiment_type = loaded_data.get('experiment_type', 'DM')  # Load experiment type
                    st.session_state.episodes = loaded_data['episodes']
                    st.session_state.participant_episode_index = 0
                    st.success("✅ Données rechargées !")
                    st.rerun()
    
    # Set participant ID in session state
    if st.session_state.participant_id != participant_id:
        st.session_state.participant_id = participant_id
    
    # Get active episodes (episodes with data from Part 1)
    active_episodes = get_active_episodes()
    
    if len(active_episodes) == 0:
        st.error("Aucun épisode trouvé pour ce participant. Veuillez vérifier l'identifiant du participant.")
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
    
    audio1_path = current_episode.get('audio1_path')
    # Check if audio1_path is an actual file (not a special message)
    if audio1_path and audio1_path not in ["The participant wishes not to answer", "The participant does not remember the answer"] and os.path.exists(audio1_path):
        st.subheader("🎵 Audio 1")
        st.info(AUDIO_INSTRUCTION_TEXT)
        
        # Audio player
        st.audio(audio1_path)
        
        # "No answer" checkbox
        no_answer_audio1 = st.checkbox(
            "Je ne peux/veux pas répondre aux questions concernant cet enregistrement audio.",
            key=f"no_answer_audio1_{current_index}",
            value=(current_episode.get('audio1_text_response', '') == NO_ANSWER_VALUE)
        )
        
        if no_answer_audio1:
            # Mark as "No answer" and disable inputs
            current_episode['audio1_text_response'] = NO_ANSWER_VALUE
            current_episode['audio1_grammar_response'] = NO_ANSWER_VALUE
            current_episode['audio1_likert_answers'] = [None] * len(PART2_AUDIO1_LIKERT_QUESTIONS)
            current_episode['audio1_yesno_answers'] = [None] * len(PART2_AUDIO1_YESNO_QUESTIONS)
            st.warning('✓ Marqué comme "No answer" - questions ignorées pour cet enregistrement audio')
        else:
            # 1. First text response (what they heard)
            st.markdown(f"**{AUDIO1_TEXT_RESPONSE_LABEL}**")
            current_episode['audio1_text_response'] = st.text_area(
                "Text Response (Audio 1)",
                value=current_episode.get('audio1_text_response', '') if current_episode.get('audio1_text_response', '') != NO_ANSWER_VALUE else '',
                height=100,
                key=f"audio1_text_{current_index}",
                label_visibility="collapsed",
                placeholder="Tapez votre réponse ici..."
            )
            
            # 2. Grammar correction question (new open text)
            st.markdown("---")
            st.markdown(f"**{AUDIO1_GRAMMAR_QUESTION.format(dream_word=dream_word)}**")
            current_episode['audio1_grammar_response'] = st.text_area(
                "Grammar Response (Audio 1)",
                value=current_episode.get('audio1_grammar_response', ''),
                height=80,
                key=f"audio1_grammar_{current_index}",
                label_visibility="collapsed",
                placeholder="Si oui, écrivez 'Oui'. Si non, écrivez la formulation correcte..."
            )
            
            # 3. Likert questions
            st.markdown("---")
            st.markdown("**Veuillez répondre aux questions suivantes :**")
            for q_idx, question in enumerate(PART2_AUDIO1_LIKERT_QUESTIONS):
                current_episode['audio1_likert_answers'][q_idx] = st.select_slider(
                    question.format(dream_word=dream_word),  # Replace {dream_word}
                    options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
                    value=current_episode['audio1_likert_answers'][q_idx] or LIKERT_MIN,
                    key=f"audio1_likert_{current_index}_q{q_idx}"
                )
            
            # 4. Yes/No questions (new)
            st.markdown("---")
            for q_idx, question in enumerate(PART2_AUDIO1_YESNO_QUESTIONS):
                # Use radio buttons for Yes/No
                current_value = current_episode['audio1_yesno_answers'][q_idx]
                if current_value is None:
                    current_value = "No response"
                
                response = st.radio(
                    question.format(dream_word=dream_word),  # Replace {dream_word}
                    options=["Oui", "Non", "Pas de response"],
                    index=["Yes", "No", "No response"].index(current_value) if current_value in ["Yes", "No", "No response"] else 2,
                    key=f"audio1_yesno_{current_index}_q{q_idx}",
                    horizontal=True
                )
                
                # Save the response (convert "No response" to None)
                current_episode['audio1_yesno_answers'][q_idx] = response if response != "No response" else None
        
        st.markdown("---")
    
    # ============================================
    # AUDIO 2 SECTION
    # ============================================
    
    audio2_path = current_episode.get('audio2_path')
    # Check if audio2_path is an actual file (not a special message)
    if audio2_path and audio2_path not in ["The participant wishes not to answer", "The participant does not remember the answer"] and os.path.exists(audio2_path):
        st.subheader("🎵 Audio 2")
        st.info(AUDIO_INSTRUCTION_TEXT)
        
        # Audio player
        st.audio(audio2_path)
        
        # "No answer" checkbox
        no_answer_audio2 = st.checkbox(
            "Je ne peux/veux pas répondre aux questions concernant cet enregistrement audio.",
            key=f"no_answer_audio2_{current_index}",
            value=(current_episode.get('audio2_text_response', '') == NO_ANSWER_VALUE)
        )
        
        if no_answer_audio2:
            # Mark as "No answer" and disable inputs
            current_episode['audio2_text_response'] = NO_ANSWER_VALUE
            current_episode['audio2_grammar_response'] = NO_ANSWER_VALUE
            current_episode['audio2_likert_answers'] = [None] * len(PART2_AUDIO2_LIKERT_QUESTIONS)
            current_episode['audio2_yesno_answers'] = [None] * len(PART2_AUDIO2_YESNO_QUESTIONS)
            st.warning('✓ Marqué comme "No answer" - questions ignorées pour cet enregistrement audio')
        else:
            # 1. First text response (what they heard)
            st.markdown(f"**{AUDIO2_TEXT_RESPONSE_LABEL}**")
            current_episode['audio2_text_response'] = st.text_area(
                "Text Response (Audio 2)",
                value=current_episode.get('audio2_text_response', '') if current_episode.get('audio2_text_response', '') != NO_ANSWER_VALUE else '',
                height=100,
                key=f"audio2_text_{current_index}",
                label_visibility="collapsed"
            )
            
            # 2. Grammar correction question (new open text)
            st.markdown("---")
            st.markdown(f"**{AUDIO2_GRAMMAR_QUESTION.format(dream_word=dream_word)}**")
            current_episode['audio2_grammar_response'] = st.text_area(
                "Grammar Response (Audio 2)",
                value=current_episode.get('audio2_grammar_response', ''),
                height=80,
                key=f"audio2_grammar_{current_index}",
                label_visibility="collapsed",
                placeholder="Si oui, écrivez 'correct'. Si non, écrivez la formulation correcte."
            )
            
            # 3. Likert questions
            st.markdown("---")
            st.markdown("**Veuillez répondre aux questions suivantes :**")
            for q_idx, question in enumerate(PART2_AUDIO2_LIKERT_QUESTIONS):
                current_episode['audio2_likert_answers'][q_idx] = st.select_slider(
                    question.format(dream_word=dream_word),  # Replace {dream_word}
                    options=list(range(LIKERT_MIN, LIKERT_MAX + 1)),
                    value=current_episode['audio2_likert_answers'][q_idx] or LIKERT_MIN,
                    key=f"audio2_likert_{current_index}_q{q_idx}"
                )
            
            # 4. Yes/No questions (new)
            st.markdown("---")
            for q_idx, question in enumerate(PART2_AUDIO2_YESNO_QUESTIONS):
                # Use radio buttons for Yes/No
                current_value = current_episode['audio2_yesno_answers'][q_idx]
                if current_value is None:
                    current_value = "No response"
                
                response = st.radio(
                    question.format(dream_word=dream_word),  # Replace {dream_word}
                    options=["Oui", "Non", "Pas de response"],
                    index=["Yes", "No", "No response"].index(current_value) if current_value in ["Yes", "No", "No response"] else 2,
                    key=f"audio2_yesno_{current_index}_q{q_idx}",
                    horizontal=True
                )
                
                # Save the response (convert "No response" to None)
                current_episode['audio2_yesno_answers'][q_idx] = response if response != "No response" else None
        
        st.markdown("---")
    
    # ============================================
    # NAVIGATION BUTTONS
    # ============================================
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Previous button
        if current_index > 0:
            if st.button("⬅️ Épisode précédent", use_container_width=True):
                st.session_state.participant_episode_index -= 1
                st.rerun()
    
    with col2:
        # Next or Finish button
        if current_index < len(active_episodes) - 1:
            if st.button("➡️ Prochain épisode", type="primary", use_container_width=True):
                st.session_state.participant_episode_index += 1
                st.rerun()
        else:
            if st.button("✅ Terminer le questionnaire", type="primary", use_container_width=True):
                # Save all data to CSV
                try:
                    csv_path = save_all_data(
                        participant_id, 
                        st.session_state.experiment_type, 
                        st.session_state.episodes
                    )
                    st.session_state.survey_completed = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving data: {str(e)}")
    
    # ============================================
    # COMPLETION MESSAGE
    # ============================================
    
    if st.session_state.survey_completed:
        st.success("✅ Questionnaire terminé avec succès !")
        st.info("Merci de votre participation. Vous pouvez désormais fermer cette fenêtre.")
        
        # Show path to saved data
        if st.session_state.participant_id:
            csv_path = get_participant_csv_path(st.session_state.participant_id)
            st.caption(f"Data saved to: {csv_path}")
