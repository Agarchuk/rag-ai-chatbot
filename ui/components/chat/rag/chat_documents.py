import streamlit as st
from backend.facades.chat_facade import ChatFacade
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from utils.logger import log_error

class ChatDocuments:    
    def __init__(self):
        self.chat_facade: ChatFacade = SessionStateService().get_or_create_chat_facade()
    
    def display(self):
        chat_id = SessionStateService().get(SessionConfig.CHAT_ID)
        user_id = SessionStateService().get(SessionConfig.USER_ID)

        with st.sidebar.expander("📚 Documents", expanded=True):
            if not chat_id:
                st.info("No documents in this chat. Upload a document to get started.")
                return
            
            st.write("### Documents for this chat")
            self._display_documents(chat_id, user_id)
    
    def _display_documents(self, chat_id: str, user_id: str):
        try:
            documents = self.chat_facade.get_documents_for_chat(chat_id=chat_id)
            
            if not documents:
                st.info("No documents in this chat. Upload a document to get started.")
                return
            
            for doc in documents:
                st.write(f"{doc.name}")
        
        except Exception as e:
            log_error(f"Error displaying documents, chat_id: {chat_id}, user_id: {user_id}", str(e))
            st.error("Failed to load documents.")
    