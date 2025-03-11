from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from backend.clients.postgres_client import Base

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    collection_name = Column(String, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    
    chat = relationship("Chat", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "collection_name": self.collection_name,
            "chat_id": self.chat_id if self.chat_id else "",
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"Document(id={self.id}, name={self.name}, collection_name={self.collection_name}, chat_id={self.chat_id}, created_at={self.created_at})"