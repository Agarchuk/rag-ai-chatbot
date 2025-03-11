from dataclasses import dataclass
from dtos.chunk_data import ChunkData

@dataclass
class AssistantResponseDto:
    response_chunks: list[str]
    chunk_data: list[ChunkData]
