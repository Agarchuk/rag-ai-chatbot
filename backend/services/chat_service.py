from typing import Optional
from backend.clients.huggingface_client import HuggingFaceClient
from backend.models.chat import Chat
from backend.repositories.chat_repository import ChatRepository
from backend.models.message import Message
from config.settings import TITLE_GENERATION_CONFIG
from utils.logger import log_warning, log_error
from backend.mapper.message_mapper import MessageMapper
from dtos.message_dto import MessageDTO
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from typing import List

# nltk.download('punkt_tab')
# log_warning(f"nltk.data.path: {nltk.data.path}")

class ChatService:
    def __init__(self, chat_repository: ChatRepository, huggingface_client: HuggingFaceClient):
        """Initialize the chat service"""
        self.chat_repository: ChatRepository = chat_repository
        self.huggingface_client: HuggingFaceClient = huggingface_client     

    def create_chat(self, user_id: str, messages: List[Message] = None) -> Chat:
        """Creates a new chat with a title generated from the first message."""
        if messages is None:
            messages = []
            title = "AI Chat"
        else:
            title = self.generate_chat_title(messages[0])
        chat = self.chat_repository.create_chat(user_id=user_id, title=title, messages=messages)
        return chat  

    def generate_chat_title(self, first_message: Message) -> str:
        first_message_content = first_message.content
        if len(first_message_content) > TITLE_GENERATION_CONFIG['length_threshold']:
            return self.huggingface_client.generate_title(first_message_content)
        return self.keyword_extraction(first_message_content)
    
    def keyword_extraction(self, text: str, max_keywords: int = 3) -> str:
        try:
            r = Rake(
                min_length=1,
                max_length=3,
                include_repeated_phrases=False
            )
            
            r.extract_keywords_from_text(text)
            phrases = r.get_ranked_phrases()
            keywords = [p.replace(' ', '_') for p in phrases[:max_keywords] if 3 <= len(p) <= 20]
            
            if not keywords:
                return self._keyword_fallback(text, max_keywords)
                
            return '_'.join(keywords)
        
        except Exception as e:
            return self._keyword_fallback(text, max_keywords)
    
    def get_user_chat_history(self, chat_id: int = None) -> list[MessageDTO]:
        if chat_id:
            chat = self.chat_repository.get_chat_by_id(chat_id)
            return [MessageMapper.map_message_model_to_dto(message) for message in chat.messages]
        else:
            return []            
    
    def get_user_chats(self, user_id: int):
        return self.chat_repository.get_chats_by_user(user_id)
    
    def get_user_chat_ids(self, user_id: int):
        return [chat.id for chat in self.get_user_chats(user_id)]

    def get_or_create_chat_id(self, user_id: int, chat_id: Optional[int] = None) -> int:
        if chat_id is not None:
            if self._validate_if_chat_exists(chat_id):
                return chat_id
        
        chat = self.chat_repository.create_chat(user_id=user_id, title="New Chat")
        return chat.id
   
    def update_chat_title(self, chat_id: int, new_title: str) -> bool:
        result = self.chat_repository.update_chat_title(chat_id, new_title)
         
        return result
    
    def attach_library_document(self, chat_id: int, document_id: int) -> bool:
        return self.chat_repository.attach_library_document(chat_id, document_id)
    
     
    def delete_chat(self, chat_id: int, user_id: str) -> bool:
        
        try:
            chat = self.chat_repository.get_chat_by_id(chat_id)
            if not chat:
                log_warning(f"Chat with ID {chat_id} not found, nothing to delete")
                return False
    

            db_deletion_success = self.chat_repository.delete_chat(chat_id)  
            return db_deletion_success
        except Exception as e:
            log_error(f"Error in delete_chat for chat ID: {chat_id}", str(e))
            return False
    
    def _validate_if_chat_exists(self, chat_id: int):
        return self.chat_repository.get_chat_by_id(chat_id) is not None

    
    def _keyword_fallback(self, text: str, max_keywords: int = 3) -> str:
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_words = [
            word for word in words 
            if word.isalnum() and word not in stop_words
        ]
        
        word_freq = Counter(filtered_words)
        keywords = [word for word, _ in word_freq.most_common(max_keywords)]
        
        return '_'.join(keywords)[:30] or 'Untitled'
    