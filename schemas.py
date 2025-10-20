from typing import List,Optional
from pydantic import BaseModel

# Response model for individual chat records
class ChatRecord(BaseModel):
    """Response model for chat endpoint."""
    role: str
    content: str
    reference: Optional[List[str]] = []

# Response model for user chat history
class UserchatHistory(BaseModel):
    """Response model for user chat history."""
    user_id: int
    chat_history: list[ChatRecord]

# Input model for chat creation
class ChatInput(BaseModel):
    """Input model for creating a new chat."""
    user_id: int
    question: str

class ResponseModel(BaseModel):
    """Response model for chat endpoint."""
    user_id: int
    question: str
    answer: str
    reference: Optional[List[str]] = []

class analyseModel(BaseModel):
    user_id: int
    focus_id: int
    analysis: str

 