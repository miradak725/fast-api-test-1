from app.schemas.schemas import UserchatHistory
from fastapi import APIRouter,HTTPException,status
from app.db.chat_history import chat_history
from typing import Optional

from core.logger import logger

router = APIRouter()

#Get chat history endpoint
@router.get("/{user_id}", response_model=UserchatHistory)
async def get_chat_history(user_id: int) -> UserchatHistory:
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

