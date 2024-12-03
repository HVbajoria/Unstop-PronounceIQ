import streamlit as st
from pages.welcome import show_welcome_page
from pages.assessment import show_assessment_page
from pages.history import show_history_page
from pages.report import show_report_page
from components.navigation import create_navigation

st.set_page_config(
    page_title="PronounceIQ",
    page_icon="🗣️",
    layout="wide"
)

# Hide the default menu and footer
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'recordings' not in st.session_state:
    st.session_state.recordings = []

# st.session_state.page = 'welcome'
# Create the navigation bar
create_navigation()

# Page routing
if st.session_state.page == 'welcome':
    show_welcome_page()
elif st.session_state.page == 'assessment':
    show_assessment_page()
elif st.session_state.page == 'history':
    show_history_page()
elif st.session_state.page == 'report':
    show_report_page()