from schemas import ResponseModel
from typing import Optional

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    {"id": 3, "name": "Bob Wilson", "email": "bob@example.com"},
    {"id": 4, "name": "Alice Brown", "email": "alice@example.com"},
    {"id": 5, "name": "Charlie Davis", "email": "charlie@example.com"}
]

#verify user
def verify_user(id: int) -> bool:
    """
    Verify if a user exists.

    Args:
        id (int): The ID of the user to verify.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    for user in users:
        if user["id"] == id:
            return True
    return False


def generate_answer(question: str) -> str:
    """
    Simulate answer generation for a given question.

    Args:
        question (str): The user's question.

    Returns:
        str: A simulated answer to the question.
    """
    # Simulate some answer generation logic
    return f"This is a simulated answer to your question: '{question}'."


def generate_response(question: str, user_id: int) -> ResponseModel:
    """
    Simulate answer generation for a given question.

    Args:
        question (str): The user's question.

    Returns:
        ResponseModel: The simulated response model.
    """
    answer = f"This is a simulated answer to your question: '{question}'."
    return ResponseModel(
        user_id=user_id,
        question=question,
        answer=answer,   
    )
