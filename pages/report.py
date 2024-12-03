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
        import os
        import google.generativeai as genai

        data_string = (
            f"Paragraph Pronunciation Score: {latest_result['Paragraph pronunciation score']:.2f}/100\n"
            f"Accuracy Score: {latest_result['Accuracy Score']:.2f}/100\n"
            f"Completeness Score: {latest_result['Completeness Score']:.2f}/100\n"
            f"Fluency Score: {latest_result['Fluency Score']:.2f}/100\n"
            f"Prosody Score: {latest_result['Prosody Score']:.2f}/100"
        )

        genai.configure(api_key="AIzaSyAVXFiJ90NXQxcIDjM9rjbroL5tGUcgZgk")

        # Create the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            generation_config=generation_config,
            system_instruction="You are a pronunciation expert. You will be given scores for a paragraph's pronunciation performance in five categories: Accuracy, Completeness, Fluency, Prosody, and Overall Score. \n\n> Based on the scores, provide concise, actionable feedback in bullet point format using Markdown. The feedback should be specific, constructive, and focused on improvement. \n\nExample Input:\n- Paragraph Pronunciation Score: 0/100\n- Accuracy Score: 3/100\n- Completeness Score: 5/100\n- Fluency Score: 8/100\n- Prosody Score: 9/100\n\nExpected Output:\n\n- **Accuracy:** Good overall accuracy. Consider double-checking pronunciation of [specific words or sounds].\n- **Completeness:** Strong performance. Ensure all sounds are pronounced clearly.\n- **Fluency:** Smooth delivery. Work on pausing strategically for better emphasis.\n- **Prosody:** Room for improvement. Focus on intonation and stress to enhance natural speech patterns.\n- **Overall:** Good effort. Prioritize prosody and accuracy for significant improvement. \n",
        )

        chat_session = model.start_chat(
            history=[]
        )

        response = chat_session.send_message(data_string)

        print(response.text)

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
        st.markdown(response.text)
    
        if st.button("Back to History"):
            st.session_state.page = 'history'