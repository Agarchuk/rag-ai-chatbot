import os
import streamlit as st
from config.models import MODEL_OPTIONS
from dtos.model_data import ModelData
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig
from utils.logger import log_info

class ModelSettingsUI:    
    def __init__(self):
        self.available_models = self._get_available_models()
        self.model_settings = SessionStateService().get_model_settings() 
    
    def _get_available_models(self):
        return [ModelData(model_type, model_name) 
                for model_type in MODEL_OPTIONS 
                for model_name in MODEL_OPTIONS[model_type]]

    def display(self):
        with st.sidebar.expander("⚙️ Model Settings", expanded=False):
            self._select_model()
            self._handle_api_keys()
            self._set_temperature()
            self._set_max_tokens()
            self._set_advanced_settings()

        log_info(f"Model settings after display: {self.model_settings}")
        SessionStateService().set_model_settings(self.model_settings)
        return self.model_settings

    def check_api_keys_exist(self, model_type):
        if model_type == 'openai':
            openai_key_exists = SessionStateService().get(SessionConfig.OPENAI_API_KEY) is not None
            log_info(f"OpenAI key exists: {openai_key_exists}")
            return openai_key_exists
        elif model_type == 'huggingface':
            hf_key_exists = SessionStateService().get(SessionConfig.HF_API_KEY) is not None
            log_info(f"HuggingFace key exists: {hf_key_exists}")
            return hf_key_exists
        return False

    def _select_model(self):
        self.model_settings.model_data = st.selectbox(
            "Select Model",
            self.available_models,
            index=0,
            format_func=lambda model: model.model_name
        )

    def _handle_api_keys(self):
        if self.model_settings.model_data.model_type == 'openai':
            self._handle_openai_api_key()
        elif self.model_settings.model_data.model_type == 'huggingface':
            self._handle_huggingface_api_key()

    def _handle_openai_api_key(self):
        api_key = st.text_input("OpenAI API Key", type="password", help="Your API key will be stored in session")
        if st.button("Save OpenAI API Key") and self._is_valid_api_key(api_key, 'sk-'):
            self._save_api_key_to_session(SessionConfig.OPENAI_API_KEY, api_key)

    def _handle_huggingface_api_key(self):
        hf_api_key = st.text_input(
            "HuggingFace Token", 
            type="password",
            value=SessionStateService().get(SessionConfig.HF_API_KEY, ""),
            help="Required for private models"
        )
        if st.button("Save HuggingFace API Key") and self._is_valid_api_key(hf_api_key, 'hf_'):
            self._save_api_key_to_session(SessionConfig.HF_API_KEY, hf_api_key)

    def _is_valid_api_key(self, api_key, prefix):
        if api_key and api_key.startswith(prefix):
            return True
        st.error("Invalid API key format. Please check your API key.")
        return False
    
    def _save_api_key_to_session(self, key_name, api_key):
        SessionStateService().set(key_name, api_key)
        os.environ[key_name] = api_key
        st.success("API key configured successfully!")

    def _set_temperature(self):
        self.model_settings.temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=1.0, 
            value=self.model_settings.temperature, 
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )

    def _set_max_tokens(self):
        self.model_settings.max_tokens = st.number_input(
            "Max Tokens", 
            min_value=100, 
            max_value=4000, 
            value=self.model_settings.max_tokens,
            step=100,
            help="Maximum length of generated response"
        )

    def _set_advanced_settings(self):
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
