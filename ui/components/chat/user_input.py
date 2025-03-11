import streamlit as st
from ui.components.chat.assistant_response import AssistantResponse
from ui.components.chat.message_history import MessageHistory

class UserInput:
    def display(self):
        prompt = self.get_user_input()
        if prompt:
            self.process_user_input(prompt)

    def get_user_input(self):
        return st.chat_input("What would you like to ask?")

    def process_user_input(self, prompt):
        MessageHistory().add_user_message(prompt)
        full_response = AssistantResponse().stream_response()
        MessageHistory().add_assistant_message(full_response)
