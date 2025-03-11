from dataclasses import dataclass

@dataclass
class ModelData:
    model_type: str
    model_name: str

    def __str__(self):
        return f"{self.model_type}: {self.model_name}"