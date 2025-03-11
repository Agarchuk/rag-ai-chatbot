from typing import Optional

from backend.loaders.base_loader import DocumentLoader
from backend.loaders.pdf_loader import PDFDocumentLoader
from backend.loaders.docx_loader import DocxDocumentLoader
from backend.loaders.text_loader import TextDocumentLoader
from backend.loaders.html_loader import HTMLDocumentLoader


class DocumentLoaderFactory:       
    def __init__(self):
        self.loaders = [
            PDFDocumentLoader(),
            DocxDocumentLoader(),
            TextDocumentLoader(),
            HTMLDocumentLoader()
        ]
    
    def get_loader(self, file_name: str) -> Optional[DocumentLoader]:
        for loader in self.loaders:
            if loader.can_load(file_name):
                return loader
        return None
    