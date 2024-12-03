import streamlit as st

def create_navigation():
    # Create three columns for layout
    logo_col, title_col, nav_col = st.columns([1, 2, 1])
    
    with logo_col:
        st.image("https://d8it4huxumps7.cloudfront.net/uploads/images/unstop/branding-guidelines/logos/white/Unstop-Logo-White-Small.png", width=100)  # Replace with actual logo
        
    with title_col:
        st.markdown("<h3 style='text-align: center;'>Unstop PronounceIQ</h3>", unsafe_allow_html=True)
        
    with nav_col:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Home"):
                st.session_state.page = 'welcome'
                
        with col2:
            if st.button("History"):
                st.session_state.page = 'history'
                
        with col3:
            if st.button("Report"):
                st.session_state.page = 'report'
                
    st.markdown("<hr>", unsafe_allow_html=True)