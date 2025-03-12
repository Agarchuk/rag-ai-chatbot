import streamlit as st
from ui.components.chat.assistant_response import AssistantResponse
from ui.components.chat.message_history import MessageHistory
from ui.components.sidebar.model_settings import ModelSettingsUI
from ui.utils.session_state_service import SessionStateService
from utils.logger import log_info

class UserInput:
    def display(self):
        prompt = self.get_user_input()
        if prompt:
            self.process_user_input(prompt)

    def get_user_input(self):
        return st.chat_input("What would you like to ask?")

    def process_user_input(self, prompt):
        model_settings = SessionStateService().get_model_settings()
        log_info(f"Model settings: {model_settings}")
        key_exists = ModelSettingsUI().check_api_keys_exist(model_settings.model_data.model_type) 
        if not key_exists:
            st.error("Please enter your API keys in the model settings.")
            return

        MessageHistory().add_system_message()
        MessageHistory().add_user_message(prompt)
        full_response = AssistantResponse().stream_response()
        MessageHistory().add_assistant_message(full_response)
        st.rerun()
