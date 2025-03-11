from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document as LangchainDocument


class DocumentLoader(ABC):    
    @abstractmethod
    def can_load(self, file_name: str) -> bool:
        pass
    
    @abstractmethod
    def load(self, file_path: str) -> List[LangchainDocument]:
        pass 