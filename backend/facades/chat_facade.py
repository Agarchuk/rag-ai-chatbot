from typing import List, Optional, Dict, Any
from backend.models.chat import Chat
from backend.models.document import Document
from backend.models.message import Message
from backend.services.assistant_service import AssistantService
from backend.services.chat_service import ChatService
from backend.services.documents_service import DocumentsService
from backend.services.models.base_model import BaseAIModel
from dtos.assistant_response_dto import AssistantResponseDto
from utils.logger import log_info, log_error

class ChatFacade:
    def __init__(self, assistant_service: AssistantService, chat_service: ChatService, documents_service: DocumentsService):
        """Initialize the chat facade."""
        self.chat_service: ChatService = chat_service
        self.assistant_service: AssistantService = assistant_service  
        self.document_service: DocumentsService = documents_service

    def get_user_chat_history(self, chat_id: int) -> List[Message]:
        return self.chat_service.get_user_chat_history(chat_id)
    
    def get_assistant_response(self, model_service: BaseAIModel, messages: List[Message], 
                               chat_id: int) -> AssistantResponseDto:
        return self.assistant_service.get_assistant_response(model_service, messages, 
                                                            chat_id)
    
    
    def get_documents_for_chat(self, chat_id: int) -> List[Document]:
        if chat_id is None:
            return []
        return self.document_service.get_documents_for_chat(chat_id)
    
    
    def update_chat_title(self, chat_id: int, new_title: str) -> bool:
        return self.chat_service.update_chat_title(chat_id, new_title)

