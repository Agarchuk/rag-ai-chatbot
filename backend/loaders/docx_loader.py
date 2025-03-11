from typing import List

from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document as LangchainDocument

from backend.loaders.base_loader import DocumentLoader


class DocxDocumentLoader(DocumentLoader):
    
    def can_load(self, file_name: str) -> bool:
        return file_name.lower().endswith('.docx')
    
    def load(self, file_path: str) -> List[LangchainDocument]:
        loader = Docx2txtLoader(file_path)
        return loader.load() 