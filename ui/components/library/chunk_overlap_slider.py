import streamlit as st

from ui.utils.session_state_service import SessionStateService

class ChunkOverlapSlider:
    def display(self):
        chunk_overlap = st.sidebar.slider(
            "Chunk overlap (%)", 
            min_value=0, 
            max_value=100, 
            value=15, 
            step=5
        ) / 100
           
        SessionStateService().set_chunk_overlap(chunk_overlap)
