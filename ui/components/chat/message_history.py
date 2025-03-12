import streamlit as st
from ui.components.chat.message_manager import MessageManager
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService

class MessageHistory:
    def add_system_message(self):
        system_prompt = SessionStateService().get(SessionConfig.SYSTEM_PROMPT, "")
        if system_prompt:
            MessageManager().add_message(system_prompt, "system")

    def add_user_message(self, prompt):
        st.chat_message("user").markdown(prompt)
        MessageManager().add_message(prompt, "user")

    def add_assistant_message(self, content):
        MessageManager().add_message(content, "assistant")
