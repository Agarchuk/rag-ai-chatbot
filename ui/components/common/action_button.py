import streamlit as st

class ActionButton:
    def __init__(self):
        pass
        
    def display(self, label, key, help_text=None, use_container_width=False):
        return st.button(
            label, 
            key=key, 
            help=help_text,
            use_container_width=use_container_width
        ) 