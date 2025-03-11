class SessionConfig:
    """Class to store key names for session state management."""
    
    # Authentication keys
    TOKEN_KEY = "auth_token"
    USER_ID = "user_id"
    USER_SUB = "user_sub"
    CHAT_ID = "chat_id"

    # Chat settings
    CHAT_TITLE = "chat_title"
    SYSTEM_PROMPT = "system_prompt"
    
    # API keys
    OPENAI_API_KEY = "openai_api_key"
    HF_API_KEY = "hf_api_key"

    # Model settings
    MODEL_SETTINGS = "model_settings"
    MODEL_TYPE = "model_type"
    AVAILABLE_MODELS = "available_models"
    
    # Collection settings
    COLLECTION_NAME = "collection_name"
    EDITING_CHAT_ID = "editing_chat_id"

    # Chunk settings
    CHUNK_SIZE = "chunk_size"
    CHUNK_OVERLAP = "chunk_overlap"

    # Client identifiers
    HUGGINGFACE_CLIENT = "huggingface_client"
    POSTGRES_CLIENT = "postgres_client"
    
    # Facades
    CHAT_FACADE = "chat_facade"
    LIBRARY_FACADE = "library_facade"
    DOCUMENTS_FACADE = "documents_facade"

    # Factories
    LOADER_FACTORY = "loader_factory"
    MODEL_FACTORY = "model_factory"

    # Services
    ASSISTANT_SERVICE = "assistant_service"
    DOCUMENT_SERVICE = "document_service"
    CHAT_SERVICE = "chat_service"
    MODEL_SERVICE = "model_service"
    COLLECTIONS_SERVICE = "collections_service"
    MESSAGE_SERVICE = "message_service"
    SESSION_SERVICE = "session_service"
    DOCUMENTS_SERVICE = "documents_service"
    CHUNKS_SERVICE = "chunks_service"
    METADATA_SERVICE = "metadata_service"
    SOURCE_SERVICE = "source_service"
    SCIENTIFIC_HUB_SERVICE = "scientific_hub_service"

    # Initializer
    SERVICE_INITIALIZER = "service_initializer"

    # Repositories
    DOCUMENT_REPOSITORY = "document_repository"
    MESSAGE_REPOSITORY = "message_repository"
    CHAT_REPOSITORY = "chat_repository"
    SOURCE_REPOSITORY = "source_repository" 
    
    # Mappers
    MESSAGE_MAPPER = "message_mapper"

    # Transformers
    SENTENCE_TRANSFORMER = "sentence_transformer"
    SUMMARIZATION_TRANSFORMER = "summarization_transformer"
    CLASSIFICATION_TRANSFORMER = "classification_transformer"
    QUESTION_ANSWERING_TRANSFORMER = "question_answering_transformer"

    # Error keys
    HF_API_KEY_ERROR = "hf_api_key_error"

    # Summarized chunks
    SUMMARIZED_CHUNKS = "summarized_chunks"
