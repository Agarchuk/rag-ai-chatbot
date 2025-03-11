import os
import uuid
from typing import List, Optional

from backend.repositories.document_repository import DocumentRepository
from backend.models.document import Document
from backend.services.rag.collections_service import CollectionsService
from backend.services.rag.metadata_service import MetadataService
from utils.logger import log_info, log_error

from backend.factories.loader_factory import DocumentLoaderFactory
from backend.services.rag.chunks_service import ChunksService
from langchain_core.documents import Document as LangchainDocument
from backend.models.chunk import Chunk

class DocumentsService:
    
    def __init__(self, document_repository: DocumentRepository, 
                 loader_factory: DocumentLoaderFactory,
                 chunk_service: ChunksService,
                 metadata_service: MetadataService,
                 collections_service: CollectionsService):
        self.document_repository = document_repository
        self.loader_factory = loader_factory
        self.chunk_service = chunk_service
        self.metadata_service = metadata_service
        self.collections_service = collections_service

    def add_document_to_collection(self, collection_name: str, 
                                    chunks: List[LangchainDocument], 
                                    document_name: str) -> List[str]:
        chroma_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            metadata = self.metadata_service.prepare_metadata(chunk, chunk_id, document_name, i, len(chunks))
            chroma_chunk_id = self.collections_service.add_collection_chunk(
                collection_name,
                chunk_id=chunk_id,
                chunk_text=chunk.page_content,
                metadata=metadata
            )
            chunk = Chunk(
                chroma_chunk_id=chroma_chunk_id
            )       
            chroma_chunks.append(chunk)
        return chroma_chunks

    def add_document_to_postgres(self, name: str, chroma_chunks: List[Chunk], user_id: str, collection_name: str, chat_id: int = None) -> Document:
        content_type = self._get_content_type(name)

        return self.document_repository.add_document(
            name=name,
            content_type=content_type,
            collection_name=collection_name,
            chroma_chunks = chroma_chunks,
            user_id=user_id,
            chat_id=chat_id,
        )
    
    def get_documents_for_chat(self, chat_id: int) -> List[Document]:
        return self.document_repository.get_documents_by_chat(chat_id)
    
    def get_documents_by_user(self, user_id: int) -> List[Document]:
        return self.document_repository.get_documents_by_user(user_id)
    
    def get_document_chunk_ids(self, document_id: int) -> List[str]:
        chunks = self.document_repository.get_document_chunks(document_id)
        return [chunk.chroma_chunk_id for chunk in chunks]
    
    def attach_document_to_chat(self, chat_id: int, document_id: int) -> bool:
        return self.document_repository.attach_document_to_chat(chat_id, document_id)
    
    def delete_document(self, document_id: int, collection_name: str) -> bool:
        try:
            document = self.document_repository.get_document_by_id(document_id)
            if not document:
                return False
            
            self.collections_service.delete_collection(collection_name)
            return self.document_repository.delete_document(document_id)
        except Exception as e:
            log_error(f"Error deleting document: {document_id}", str(e))
            return False

    def _get_content_type(self, file_name: str) -> str:
        extension = os.path.splitext(file_name.lower())[1]
        content_types = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.htm': 'text/html'
        }
        return content_types.get(extension, 'application/octet-stream')