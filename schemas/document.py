from schemas.chunk import Chunk
from dataclasses import dataclass

@dataclass
class Document:
    name: str
    chunks: list[Chunk]

    def __str__(self):
        return f"Document(name={self.name}, chunks={self.chunks})"
    
    def get_chunk_count(self):
        return len(self.chunks)
    
    def get_chunk(self, index: int):
        return self.chunks[index]
 