import streamlit as st

from backend.facades.library_facade import LibraryFacade
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig

class AttachLibraryDocument:
    def __init__(self):
        self.library_facade: LibraryFacade = SessionStateService().get_or_create_library_facade()

    def display(self):
        user_id = SessionStateService().get(SessionConfig.USER_ID)
        chat_id = SessionStateService().get(SessionConfig.CHAT_ID)
        documents = self.library_facade.get_all_user_documents(user_id)

        selected_doc_id = st.sidebar.selectbox("Select a document to attach:", 
                                               options=[(document.name, document.id) for document in documents] if documents else [("No documents available", None)],
                                               format_func=lambda x: x[0])[1]

        if st.sidebar.button("Attach Document"):
            if selected_doc_id:
                chat_id = self.library_facade.attach_document_to_chat(user_id, chat_id, document_id=selected_doc_id)
                SessionStateService().set(SessionConfig.CHAT_ID, chat_id)
                st.sidebar.success("Document attached successfully!")
            else:
                st.sidebar.error("Please select a document to attach.")

        st.divider()
