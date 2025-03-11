import streamlit as st
from backend.facades.library_facade import LibraryFacade
from ui.components.common.document_uploader import DocumentUploader
from ui.components.library.chunk_overlap_slider import ChunkOverlapSlider
from ui.components.library.chunk_size_slider import ChunkSizeSlider
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from ui.components.library.library_documents_viewer import LibraryDocumentsViewer
from utils.logger import log_info

def get_collection_name(collection_name: str, model_name: str = None):
    if model_name is None:
        return collection_name
    model_suffix = model_name.replace("/", "_")
    return f"{collection_name}__{model_suffix}"

if __name__ == "__page__":
    st.title("ChromaDB Documents")
    st.write("View and manage your documents directly from ChromaDB")
    
    st.info("""
    This page shows documents as they are stored in ChromaDB (vector database).
    Documents are split into chunks for better retrieval during RAG operations.
    """)
    
    collection_name = "library_documents"
    model_name = "all-MiniLM-L6-v2"
    collection_name = get_collection_name(collection_name, model_name)
    SessionStateService().set(SessionConfig.COLLECTION_NAME, collection_name)


    library_facade: LibraryFacade = SessionStateService().get_or_create_library_facade()

    uploaded_file = DocumentUploader().display(title="Upload document into ChromaDB")
    user_id = SessionStateService().get_user_id()

    if uploaded_file is not None:
        
        ChunkSizeSlider().display()
        ChunkOverlapSlider().display()

        if st.button("Send to ChromaDB"):
            chunk_size = SessionStateService().get_chunk_size()
            chunk_overlap = SessionStateService().get_chunk_overlap()
            log_info(f"Chunk size: {chunk_size}, Chunk overlap: {chunk_overlap}")

            library_facade.add_document_to_library(uploaded_file, 
                                                   user_id, 
                                                   collection_name, 
                                                   chunk_size=chunk_size, 
                                                   percentage_overlap=chunk_overlap)

    LibraryDocumentsViewer(collection_name, model_name).display()
