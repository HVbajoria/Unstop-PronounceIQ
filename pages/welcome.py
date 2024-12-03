import streamlit as st

def show_welcome_page():
    st.subheader("Your AI-Powered Pronunciation Assessment Platform")
    
    # Language selection
    languages = ["Hindi", "English (Under progress)", "Spanish (Under progress)", "French (Under progress)", "German (Under progress)"]
    selected_language = st.selectbox(
        "Choose your preferred language",
        languages
    )
    
    # Start assessment button
    if st.button("Start Assessment", type="primary"):
        st.session_state.page = 'assessment'