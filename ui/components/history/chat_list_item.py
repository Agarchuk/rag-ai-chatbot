import streamlit as st
from backend.services.chat_service import ChatService
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from ui.components.common.action_button import ActionButton

class ChatListItem:
    def __init__(self):
        self.chat_service: ChatService = SessionStateService().get_or_create_chat_service()
        
    def display(self, chat):
        col1, col2, col3 = st.columns([8, 1, 1])
        with col1:
            if ActionButton().display(chat.title, key=f"chat_button_{chat.id}", use_container_width=True): 
                return self._handle_chat_selection(chat)
        with col2:
            if ActionButton().display("✏️", key=f"edit_button_{chat.id}", help_text="Edit title"):
                return "edit"
        with col3:
            if ActionButton().display("🗑️", key=f"delete_button_{chat.id}", help_text="Delete chat"):
                return self._handle_delete_chat(chat)
        
        return None
        
    def _handle_chat_selection(self, chat):
        SessionStateService().set(SessionConfig.CHAT_ID, chat.id) 
        SessionStateService().set(SessionConfig.CHAT_TITLE, chat.title)
        st.switch_page("ui/pages/1_rag_chat.py")
        return "select"
        
    def _handle_delete_chat(self, chat):
        user_id = SessionStateService().get(SessionConfig.USER_ID)
        if self.chat_service.delete_chat(chat.id, user_id):
            st.success(f"Chat '{chat.title}' deleted successfully!")
            SessionStateService().set(SessionConfig.CHAT_ID, None)
            SessionStateService().set(SessionConfig.CHAT_TITLE, None)
            return "delete"
        else:
            st.error("Failed to delete chat.")
            return None 