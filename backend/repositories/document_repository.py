from typing import List, Optional
from backend.clients.postgres_client import PostgresClient
from backend.models.chunk import Chunk
from backend.models.document import Document
from utils.logger import log_info, log_error

class DocumentRepository:
    def __init__(self, postgres_client: PostgresClient):
        self.postgres_client = postgres_client
    
    def add_document(self, name: str, content_type: str, collection_name: str, chroma_chunks: List[Chunk], 
                       user_id: str, chat_id: int = None) -> Document:
        session = self.postgres_client.Session()
        try:
            document = Document(
                name=name,
                content_type=content_type,
                collection_name=collection_name,
                chunks=chroma_chunks,
                chat_id=chat_id,
                user_id=user_id
            )
            
            session.add(document)
            session.commit()
            
            if chat_id:
                _ = document.chat
                log_info(f"Document created with ID {document.id} for chat {chat_id}, user {user_id}")
            else:
                log_info(f"Document created with ID {document.id} for user {user_id}")
            return document.id
        except Exception as e:
            log_error(f"Error creating document {name}", str(e))
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        session = self.postgres_client.Session()
        try:
            return session.get(Document, document_id)
        finally:
            session.close()
    
    def get_documents_by_chat(self, chat_id: int) -> List[Document]:
        session = self.postgres_client.Session()
        try:
            return session.query(Document).filter(
                Document.chat_id == chat_id
            ).order_by(Document.created_at.desc()).all()
        finally:
            session.close()

    def get_documents_by_user(self, user_id: int) -> List[Document]:
        session = self.postgres_client.Session()
        try:
            return session.query(Document).filter(
                Document.user_id == user_id
            ).order_by(Document.created_at.desc()).all()
        finally:
            session.close() 

    def get_document_chunks(self, document_id: int) -> List[Chunk]:
        session = self.postgres_client.Session()
        try:
            return session.query(Chunk).filter(
                Chunk.document_id == document_id
            ).all() 
        finally:
            session.close()

    def attach_document_to_chat(self, chat_id: int, document_id: int) -> bool:
        session = self.postgres_client.Session()
        try:
            document = session.get(Document, document_id)
            if document:
                document.chat_id = chat_id
                session.commit()
                log_info(f"Document {document_id} attached to chat {chat_id}")
                return True
            log_info(f"Document with ID {document_id} not found")
            return False
        except Exception as e:
            log_error(f"Error attaching document to chat {chat_id}: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def delete_document(self, document_id: int) -> bool:
        session = self.postgres_client.Session()
        try:
            document = session.get(Document, document_id)
            if document:
                session.delete(document)
                session.commit()
                log_info(f"Document {document_id} deleted")
                return True
            return False
        except Exception as e:
            log_error(f"Error deleting document: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()
