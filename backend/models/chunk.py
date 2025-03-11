from sqlalchemy import Column, Integer, ForeignKey, String
from backend.clients.postgres_client import Base
from sqlalchemy.orm import relationship

class Chunk(Base):
    __tablename__ = 'chunks'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    chroma_chunk_id = Column(String, nullable=False)

    document = relationship("Document", back_populates="chunks")

    def __repr__(self):
        return f"Chunk(id={self.id}, chroma_chunk_id={self.chroma_chunk_id})"