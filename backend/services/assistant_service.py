from backend.models.message import Message
from backend.services.models.base_model import BaseAIModel
from dtos.assistant_response_dto import AssistantResponseDto
from dtos.message_dto import MessageDTO
from dtos.relevant_context_dto import RelevantContextDto
from backend.mapper.message_mapper import MessageMapper
from backend.services.rag.collections_service import CollectionsService
from backend.services.documents_service import DocumentsService
from utils.logger import log_info

class AssistantService:
    def __init__(self, collections_service: CollectionsService, documents_service: DocumentsService):
        self.collections_service = collections_service
        self.documents_service = documents_service

    def get_assistant_response(self, model_service: BaseAIModel, messages: list[Message], 
                               chat_id: int) -> AssistantResponseDto:
        
        user_query = self._extract_user_query(messages)
        documents = self.documents_service.get_documents_for_chat(chat_id)
        chunk_ids_and_collection_name_by_document_id = {}
        for document in documents:
            document_id = document.id
            collection_name = document.collection_name
            chunk_ids = self.documents_service.get_document_chunk_ids(document_id)
            chunk_ids_and_collection_name_by_document_id[document_id] = {
                "collection_name": collection_name,
                "chunk_ids": chunk_ids
            }
        log_info(f"Chunk IDs and collection name by document ID: {chunk_ids_and_collection_name_by_document_id}")

        relevant_context_dto = RelevantContextDto(context="", chunk_data=[])

        if chunk_ids_and_collection_name_by_document_id:
            relevant_context_dto = self._get_relevant_context(user_query, 
                                                              chunk_ids_and_collection_name_by_document_id)
        
        if relevant_context_dto.context:
            self._update_or_create_system_message(messages, relevant_context_dto.context)

        langchain_messages = [MessageMapper.map_message_dto_to_langchain_message(message) for message in messages]
        log_info(f"Langchain messages: {langchain_messages}")
        log_info(f"Model service: {model_service}")
        response_chunks = model_service.generate_response(langchain_messages)  
        return AssistantResponseDto(response_chunks=response_chunks, chunk_data=relevant_context_dto.chunk_data)

    def _extract_user_query(self, messages: list[Message]) -> str:
        if not messages:
            return ""
        last_message = max(messages, key=lambda msg: msg.id)
        return last_message.content if last_message.role == "user" else ""

    def _get_relevant_context(self, user_query: str, 
                              chunk_ids_and_collection_name_by_document_id: dict[int, dict[str, list[int]]]) -> RelevantContextDto:
        if user_query:
            return self.collections_service.get_relevant_context(chunk_ids_and_collection_name_by_document_id, 
                                                                 user_query, 
                                                                 max_length=4000)
        return RelevantContextDto(context="", chunk_data=[])

    def _update_or_create_system_message(self, messages: list[Message], context: str) -> list[Message]:
        system_message_index = next((i for i, msg in enumerate(messages) if msg.role == "system"), -1)

        if system_message_index >= 0:
            original_content = messages[system_message_index].content
            messages[system_message_index].content = f"{original_content}\n\nAdditional context from uploaded documents:\n{context}"
        else:
            system_message = MessageDTO(
                role="system",
                content=f"You are a helpful assistant. Use the following additional context from uploaded documents to answer the user's question:\n\n{context}"
            )
            messages.insert(0, system_message)
