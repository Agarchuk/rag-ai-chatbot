import streamlit as st
from ui.pages.login import LoginPage
from ui.utils.service_initializer import ServiceInitializer
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig

class App:
    def render(self):  
        session_token =  SessionStateService().get(SessionConfig.TOKEN_KEY, None) 

        if session_token is None:
            LoginPage().display()
        else:
            if not SessionStateService.has(SessionConfig.SERVICE_INITIALIZER):
                service_initializer = ServiceInitializer()
                SessionStateService.set(SessionConfig.SERVICE_INITIALIZER, service_initializer)
                service_initializer.initialize_app()
            
            pages = [
                st.Page("ui/pages/1_rag_chat.py", title="RAG Chat", icon=":material/book:"),
                st.Page("ui/pages/2_history.py", title="History", icon=":material/history:"),
                st.Page("ui/pages/3_chromadb_documents.py", title="ChromaDB Documents", icon=":material/database:"),
            ]
                    
            pg = st.navigation(pages)
            pg.run()
