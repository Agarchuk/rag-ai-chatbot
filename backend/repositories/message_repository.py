from backend.clients.postgres_client import PostgresClient
from backend.models.message import Message
from utils.logger import log_info

class MessageRepository:
    def __init__(self, postgres_client: PostgresClient):
        self.postgres_client = postgres_client
        
    def add_message(self, message: Message) -> Message:
        """Adds a message to the database."""
        session = self.postgres_client.Session()
        try:
            session.add(message)
            session.commit()
            session.refresh(message)  # Ensure the message is bound to the session
            return message
        finally:
            session.close()

    def get_user_chat_history(self, chat_id: int = None) -> list:
        """Gets the chat history for a user."""
        session = self.postgres_client.Session()
        try:
            messages = session.query(Message).filter(Message.chat_id == chat_id).order_by(Message.id).all()
            return messages
        finally:
            session.close()