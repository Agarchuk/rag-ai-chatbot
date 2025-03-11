from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document as LangchainDocument

from backend.loaders.base_loader import DocumentLoader


class TextDocumentLoader(DocumentLoader):
    
    def can_load(self, file_name: str) -> bool:
        return file_name.lower().endswith('.txt')
    
    def load(self, file_path: str) -> List[LangchainDocument]:
        loader = TextLoader(file_path)
        return loader.load() 