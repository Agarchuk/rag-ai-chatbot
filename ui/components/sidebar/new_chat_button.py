import streamlit as st
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService

class NewChatButton:

    def display(self):
        with st.sidebar:
            if st.sidebar.button("➕ New Chat", use_container_width=True):
                SessionStateService().set(SessionConfig.CHAT_ID, None)
                SessionStateService().set(SessionConfig.CHAT_TITLE, "New AI Chat")
                st.rerun()  
