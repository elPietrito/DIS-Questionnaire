# app.py
# ============================================
# MAIN APPLICATION ENTRY POINT
# Routes between experimenter and participant interfaces
# ============================================

import streamlit as st
from state_manager import initialize_session_state
from experimenter_page import render_experimenter_page
from participant_page import render_participant_page

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Audio Survey Application",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# INITIALIZE SESSION STATE
# ============================================

initialize_session_state()

# ============================================
# ROUTE BASED ON URL PARAMETER
# ============================================

def main():
    """
    Main application logic.
    Routes to either experimenter or participant interface based on URL parameter.
    """
    
    # Check for participant parameter in URL
    query_params = st.query_params
    participant_id = query_params.get("participant", None)
    
    # ============================================
    # LOCAL DEBRIEF MODE (Experimenter clicks "Start Debrief")
    # ============================================
    
    if st.session_state.get('show_local_debrief', False):
        # Show Part 2 on the same computer
        render_participant_page(st.session_state.participant_id)
        return
    
    # ============================================
    # PARTICIPANT MODE (URL has ?participant=ID)
    # ============================================
    
    if participant_id:
        render_participant_page(participant_id)
    
    # ============================================
    # EXPERIMENTER MODE (Default, no URL parameter)
    # ============================================
    
    else:
        render_experimenter_page()


# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    main()
