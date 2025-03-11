from abc import ABC, abstractmethod
from backend.models.message import Message

class BaseAIModel(ABC):
    @abstractmethod
    def generate_response(self, messages: list[Message]) -> str:
        pass
