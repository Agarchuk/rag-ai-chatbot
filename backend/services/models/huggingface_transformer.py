import os
from streamlit import secrets
from huggingface_hub import login
from backend.services.models.base_model import BaseAIModel
from dtos.model_settings import ModelSettings
from utils.logger import log_info
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
import threading


class HuggingFaceTransformer(BaseAIModel):
    def __init__(self, model_settings: ModelSettings):
        self.model_settings = model_settings

    def generate_response(self, messages):
        log_info(f"Generating response for messages: {messages}")
        api_key = self.get_api_key()
        if not api_key:
            return
        else:
            login(token=api_key)  
            tokenizer = AutoTokenizer.from_pretrained(self.model_settings.model_data.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_settings.model_data.model_name)
            streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)
        
            chat_history = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages
            ]
            
            formatted_input = tokenizer.apply_chat_template(
                chat_history,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = tokenizer(formatted_input, return_tensors="pt")
            
            thread = threading.Thread(
                target=model.generate,
                kwargs={
                    **inputs,
                    "max_new_tokens": 512,
                    "streamer": streamer,
                    "pad_token_id": tokenizer.eos_token_id,
                    "eos_token_id": tokenizer.eos_token_id,
                }
            )
            thread.start()

            for new_text in streamer:
                decoded_text = tokenizer.decode(tokenizer.encode(new_text), skip_special_tokens=True)
                yield decoded_text

    def get_api_key(self):
        log_info(f"HF_API_KEY: ")
        try:
            api_key = secrets["HF_API_KEY"] or os.environ.get("HF_API_KEY")
        except Exception:
            api_key = os.environ.get("HF_API_KEY")
        
        if not api_key:
            st.warning("Hugging Face API key is required. Please set it in Model Settings in sidebar.")
            api_key = None

        return api_key