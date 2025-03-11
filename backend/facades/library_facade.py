import os
from typing import BinaryIO
from backend.models.document import Document
from backend.services.chat_service import ChatService
from backend.services.documents_service import DocumentsService
from backend.services.rag.chunks_service import ChunksService
from backend.factories.loader_factory import DocumentLoaderFactory
from utils.logger import log_error, log_info
from utils.file_helper import FileHelper
from typing import List

class LibraryFacade:
    def __init__(self, 
                 loader_factory: DocumentLoaderFactory, 
                 document_service: DocumentsService,
                 chat_service: ChatService,
                 chunk_service: ChunksService):
        self.loader_factory = loader_factory
        self.document_service = document_service  
        self.chat_service = chat_service   
        self.chunk_service = chunk_service

    def add_document_to_library(self, uploaded_file: BinaryIO, user_id: str, 
                                collection_name: str, 
                                chunk_size: int = 1000, 
                                percentage_overlap: float = 0.15,
                                chat_id: int = None) -> int:
        
        file_name = uploaded_file.name
        loader = self.loader_factory.get_loader(file_name)

        if not loader:
            log_error(f"No loader found for document: {file_name}", "Invalid file format")
            return None
        
        file_content = FileHelper().get_file_content(uploaded_file)

        temp_file_path = FileHelper().create_temp_file(file_content)
        try:
            documents = loader.load(temp_file_path)

            chunks = self.chunk_service.chunk(documents, chunk_size=chunk_size, percentage_overlap=percentage_overlap)     
            chroma_chunks = self.document_service.add_document_to_collection(collection_name, chunks, file_name)
            return self.document_service.add_document_to_postgres(file_name, chroma_chunks, user_id, collection_name, chat_id)
        finally:
            os.unlink(temp_file_path)

    def get_all_user_documents(self, user_id: str) -> List[Document]:
        return self.document_service.get_documents_by_user(user_id) 
    
    def get_document_chunk_ids(self, document_id: int) -> List[str]:
        return self.document_service.get_document_chunk_ids(document_id)
    
    def attach_document_to_chat(self, user_id: str, chat_id: int, document_id: int) -> int:
        log_info(f"Attaching document {document_id} to chat {chat_id}")
        if chat_id is None:
            chat = self.chat_service.create_chat(user_id)
            chat_id = chat.id
        
        self.document_service.attach_document_to_chat(chat_id, document_id)
        return chat_id
    
    def delete_document(self, document_id: int, collection_name: str):
        return self.document_service.delete_document(document_id, collection_name)
