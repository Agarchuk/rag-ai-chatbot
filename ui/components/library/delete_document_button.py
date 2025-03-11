import streamlit as st

from backend.facades.library_facade import LibraryFacade

class DeleteDocumentButton:
    def __init__(self, document_id: str, library_facade: LibraryFacade, collection_name: str):
        self.document_id = document_id
        self.library_facade = library_facade
        self.collection_name = collection_name

    def display(self):
        if st.button("Delete Document", key=f"delete_document_{self.document_id}"):
            self.library_facade.delete_document(self.document_id, self.collection_name)
            st.success("Document deleted successfully")
            st.rerun()
