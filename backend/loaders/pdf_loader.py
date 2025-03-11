from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document as LangchainDocument

from backend.loaders.base_loader import DocumentLoader


class PDFDocumentLoader(DocumentLoader):
    
    def can_load(self, file_name: str) -> bool:
        return file_name.lower().endswith('.pdf')
    
    def load(self, file_path: str) -> List[LangchainDocument]:
        loader = PyPDFLoader(file_path)
        return loader.load() 