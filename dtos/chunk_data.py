from pydantic import BaseModel

class ChunkData(BaseModel):
    text: str
    document_name: str
    id: str
    distance: float
    document_id: int = None

