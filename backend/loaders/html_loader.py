from typing import List

from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.documents import Document as LangchainDocument

from backend.loaders.base_loader import DocumentLoader


class HTMLDocumentLoader(DocumentLoader):    
    def can_load(self, file_name: str) -> bool:
        file_name_lower = file_name.lower()
        return file_name_lower.endswith('.html') or file_name_lower.endswith('.htm')
    
    def load(self, file_path: str) -> List[LangchainDocument]:
        loader = UnstructuredHTMLLoader(file_path)
        return loader.load() 