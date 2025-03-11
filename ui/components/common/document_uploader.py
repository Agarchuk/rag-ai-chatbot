import streamlit as st

class DocumentUploader:
    def display(self, title=""):
        st.divider()
        uploaded_file = st.file_uploader(title, type=["pdf", "docx", "txt"])
        return uploaded_file

