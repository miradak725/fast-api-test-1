from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status , Query
from typing import Optional
from utils import verify_user, generate_response
from schemas import ChatInput, UserchatHistory, analyseModel
from logger import logger

app = FastAPI()
logger.info("FastAPI app initialized.")

# /chat POST question,user_id -> question,answer,reference,user_id
# /history GET user_id -> List[message]
# /analysis/create POST user_id, focus_id -> user_id, focus_id, analysis


chat_history = [
    {
        "user_id": 1,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you! How can I assist you today?","reference": []},
            {"role": "user", "content": "Tell me a joke."},
]
    },
    {
        "user_id": 2,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the weather like today?"},
            {"role": "assistant", "content": "The weather is sunny with a high of 75°F.","reference": []},
            {"role": "user", "content": "Great, thank you!"},       
        ]
    },
    {
        "user_id": 3,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you help me with my homework?"},
            {"role": "assistant", "content": "Of course! What subject is your homework in?", "reference": []},
            {"role": "user", "content": "It's math."},
        ]
    },
    {
        "user_id": 4,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris.", "reference": []},
            {"role": "user", "content": "Thanks!"},
        ]
    },
    {
        "user_id": 5,
        "chat_history": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you recommend a good book?"},
            {"role": "assistant", "content": "Sure! 'To Kill a Mockingbird' is a great read.", "reference": []},
            {"role": "user", "content": "I've read that one. Something else?"},
        ]
    }
]  # In-memory storage for chat history grouped by user



def add_chat_history(user_id: int, question: str, answer: str, reference: Optional[str] = None):
    """
    Add a new chat record to the chat history for a specific user.

    Args:
        user_id (int): The ID of the user.
        question (str): The user's question.
        answer (str): The assistant's answer.
        reference (Optional[str]): An optional reference for the answer.

    """
    for user in chat_history:
        if user["user_id"] == user_id:
            user["chat_history"].append({"role": "user", "content": question})
            user["chat_history"].append({"role": "assistant", "content": answer, "reference": reference})
            return


# def generate_answer(question: str) -> str:
#     """
#     Simulate answer generation for a given question.

#     Args:
#         question (str): The user's question.

#     Returns:
#         str: A simulated answer to the question.
#     """
#     # Simulate some answer generation logic
#     return f"This is a simulated answer to your question: '{question}'."

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint returning a welcome message.

    Returns:
        dict: A simple greeting message confirming the API is running.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Hello, World!"}


# chat endpoint
@app.post("/chat", tags=["chat"], status_code=status.HTTP_201_CREATED)
def chat(user_input: ChatInput):
    """
    Handle chat interactions by receiving a user's question and returning an answer.
    """
    logger.info(f"Chat endpoint accessed by user_id: {user_input.user_id}")
    if not verify_user(user_input.user_id):
        logger.error(f"Invalid user_id {user_input.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    if not user_input.question:
        logger.warning("Empty question received.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must be provided."
        )

    try:
        response = generate_response(user_input.question, user_input.user_id)
        logger.debug(f"Generated response for user_id {user_input.user_id}: {response}")
        add_chat_history(user_input.user_id, user_input.question, response.answer, response.reference)
        logger.info(f"Chat history updated for user_id {user_input.user_id}")
        return response
    
    except Exception as e:
        logger.error(f"Error occurred while processing request for user_id {user_input.user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )

    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail="User not found."
    # )


#Get chat history endpoint
@app.get("/history", tags=["chat"], response_model=UserchatHistory)
def get_chat_history(user_id: int) -> UserchatHistory:
    logger.info(f"chat history accessed for user_id={user_id}")
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
                logger.debug(f"Returning chat history for user_id={user_id}")
                return UserchatHistory(user_id=user_id, chat_history=user["chat_history"])
            except Exception as e:
                logger.exception(f"Error retrieving chat history for user_id={user_id}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while retrieving chat history."
                )

    logger.warning(f"Chat history not found for user_id={user_id}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found."
    )


# /analysis/create POST user_id, focus_id -> user_id, focus_id, analysis
@app.post("/analysis/create", tags=["Analysis"])
def create_analysis(user_id: int, focus_id: int)-> analyseModel:

    if not verify_user(user_id):
        logger.error(f"User verification failed for user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    try:
        logger.debug(f"Generating analysis for user_id={user_id}, focus_id={focus_id}")
        result=analyseModel(
            user_id=user_id,
            focus_id=focus_id,
            analysis="This is a generated analysis."
        )
        logger.info(f"Analysis generated for user_id={user_id}, focus_id={focus_id} successfully")
        return result
    except Exception as e:
        logger.exception(f"Error generating analysis for user_id={user_id}, focus_id={focus_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the analysis."
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
