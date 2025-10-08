from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# Sample in-memory data store for todo items
all_todos=[
    {"id":1,"task":"Do laundry"},
    {"id":2,"task":"Read a book"},
    {"id":3,"task":"Write code"},
    {"id":4,"task":"Exercise"}
]

# Pydantic model for a todo item
class Todo(BaseModel):
    """Model for a todo item"""
    task: str


# Root endpoint
@app.get("/")
async def root()->dict: 
    """
    Root endpoint returning a welcome message.

    Inputs:
        None
    Returns:
        dict: A simple greeting message confirming the API is running.
    """
    try:
        return {"message": "Hello, World!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Chat endpoint
@app.get("/chat", tags=["chat"])
def chat(message:str) -> dict:
    """
    Chat endpoint returning a greeting message.

    Inputs:
        message (str): The message from the user.
    Returns:
        dict: A friendly greeting message.
    """
    return {"message": "Hello!"}


# Get Todo by ID
@app.get('/todos/{id}', tags=["todos"])
def get_todo(id:int) -> dict:
    """
    Retrieve a todo item by its unique ID.

    Args:
        id (int): The ID of the todo item to retrieve.

    Returns:
        dict: The todo item if found.

    Raises:
        HTTPException: If the todo with the given ID does not exist (404 Not Found).
    """
    for todo in all_todos:
        if todo['id']==id:
            return {'result':todo}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


# Get All Todos
@app.get(
    '/todos',
    summary="Retrieve all todo items",
    description="Fetch a list of all todo items available in the system.", 
    tags=["todos"])
def get_todos():
    """
    Retrieve all todo items.

    Inputs:
        None
    Returns:
        list: A list of all todo items.
    """
    return all_todos


# Search Todos by Keyword
@app.get("/todos/search/", tags=["Search task"])
def search_todos(query: str):
    """
    Search for todo items containing a keyword in their task name.

    Args:
        query (str): The keyword to search for (case-insensitive).

    Returns:
        dict: A dictionary with matching todo items under the "results" key.

    Raises:
        HTTPException: If no matching todos are found (404 Not Found).
    """
    results = [todo for todo in all_todos if query.lower() in todo['task'].lower()]
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching todos found")
    return {"results": results}



# Create a New Todo
@app.post('/todos',tags=["Create new task"])
def create_todo(todo: Todo):
    """
    Create a new todo item.

    Args:
        todo (Todo): The todo item data (task name).

    Returns:
        dict: The newly created todo item with an assigned unique ID.
    """
    new_todo_id=max(todo['id'] for todo in all_todos)+1

    new_todo={
        "id":new_todo_id,
        "task":todo.task,
    }
    all_todos.append(new_todo)
    return new_todo


# Delete Todo by ID
@app.delete('/todos/{id}',tags=["Delete a task"])
def delete_todo(id:int):
    """
    Delete a todo item by its ID.

    Args:
        id (int): The ID of the todo item to delete.

    Returns:
        dict: A message indicating the result of the deletion.

    Raises:
        HTTPException: If the todo with the given ID does not exist (404 Not Found).
    """
    try:
        for index,todo in enumerate(all_todos):
            if todo['id']==id:
                all_todos.pop(index)
                return {"message":"Todo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")