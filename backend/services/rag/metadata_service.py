from typing import Dict, Any
from langchain_core.documents import Document as LangchainDocument

class MetadataService:

    def prepare_metadata(self, chunk: LangchainDocument, chunk_id: str, document_name: str, chunk_index: int, total_chunks: int) -> Dict[str, Any]:
        metadata = chunk.metadata.copy() if hasattr(chunk, 'metadata') else {}
        metadata.update({
            'chunk_id': chunk_id,
            'document_name': document_name,
            'chunk_index': chunk_index,
            'total_chunks': total_chunks
        })
        return metadata
