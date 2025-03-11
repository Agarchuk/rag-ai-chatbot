import streamlit as st
from backend.clients.huggingface_client import HuggingFaceClient
from backend.clients.postgres_client import PostgresClient
from backend.facades.chat_facade import ChatFacade
from backend.facades.library_facade import LibraryFacade
from backend.factories.model_factory import ModelFactory
from backend.mapper.message_mapper import MessageMapper
from backend.repositories.chat_repository import ChatRepository
from backend.repositories.document_repository import DocumentRepository
from backend.repositories.message_repository import MessageRepository
from backend.services.assistant_service import AssistantService
from backend.services.chat_service import ChatService
from backend.services.message_service import MessageService
from backend.services.rag.chunks_service import ChunksService
from backend.factories.loader_factory import DocumentLoaderFactory
from backend.services.documents_service import DocumentsService
from backend.services.rag.collections_service import CollectionsService
from backend.services.rag.metadata_service import MetadataService
from config.models import MODEL_OPTIONS
from dtos.model_settings import ModelSettings
from ui.utils.session_config import SessionConfig
from utils.logger import log_info, log_error

class SessionStateService:
    """Flexible service for managing user state in Streamlit."""

    @staticmethod
    def set(key: str, value):
        """Sets the value for the specified key in session_state."""
        st.session_state[key] = value

    @staticmethod
    def get(key: str, default=None):
        """Gets the value from session_state; returns default if not found."""
        return st.session_state.get(key, default)

    @staticmethod
    def has(key: str) -> bool:
        """Checks if the key exists in session_state."""
        return key in st.session_state

    @staticmethod
    def get_all() -> dict:
        """Returns all current states as a dictionary."""
        return dict(st.session_state)

    @staticmethod
    def get_chat_id() -> str:
        return SessionStateService.get(SessionConfig.CHAT_ID)

    @staticmethod
    def get_user_id() -> str:
        return SessionStateService.get(SessionConfig.USER_ID)

    @staticmethod
    def get_user_sub() -> str:
        return SessionStateService.get(SessionConfig.USER_SUB)

    @staticmethod
    def get_chat_title(default="AI Chat") -> str:
        return SessionStateService.get(SessionConfig.CHAT_TITLE) or default

    @staticmethod
    def get_chunk_size(default=1000) -> int:
        return SessionStateService.get(SessionConfig.CHUNK_SIZE, default)

    @staticmethod
    def get_chunk_overlap(default=15) -> int:
        return SessionStateService.get(SessionConfig.CHUNK_OVERLAP, default)

    @staticmethod
    def set_chunk_size(chunk_size: int):
        SessionStateService.set(SessionConfig.CHUNK_SIZE, chunk_size)

    @staticmethod
    def set_chunk_overlap(chunk_overlap: int):
        SessionStateService.set(SessionConfig.CHUNK_OVERLAP, chunk_overlap)

    @staticmethod
    def get_model_settings(default=None) -> ModelSettings:
        model_settings = SessionStateService.get(SessionConfig.MODEL_SETTINGS, default)
        return model_settings if model_settings else ModelSettings()

    @staticmethod
    def set_model_settings(model_settings: ModelSettings):
        SessionStateService.set(SessionConfig.MODEL_SETTINGS, model_settings)

    @staticmethod
    def get_available_models() -> list:
        return SessionStateService.get(SessionConfig.AVAILABLE_MODELS, MODEL_OPTIONS)

    @staticmethod
    def set_available_models(models: list):
        SessionStateService.set(SessionConfig.AVAILABLE_MODELS, models)

    @staticmethod
    def get_or_create_component(key, constructor, *args, **kwargs):
        if not SessionStateService.has(key):
            log_info(f"Creating component: {key}")
            component_instance = constructor(*args, **kwargs) if callable(constructor) else constructor()
            SessionStateService.set(key, component_instance)
        return SessionStateService.get(key)

    @staticmethod
    def get_or_create_postgres_client():
        return SessionStateService.get_or_create_component(SessionConfig.POSTGRES_CLIENT, PostgresClient)

    @staticmethod
    def get_or_create_chat_repository():
        postgres_client = SessionStateService.get_or_create_postgres_client()
        return SessionStateService.get_or_create_component(SessionConfig.CHAT_REPOSITORY, ChatRepository, postgres_client)

    @staticmethod
    def get_or_create_huggingface_client():
        return SessionStateService.get_or_create_component(SessionConfig.HUGGINGFACE_CLIENT, HuggingFaceClient)
    
    @staticmethod
    def get_or_create_chat_service():
        model_type = SessionStateService.get_model_settings().model_data.model_type
        key = f"{SessionConfig.CHAT_SERVICE}_{model_type}"
        if SessionStateService.has(key):
            del st.session_state[key]
        chat_repository = SessionStateService.get_or_create_chat_repository()
        huggingface_client = SessionStateService.get_or_create_huggingface_client()
        return SessionStateService.get_or_create_component(SessionConfig.CHAT_SERVICE, ChatService, chat_repository, huggingface_client)
    
    @staticmethod
    def get_or_create_message_service():
        message_repository = SessionStateService.get_or_create_message_repository()
        chat_service = SessionStateService.get_or_create_chat_service()
        message_mapper = SessionStateService.get_or_create_component(SessionConfig.MESSAGE_MAPPER, MessageMapper)
        return SessionStateService.get_or_create_component(SessionConfig.MESSAGE_SERVICE, MessageService, message_repository, chat_service, message_mapper)

    @staticmethod
    def get_or_create_message_repository():
        postgres_client = SessionStateService.get_or_create_postgres_client()
        return SessionStateService.get_or_create_component(SessionConfig.MESSAGE_REPOSITORY, MessageRepository, postgres_client)

    @staticmethod
    def get_or_create_documents_service():
        postgres_client = SessionStateService.get_or_create_postgres_client()
        document_repository = SessionStateService.get_or_create_component(SessionConfig.DOCUMENT_REPOSITORY, DocumentRepository, postgres_client)
        loader_factory = SessionStateService.get_or_create_component(SessionConfig.LOADER_FACTORY, DocumentLoaderFactory)
        chunk_service = SessionStateService.get_or_create_chunks_service()
        metadata_service = SessionStateService.get_or_create_component(SessionConfig.METADATA_SERVICE, MetadataService)
        collections_service = SessionStateService.get_or_create_component(SessionConfig.COLLECTIONS_SERVICE, CollectionsService)

        return SessionStateService.get_or_create_component(
            SessionConfig.DOCUMENTS_SERVICE, 
            DocumentsService, 
            document_repository, 
            loader_factory, 
            chunk_service, 
            metadata_service, 
            collections_service
        )

    @staticmethod
    def get_or_create_model_service():
        model_settings = SessionStateService.get_model_settings()

        model_type = model_settings.model_data.model_type
        
        # If model settings don't have a model specified, use the first available model of the selected type
        if not model_settings.model_data.model_name:
            available_models = SessionStateService.get_available_models()
            models_of_type = [m for m in available_models if m["type"] == model_type]
            if models_of_type:
                model_settings.model_data.model_name = models_of_type[0]["name"]
        
        # Create a unique key for the model service based on model type
        model_service_key = f"{SessionConfig.MODEL_SERVICE}_{model_type}"

        # Create or retrieve the model service from session state
        log_info(f"Creating or retrieving model service: {model_service_key}")
        return SessionStateService.get_or_create_component(model_service_key, ModelFactory().create_model_service, model_settings)

    @staticmethod
    def get_or_create_chunks_service():
        return SessionStateService.get_or_create_component(SessionConfig.CHUNKS_SERVICE, ChunksService)

    @staticmethod
    def get_or_create_assistant_service() -> AssistantService:
        if SessionStateService.has(SessionConfig.ASSISTANT_SERVICE):
            del st.session_state[SessionConfig.ASSISTANT_SERVICE]
        collection_service = SessionStateService.get_or_create_component(SessionConfig.COLLECTIONS_SERVICE, CollectionsService)
        documents_service = SessionStateService.get_or_create_documents_service()
        return SessionStateService.get_or_create_component(SessionConfig.ASSISTANT_SERVICE, 
                                                           AssistantService, 
                                                           collection_service, 
                                                           documents_service)

    @staticmethod
    def get_or_create_library_facade():
        loader_factory = SessionStateService.get_or_create_component(SessionConfig.LOADER_FACTORY, DocumentLoaderFactory) 
        documents_service = SessionStateService.get_or_create_documents_service()
        chat_service = SessionStateService.get_or_create_chat_service()
        chunks_service = SessionStateService.get_or_create_chunks_service()

        return SessionStateService.get_or_create_component(SessionConfig.LIBRARY_FACADE, 
                                                           LibraryFacade, 
                                                           loader_factory, 
                                                           documents_service, 
                                                           chat_service, 
                                                           chunks_service)

    @staticmethod
    def get_or_create_chat_facade():
        chat_service = SessionStateService.get_or_create_chat_service()
        assistant_service = SessionStateService.get_or_create_assistant_service()
        documents_service = SessionStateService.get_or_create_documents_service()
        return SessionStateService.get_or_create_component(SessionConfig.CHAT_FACADE, ChatFacade, 
                                                           assistant_service, 
                                                           chat_service, 
                                                           documents_service)
    