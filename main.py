from fastapi import FastAPI,Request
from contextlib import asynccontextmanager
from app.api import routes_analysis,routes_chat,routes_chat_history
from core.logger import logger
from app.utils.rag_chain import load_llm,load_retriever,retrieve_method
from app.utils.rag_chain import llm,retriever

# llm=None
# retriever=None

@asynccontextmanager
async def lifespan(app:FastAPI):
    #Load llm
    load_llm()
    load_retriever(retrieve_method)
    print("Starting the application...")
    yield
    print("Shutting down the application...")
    # Clean up the retriever
    if retriever:
        retriever.cleanup()
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


@app.get("/health")
async def health()->dict:
    return {"status":"ok", "messege":"RAG Chat app backend is running"}
