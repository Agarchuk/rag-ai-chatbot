from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from utils.logger import log_info
from backend.clients.postgres_client import PostgresClient

_cleanup_performed = False

class ServiceInitializer:

    def initialize_app(self):
        log_info("Initializing app")
        SessionStateService().set(SessionConfig.COLLECTION_NAME, "library_documents")
        if not SessionStateService().has(SessionConfig.POSTGRES_CLIENT):
            self.init_db()

    def init_db(self):
        log_info("Initializing db")
        db_client = PostgresClient.get_instance()
        SessionStateService().set(SessionConfig.POSTGRES_CLIENT, db_client)
    
    def cleanup_db(self):
        db_client = PostgresClient.get_instance()
        global _cleanup_performed
        if not _cleanup_performed:
            db_client.close_connection()
            _cleanup_performed = True

    
