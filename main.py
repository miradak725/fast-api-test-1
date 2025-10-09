from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status , Query
from typing import Annotated

app = FastAPI()

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint returning a welcome message.

    Returns:
        dict: A simple greeting message confirming the API is running.
    """
    return {"message": "Hello, World!"}


# Chat endpoint
@app.get("/chat", tags=["chat"])
def chat(user:str)->dict:
    """
    Chat endpoint returning a greeting message.

    Returns:
        dict: A friendly greeting message.
    """
    if not user.isalpha():  # Optional: stricter rule (only letters)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must contain only letters."
        )
    try:
        # Simulate some processing
        result = {"message": f"Hello, {user}!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )
    return result

