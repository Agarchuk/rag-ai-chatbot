from typing import List, Optional
from backend.clients.postgres_client import PostgresClient
from backend.models.chat import Chat
from backend.models.message import Message
from utils.logger import log_error, log_info

class ChatRepository:
    def __init__(self, postgres_client: PostgresClient):
        self.postgres_client = postgres_client

    def create_chat(self, user_id: str, title: str = "New Chat", messages: List[Message] = []) -> Chat:
        """Creates a new chat with a title generated from the first message."""
        session = self.postgres_client.Session()
        try:
            chat = Chat(user_id=user_id, title=title, messages=messages)
            
            session.add(chat)
            session.commit()
            session.refresh(chat)
            
            log_info(f"Chat created with ID {chat.id} for user {user_id}")
            return chat
        finally:
            session.close()
    
    def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        session = self.postgres_client.Session()
        log_info(f"Getting chat by ID: {chat_id}")
        try:
            chat = session.get(Chat, chat_id)
            if chat:
                return Chat(id=chat.id, user_id=chat.user_id, title=chat.title, messages=chat.messages)
            return None
        finally:
            session.close()
    
    def get_chats_by_user(self, user_id: int) -> List[Chat]:
        session = self.postgres_client.Session()
        try:
            return session.query(Chat).filter(
                Chat.user_id == user_id
            ).order_by(Chat.updated_at.desc()).all()
        finally:
            session.close()


    def update_chat_title(self, chat_id: int, new_title: str) -> bool:
        session = self.postgres_client.Session()
        try:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                chat.title = new_title
                session.commit()
                log_info(f"Chat title updated for chat ID {chat_id}: '{new_title}'")
                return True
            log_info(f"Chat with ID {chat_id} not found for title update")
            return False
        except Exception as e:
            log_error(f"Error updating chat title for chat ID {chat_id}: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def delete_chat(self, chat_id: int) -> bool:
        session = self.postgres_client.Session()
        try:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                session.delete(chat)
                session.commit()
                log_info(f"Chat with ID {chat_id} deleted successfully")
                return True
            log_info(f"Chat with ID {chat_id} not found")
            return False 
        except Exception as e:
            log_error(f"Error deleting chat with ID {chat_id}", str(e))
            session.rollback()
            return False
        finally:
            session.close()
