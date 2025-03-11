from backend.models.message import Message 
from dtos.message_dto import MessageDTO

class MessageMapper:
    
    @staticmethod
    def map_message_model_to_dto(message_model: Message) -> MessageDTO:
        """Maps MessageModel to MessageDTO."""
        return MessageDTO(id=message_model.id, content=message_model.content, role=message_model.role, chat_id=message_model.chat_id)
    
    @staticmethod
    def map_message_dto_to_message(message_dto: MessageDTO) -> Message:
        """Maps MessageDTO to MessageModel."""
        return Message(id=message_dto.id, content=message_dto.content, role=message_dto.role, chat_id=message_dto.chat_id)

    @staticmethod
    def map_message_dto_to_langchain_message(message_dto: MessageDTO) -> dict:
        """Maps MessageDTO to LangchainMessage."""
        return {
            "role": message_dto.role,
            "content": message_dto.content
        }