import streamlit as st
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from ui.components.history.chat_list_item import ChatListItem
from ui.components.history.chat_editor import ChatEditor
from backend.services.chat_service import ChatService

class UserChatsHistory:
    def __init__(self):
        self.chat_service: ChatService = SessionStateService().get_or_create_chat_service()

        # Initialize state for editing chat title
        if "editing_chat_id" not in st.session_state:
            SessionStateService().set(SessionConfig.EDITING_CHAT_ID, None)

    def display(self):
        user_id = SessionStateService().get(SessionConfig.USER_ID)
        user_chats = self.chat_service.get_user_chats(user_id)
        
        if not user_chats:
            st.info("You currently have no created chats.")
            return
            
        for chat in user_chats:
            if SessionStateService().get(SessionConfig.EDITING_CHAT_ID) == chat.id:
                result = ChatEditor().display(chat)
                self._handle_editor_result(result)
            else:
                result = ChatListItem().display(chat)
                self._handle_list_item_result(result, chat.id)
    
    def _handle_editor_result(self, result):
        if result in ["save", "cancel"]:
            SessionStateService().set(SessionConfig.EDITING_CHAT_ID, None)
            st.rerun()
    
    def _handle_list_item_result(self, result, chat_id):
        if result == "edit":
            SessionStateService().set(SessionConfig.EDITING_CHAT_ID, chat_id)
            st.rerun()
        elif result == "delete":
            st.rerun()