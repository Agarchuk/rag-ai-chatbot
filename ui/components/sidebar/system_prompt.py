import streamlit as st

from ui.components.chat.message_manager import MessageManager
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService

class SystemPrompt:

    def __init__(self):
        self.system_prompt = "You are a smart and friendly chatbot specializing in IT."

    def display(self):
        """Creates a sidebar section for system prompt configuration."""
        with st.sidebar:
            st.header("System Prompt")
            self.system_prompt = st.text_area(
                "System Prompt",
                value=self.system_prompt,
                help="Defines the basic behavior and role of the chatbot"
            )
            if st.button("Apply System Prompt"):
                SessionStateService().set(SessionConfig.SYSTEM_PROMPT, self.system_prompt)  
                st.success("System prompt applied successfully.")
    
    def get_prompt(self):
        return self.system_prompt 