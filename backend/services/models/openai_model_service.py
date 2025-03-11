from typing import List
from backend.services.models.base_model import BaseAIModel
from langchain_openai import ChatOpenAI
from streamlit import secrets
import os
from dtos.model_settings import ModelSettings
from utils.logger import log_info
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import streamlit as st

class OpenAIModelService(BaseAIModel):
    def __init__(self, model_settings: ModelSettings):
        self.model_settings = model_settings        

    def generate_response(self, messages: List[dict]):
        log_info(f"OpenAIModelService is generating response")
        api_key = self.get_api_key()
        if not api_key:
            return
        
        client = ChatOpenAI(
            api_key=api_key,
            model=self.model_settings.model_data.model_name,
            temperature=self.model_settings.temperature,
            streaming=True  
        )
        langchain_messages = self._convert_messages(messages)
        
        log_info(f"langchain_messages: {langchain_messages}")
        stream = client.stream(langchain_messages)
        
        for chunk in stream:
            yield chunk.content

    def _convert_messages(self, messages: List[dict]) -> List[any]:
        message_map = {
            "system": SystemMessage,
            "user": HumanMessage,
            "assistant": AIMessage
        }
        return [
            message_map[msg["role"]](content=msg["content"])
            for msg in messages
        ]
    
    def get_api_key(self):
        try:
            api_key = secrets["OPENAI_API_KEY"] or os.environ.get("OPENAI_API_KEY")
        except Exception:
            api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            st.warning("OpenAI API key is required. Please set it in Model Settings in sidebar.")
            api_key = None

        return api_key