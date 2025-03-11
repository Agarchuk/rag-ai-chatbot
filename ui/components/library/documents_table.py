import streamlit as st
import pandas as pd

from backend.facades.library_facade import LibraryFacade
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from utils.logger import log_info

class DocumentsTable:
    def __init__(self, library_facade: LibraryFacade):
        self.library_facade = library_facade

    def display(self):
        user_id = SessionStateService().get(SessionConfig.USER_ID)
        documents = self.library_facade.get_all_user_documents(user_id)

        if documents:
            pandas_df = pd.DataFrame([doc.to_dict() for doc in documents])
            st.title("Documents")
            selected_row = st.dataframe(
                pandas_df,
                key="data",
                on_select="rerun",
                selection_mode="single-row"
            )

            selected_indices = selected_row.get("selection", {}).get("rows", [])
            if selected_indices:
                selected_index = selected_indices[0]
                selected_doc_id = pandas_df.iloc[selected_index]['id']
                return selected_doc_id
            else:
                st.write("Select a document from the table above to view details")
                return None
