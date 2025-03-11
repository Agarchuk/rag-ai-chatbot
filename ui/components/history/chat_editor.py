from turtle import width
import streamlit as st
from backend.facades.chat_facade import ChatFacade
from backend.models.chat import Chat
from ui.utils.session_state_service import SessionStateService

class ChatEditor:
    def __init__(self):
        self.chat_facade: ChatFacade = SessionStateService().get_or_create_chat_facade()
    
    def display(self, chat: Chat):
        with st.form(key=f"edit_chat_form_{chat.id}"):
            columns = st.columns([4, 1, 1])
            
            with columns[0]:
                new_title = st.text_input("New Title", value=chat.title, key=f"new_title_{chat.id}")
            with columns[1]:
                save_button = st.form_submit_button("💾", help="Save")
            with columns[2]:
                cancel_button = st.form_submit_button("❌", help="Cancel")
            
            if save_button and new_title:
                return self._handle_save(chat.id, new_title)
            
            if cancel_button:
                return self._handle_cancel()
                
        return None
    
    def _handle_save(self, chat_id, new_title):
        if self.chat_facade.update_chat_title(chat_id, new_title):
            st.success(f"Chat title updated to '{new_title}'")
            return "save"
        else:
            st.error("Failed to update chat title")
            return None
            
    def _handle_cancel(self):
        return "cancel" 