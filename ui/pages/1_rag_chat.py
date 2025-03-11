from backend.facades.library_facade import LibraryFacade
from ui.components.chat.chat_history import ChatHistory
from ui.components.chat.user_input import UserInput
from ui.components.chat.rag.rag_chat_sidebar import RagChatSidebar
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig
import streamlit as st

if __name__ == "__page__":
    title = SessionStateService().get(SessionConfig.CHAT_TITLE) or "AI Chat"
    st.title(title)
    
    RagChatSidebar().display() 
    ChatHistory().display()
    UserInput().display()
