from ui.components.history.user_chats_history import UserChatsHistory
import streamlit as st

if __name__ == "__page__":
    st.title("Chat History")

    UserChatsHistory().display()

