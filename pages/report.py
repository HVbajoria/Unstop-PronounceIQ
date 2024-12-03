import streamlit as st

def show_report_page():
    st.subheader("Assessment Report")
    if 'results' not in st.session_state:
        st.info("No assessments found. Take an assessment first!")
        if st.button("Start New Assessment"):
            st.session_state.page = 'assessment'
            return
    else:
        # View report button
        if st.button("View Report"):
            st.session_state.page = 'report'
        # Display mock report data
        latest_result = st.session_state.results[-1]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Paragraph Pronunciation Score", f"{latest_result['Paragraph pronunciation score']:.2f}/100")
            st.metric("Accuracy Score", f"{latest_result['Accuracy Score']:.2f}/100")

        with col2:
            st.metric("Completeness Score", f"{latest_result['Completeness Score']:.2f}/100")
            st.metric("Fluency Score", f"{latest_result['Fluency Score']:.2f}/100")
            st.metric("Prosody Score", f"{latest_result['Prosody Score']:.2f}/100")

        # Detailed feedback
        st.subheader("Detailed Feedback")
        st.write("""
        - Excellent pronunciation and clarity
        - Good use of vocabulary
        - Natural flow of speech
        - Minor grammatical improvements needed
        """)
    
        if st.button("Back to History"):
            st.session_state.page = 'history'