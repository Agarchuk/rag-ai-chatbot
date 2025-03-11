from backend.loaders.base_loader import DocumentLoader
from backend.loaders.pdf_loader import PDFDocumentLoader
from backend.loaders.docx_loader import DocxDocumentLoader
from backend.loaders.text_loader import TextDocumentLoader
from backend.loaders.html_loader import HTMLDocumentLoader

__all__ = [
    'DocumentLoader',
    'PDFDocumentLoader',
    'DocxDocumentLoader',
    'TextDocumentLoader',
    'HTMLDocumentLoader'
]
