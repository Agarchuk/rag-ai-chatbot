from dataclasses import dataclass, asdict

@dataclass
class MessageDTO:
    id: int = None
    content: str = None
    role: str = None
    chat_id: int = None
    user_id: int = None

    def to_dict(self):
        return asdict(self)
