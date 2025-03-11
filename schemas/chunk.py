from dataclasses import dataclass

@dataclass
class Chunk:
    content: str
    metadata: dict

    def __str__(self):
        return f"Chunk(content={self.content}, metadata={self.metadata})"
    
    def summary(self):
        return (self.content[:100] + '...') if len(self.content) > 100 else self.content