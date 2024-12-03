import streamlit as st
import pandas as pd

def show_history_page():
    st.subheader("Interview History")
    
    if not st.session_state.recordings:
        st.info("No recordings found. Take an assessment first!")
        if st.button("Start New Assessment"):
            st.session_state.page = 'assessment'
        return
    
    # Display recordings as a table
    df = pd.DataFrame(st.session_state.recordings)
    st.dataframe(df.style.set_properties(**{'width': '100%', 'height': 'auto'}))
    
    # View report button
    if st.button("View Report"):
        st.session_state.page = 'report'