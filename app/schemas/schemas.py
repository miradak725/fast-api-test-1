from typing import List,Optional
from datetime import datetime
from pydantic import BaseModel,Field

# Response model for individual chat records
class ChatRecord(BaseModel):
    """Response model for chat endpoint."""
    role: str
    content: str
    # reference: Optional[List[str]]      #Optional

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

class ChatOutput(BaseModel):
    """Response model for chat endpoint."""
    user_id: int
    question: str
    answer: str
    references: Optional[List[str]] = []
    # references: List[str] 

class AnalyseInput(BaseModel):
    user_id:int
    focus_id:int

class AnalyseOutput(BaseModel):
    user_id: int
    focus_id: int
    analysis: str


class FocusOutput(BaseModel):
    focus_id:int
    focus_name:str
    reports:List['FocusReport']

class FocusReport(BaseModel):
    country:str
    description:str
    created_at:str
    

class TokenUsageOutput(BaseModel):
    user_id: int
    month:int
    tokens_used:int
    remaining_tokens:int
    updated_at: datetime


 