import os
import streamlit as st
from config.models import MODEL_OPTIONS
from dtos.model_data import ModelData
from dtos.model_settings import ModelSettings
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig
from utils.logger import log_info

class ModelSettingsUI:    
    def __init__(self):
        self.available_models: list[ModelData] = [ModelData(model_type, model_name) for model_type in MODEL_OPTIONS.keys() for model_name in MODEL_OPTIONS[model_type]]
        self.model_settings: ModelSettings = SessionStateService().get_model_settings() 
    
    def display(self):
        with st.sidebar.expander("⚙️ Model Settings", expanded=False):
            # Model selection
            self.model_settings.model_data = st.selectbox(
                "Select Model",
                self.available_models,
                index=0,
                format_func=lambda model: model.model_name
            )  
            
            if self.model_settings.model_data.model_type == 'openai':
                api_key = st.text_input("OpenAI API Key", type="password", help="Your API key will be stored securely in the session")
                if st.button("Save API Key"):
                    if api_key:
                        if api_key.startswith('sk-') and len(api_key) > 40:  # Basic validation
                            # Ensure the directory exists before writing the file
                            os.makedirs('.streamlit', exist_ok=True)
                            with open('.streamlit/secrets.toml', 'w') as f:
                                f.write(f'OPENAI_API_KEY = "{api_key}"\n')
                            st.success("API key configured successfully!")
                            SessionStateService().set(SessionConfig.OPENAI_API_KEY, api_key)
                        else:
                            st.error("Invalid API key format. Please check your API key.")
            if self.model_settings.model_data.model_type == 'huggingface':
                hf_api_key = st.text_input(
                    "HuggingFace Token", 
                    type="password",
                    value=SessionStateService().get(SessionConfig.HF_API_KEY, ""),
                    help="Required for private models"
                )
                if st.button("Save API Key"):
                    if hf_api_key:
                        SessionStateService().set(SessionConfig.HF_API_KEY, hf_api_key)
                        if hf_api_key.startswith('hf_'):
                            os.makedirs('.streamlit', exist_ok=True)
                            with open('.streamlit/secrets.toml', 'w') as f:
                                f.write(f'HF_API_KEY = "{hf_api_key}"\n')
                            st.success("API key configured successfully!")
                        else:
                            st.error("Invalid API key format. Please check your API key.")

            # Temperature setting
            self.model_settings.temperature = st.slider(
                "Temperature", 
                min_value=0.0, 
                max_value=1.0, 
                value=self.model_settings.temperature, 
                step=0.1,
                help="Higher values make output more random, lower values more deterministic"
            )
            
            # Max length setting
            self.model_settings.max_tokens = st.number_input(
                "Max Tokens", 
                min_value=100, 
                max_value=4000, 
                value=self.model_settings.max_tokens,
                step=100,
                help="Maximum length of generated response"
            )
            
            # Additional settings if needed
            if st.checkbox("Advanced Settings", value=False):
                self.model_settings.top_p = st.slider(
                    "Top P", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=self.model_settings.top_p, 
                    step=0.05,
                    help="Alternative to temperature for nucleus sampling"
                )
                
                self.model_settings.frequency_penalty = st.slider(
                    "Frequency Penalty", 
                    min_value=0.0, 
                    max_value=2.0, 
                    value=self.model_settings.frequency_penalty, 
                    step=0.1,
                    help="Reduces repetition of tokens based on frequency"
                )

        log_info(f"Model settings after display: {self.model_settings}")
        
        SessionStateService().set_model_settings(self.model_settings)  # Save model settings to session state
        return self.model_settings
