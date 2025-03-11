
from typing import List
from backend.facades.library_facade import LibraryFacade
from backend.services.rag.collections_service import CollectionsService
from ui.components.library.delete_document_button import DeleteDocumentButton
from ui.components.library.document_chunks_viewer import DocumentChunksViewer
from ui.components.library.documents_table import DocumentsTable
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from utils.logger import log_error
import streamlit as st

class LibraryDocumentsViewer:
    def __init__(self, collection_name: str, model_name: str = None):
        self.library_facade: LibraryFacade = SessionStateService().get(SessionConfig.LIBRARY_FACADE)
        self.collection_name = collection_name
        self.model_name = model_name
        
    def display(self):
        """Display all documents for a specific chat"""
        try:
            selected_doc_id = DocumentsTable(self.library_facade).display()

            if selected_doc_id:
                chunk_ids = self.library_facade.get_document_chunk_ids(selected_doc_id)
                DeleteDocumentButton(selected_doc_id, self.library_facade, self.collection_name).display()
                DocumentChunksViewer(chunk_ids, self.collection_name, model_name=self.model_name).display()

        except Exception as e:
            log_error(f"Error displaying documents", str(e))
            st.error("An error occurred while displaying documents")