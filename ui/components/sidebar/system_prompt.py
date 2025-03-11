import streamlit as st

class SystemPrompt:

    def __init__(self):
        self.system_prompt = "You are a smart and friendly chatbot specializing in IT."

    def display(self):
        """Creates a sidebar section for system prompt configuration."""
        with st.sidebar:
            st.header("System Prompt")
            self.system_prompt = st.text_area(
                "System Prompt",
                value=self.system_prompt,
                help="Defines the basic behavior and role of the chatbot"
            )
    
    def get_prompt(self):
        return self.system_prompt 