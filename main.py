from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status , Query
from typing import Annotated
from typing import Optional

app = FastAPI()

# /chat POST question,user_id -> question,answer,reference,user_id
# /history GET user_id -> List[message]
# /analysis/create POST user_id, focus_id -> user_id, focus_id, analysis


chat_history = [
    {
        "user_id": 1,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you! How can I assist you today?","reference": None},
            {"role": "user", "content": "Tell me a joke."},
]
    },
    {
        "user_id": 2,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the weather like today?"},
            {"role": "assistant", "content": "The weather is sunny with a high of 75°F.","reference": None},
            {"role": "user", "content": "Great, thank you!"},       
        ]
    },
    {
        "user_id": 3,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you help me with my homework?"},
            {"role": "assistant", "content": "Of course! What subject is your homework in?", "reference": None},
            {"role": "user", "content": "It's math."},
        ]
    },
    {
        "user_id": 4,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris.", "reference": None},
            {"role": "user", "content": "Thanks!"},
        ]
    },
    {
        "user_id": 5,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you recommend a good book?"},
            {"role": "assistant", "content": "Sure! 'To Kill a Mockingbird' is a great read.", "reference": None},
            {"role": "user", "content": "I've read that one. Something else?"},
        ]
    }
]  # In-memory storage for chat history grouped by user


# Request model for chat endpoint
class ChatRecord(BaseModel):
    """Response model for chat endpoint."""
    role: str
    content: str
    reference: Optional[str] = None

class UserchatHistory(BaseModel):
    """Response model for user chat history."""
    user_id: int
    chat_history: list[ChatRecord]

# Input model for chat creation
class ChatInput(BaseModel):
    """Input model for creating a new chat."""
    user_id: int
    question: str


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint returning a welcome message.

    Returns:
        dict: A simple greeting message confirming the API is running.
    """
    return {"message": "Hello, World!"}


# chat endpoint
@app.post("/chat", tags=["chat"], status_code=status.HTTP_201_CREATED)
def chat(user_input: ChatInput):
    """
    Append a new question to an existing user's chat_history.
    """
    if not user_input.question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must be provided."
        )

    for user in chat_history:
        if user["user_id"] == user_input.user_id:
            user_message={"role": "user", "content": user_input.question}
            assistant_message={"role": "assistant", "content": "This is a generated answer.", "reference": None}
            user["chat_history"].append(user_message)
            user["chat_history"].append(assistant_message)
            return {"user": user_message, "assistant": assistant_message}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found."
    )
#Get chat history endpoint
@app.get("/history", tags=["chat"], response_model=UserchatHistory)
def get_chat_history(user_id: int) -> UserchatHistory:
    """
    Get the chat history for a specific user.

    Args:
        user_id (int): The ID of the user whose chat history is to be retrieved.

    Returns:
        UserchatHistory: The chat history of the user.
    """
    for user in chat_history:
        if user["user_id"] == user_id:
            try:
                return UserchatHistory(user_id=user_id, chat_history=user["chat_history"])
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while retrieving chat history."
                )   
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found."
    )

# # /analysis/create POST user_id, focus_id -> user_id, focus_id, analysis
# @app.post("/analysis/create", tags=["analysis"], response_model=UserchatHistory)
# def create_analysis(user_id: int, focus_id: int):
#     """
#     Create a new analysis for a specific user and focus ID.

#     Args:
#         user_id (int): The ID of the user creating the analysis.
#         focus_id (int): The ID of the focus for the analysis.

#     Returns:
#         UserchatHistory: The created analysis information.
#     """
#     # Simulate analysis creation
#     analysis = {"user_id": user_id, "focus_id": focus_id, "analysis": "This is a generated analysis."}
#     return UserchatHistory(user_id=user_id, chat_history=[analysis])





# # Chat endpoint
# @app.get("/chat", tags=["chat"])
# def chat(user:str)->dict:
#     """
#     Chat endpoint returning a greeting message.

#     Returns:
#         dict: A friendly greeting message.
#     """
#     if not user.isalpha():  # Optional: stricter rule (only letters)
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username must contain only letters."
#         )
#     try:
#         # Simulate some processing
#         result = {"message": f"Hello, {user}!"}
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An error occurred while processing your request."
#         )
#     return result
