from dataclasses import dataclass, field
from dtos.model_data import ModelData

@dataclass
class ModelSettings:
    model_data: ModelData = field(default_factory=ModelData)
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    api_key: str = ""
    hf_api_key: str = ""

    def __str__(self):
        return f"ModelSettings(model_data={self.model_data}, temperature={self.temperature}, max_tokens={self.max_tokens}, top_p={self.top_p}, frequency_penalty={self.frequency_penalty}, presence_penalty={self.presence_penalty})"