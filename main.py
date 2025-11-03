from fastapi import FastAPI,Request
from contextlib import asynccontextmanager
from app.api import routes_analysis,routes_chat,routes_chat_history,routes_focus
from app.service import token_service
from core.logger import logger
from app.utils.rag_chain import load_llm,load_retriever,retrieve_method
from app.utils.rag_chain import llm,retriever
from app.db.db import init_db

from app.schemas.schemas import TokenUsageOutput
from app.db.db import SessionDep
from app.service.token_service import TokenService
from datetime import datetime


# llm=None
# retriever=None

@asynccontextmanager
async def lifespan(app:FastAPI):
    #Load llm
    load_llm()
    load_retriever(retrieve_method)
    #Initialize the database
    print("Initializing the database...")
    init_db()
    print("Initializing the database successful.")
    print("Starting the application...")
    yield
    print("Shutting down the application...")

    # Clean up the ML model
    if llm:
        llm.cleanup()
    print("Application shut down complete.")


app = FastAPI(lifespan=lifespan)
logger.info("FastAPI app initialized.")

#Root end point
@app.get("/")
async def root():
    """
    Root endpoint returning a welcome message.

    Returns:
        dict: A simple greeting message confirming the API is running.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Hello, World!"}


app.include_router(routes_analysis.router,prefix="/api/analysis",tags=["Analysis"])
app.include_router(routes_chat.router,prefix="/api/chat",tags=["Chat"])
app.include_router(routes_chat_history.router,prefix="/api/chat_history",tags=["Chat_history"])
app.include_router(routes_focus.router,prefix="/api/focus",tags=["Focus"])


# Health check endpoint
@app.get("/health")
async def health()->dict:
    return {"status":"ok", "messege":"RAG Chat app backend is running"}

#Get token count endpoint
@app.get("/tokens/get_tokens/{user_id}",response_model= TokenUsageOutput)
def get_token_count(user_id:int, session: SessionDep):
    """Endpoint to get the token count for a specific user."""
    token_service=TokenService()
    record = token_service.get_token_count(user_id, session)
    if not record:
        return {"error": "User not found"}
    return TokenUsageOutput(
        user_id=record.user_id,
        month=record.month,
        tokens_used=record.tokens_used,
        remaining_tokens=record.remaining_tokens,
        updated_at=record.updated_at
    )

#Set token count endpoint
@app.post("/tokens/set_tokens/{user_id}", response_model=TokenUsageOutput)
def set_token_count(user_id: int,month:int,tokens_used: int, session: SessionDep):
    """Endpoint to set the token count for a specific user."""
    token_service = TokenService()
    record=token_service.set_token_count(user_id,month, tokens_used, session)
    print("Token count set successfully.")
    return record
