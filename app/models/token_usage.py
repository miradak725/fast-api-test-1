from sqlmodel import SQLModel,Field
from datetime import datetime


class TokenUsage(SQLModel,table=True):
    """Model representing token usage statistics."""

    __tablename__ = "token_usage" 
    usage_id: int = Field(default=None, primary_key=True)
    user_id: int
    month: int 
    tokens_used: int = Field(default=0)
    remaining_tokens: int = Field(default=0)
    updated_at: datetime = Field(default=datetime.utcnow)  # ISO formatted timestamp

    def __repr__(self):
        return f"<TokenUsage(user_id={self.user_id}, month={self.month}, tokens_used={self.tokens_used}, remaining_tokens={self.remaining_tokens}, updated_at={self.updated_at})>"