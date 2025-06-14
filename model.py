from pydantic import BaseModel
from dataclasses import dataclass

# Define model
class ChatRequest(BaseModel):
    session_id: str
    message: str

@dataclass
class ChatRequestModel:
    session_id: str
    message: str
