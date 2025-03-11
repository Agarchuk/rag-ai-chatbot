from dtos.chunk_data import ChunkData

class RelevantContextDto:
    def __init__(self, context: str, chunk_data: list[ChunkData]):
        self.context = context
        self.chunk_data = chunk_data

    def __str__(self):
        return f"Context: {self.context}\nChunk Data: {self.chunk_data}"
