from backend.services.chat_service import ChatService
from backend.repositories.message_repository import MessageRepository
from utils.logger import log_info
from backend.mapper.message_mapper import MessageMapper
from dtos.message_dto import MessageDTO


class MessageService:
    def __init__(self, message_repository: MessageRepository, chat_service: ChatService, message_mapper: MessageMapper):
        """Initialize the chat service"""
        self.message_repository = message_repository
        self.chat_service = chat_service
        self.message_mapper = message_mapper
    
    def add_message(self, message_dto: MessageDTO) -> MessageDTO:
        message = self.message_mapper.map_message_dto_to_message(message_dto)
        
        if message.chat_id is None:
            chat_id = self.chat_service.create_chat(user_id=message_dto.user_id, messages=[message]).id
            message.chat_id = chat_id

        updated_message = self.message_repository.add_message(message)
        return updated_message
    
    def get_user_chat_history(self, chat_id: int = None) -> list:
        messages = self.message_repository.get_user_chat_history(chat_id)
        return [self.message_mapper.map_message_model_to_dto(message) for message in messages]