import streamlit as st
from ui.components.chat.message_manager import MessageManager

class ChatHistory:
    def display(self):
        messages = MessageManager().get_chat_messages()
        
        for message in messages:
            with st.chat_message(message.role):
                st.markdown(message.content)
