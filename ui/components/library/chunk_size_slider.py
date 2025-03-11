import streamlit as st

from ui.utils.session_state_service import SessionStateService

class ChunkSizeSlider:
    def display(self):
        """Display model settings in an expander in the sidebar."""

        chunk_size = st.sidebar.slider(
            "Chunk size", 
            min_value=50, 
            max_value=2000, 
            value=100, 
            step=50
        )
           
        SessionStateService().set_chunk_size(chunk_size)
