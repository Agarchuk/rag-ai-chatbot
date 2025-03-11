from backend.services.message_service import MessageService
from dtos.message_dto import MessageDTO
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService

class MessageManager:
    def __init__(self):
        self.message_service: MessageService = SessionStateService().get_or_create_message_service()

    def get_chat_messages(self, chat_id=None) -> list[MessageDTO]:
        if chat_id is None:
            chat_id = SessionStateService().get(SessionConfig.CHAT_ID)
        return self.message_service.get_user_chat_history(chat_id)
    
    def add_message(self, content, role):
        chat_id = SessionStateService().get(SessionConfig.CHAT_ID)
        user_id = SessionStateService().get(SessionConfig.USER_ID)

        message_dto = MessageDTO(content=content, role=role, chat_id=chat_id, user_id=user_id)
        message_dto = self.message_service.add_message(message_dto)
        SessionStateService().set(SessionConfig.CHAT_ID, message_dto.chat_id)
        return message_dto
