import streamlit as st
from ui.components.chat.message_manager import MessageManager

class MessageHistory:

    def add_user_message(self, prompt):
        st.chat_message("user").markdown(prompt)
        MessageManager().add_message(prompt, "user")

    def add_assistant_message(self, content):
        MessageManager().add_message(content, "assistant")
