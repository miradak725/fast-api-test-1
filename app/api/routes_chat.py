from fastapi import HTTPException, status,APIRouter
from app.utils.utils import verify_user
from app.utils.rag_chain import retrieve_method, generate_answer,load_retriever
from app.db.chat_history import chat_history
from app.schemas.schemas import ChatInput,ChatOutput
from typing import Optional
from core.logger import logger

router= APIRouter()
retriever = load_retriever(retrieve_method)


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


# chat endpoint
@router.post("/generate", tags=["Chat"], status_code=status.HTTP_201_CREATED)
async def chat(user_input: ChatInput)->ChatOutput:
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
        response ,references= generate_answer(user_input.question)

        logger.debug(f"Generated response for user_id {user_input.user_id}: {response}")
        logger.info(f"Starting chat history update for user_id: {user_input.user_id}")

        add_chat_history(user_input.user_id, user_input.question, response)
        logger.info(f"Chat history updated for user_id {user_input.user_id}")
        chat_response ={
            "user_id": user_input.user_id,
            "question": user_input.question,
            "answer": response,
            "references":references,
        }
        return chat_response
    
    except Exception as e:
        logger.error(f"Error occurred while processing request for user_id {user_input.user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )
