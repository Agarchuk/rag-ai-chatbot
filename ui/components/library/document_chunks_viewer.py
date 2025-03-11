from typing import List
import streamlit as st

from backend.services.rag.collections_service import CollectionsService
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService

class DocumentChunksViewer:
    def __init__(self, chunk_ids: List[str], collection_name: str, model_name: str = None):
        self.chunk_ids = chunk_ids
        self.model_name = model_name
        self.collection_service: CollectionsService = SessionStateService().get_or_create_component(SessionConfig.COLLECTIONS_SERVICE, CollectionsService)
        self.collection_name = collection_name

    def display(self):
        """Display chunks of the selected document."""
        if self.chunk_ids:
            st.write(f"Document has been split into the following {len(self.chunk_ids)} chunks:")
            chunks = self.collection_service.get_chunks_by_ids(self.collection_name, self.chunk_ids)
            chunks_documents = chunks["documents"]

            for i, chunk_document in enumerate(chunks_documents):
                with st.expander(f"Chunk {i+1}", expanded=False):
                    st.write(chunk_document)
        else:
            st.write("No chunks available for this document.") 