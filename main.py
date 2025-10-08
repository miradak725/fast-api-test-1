from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

all_todos=[
    {"id":1,"task":"Do laundry"},
    {"id":2,"task":"Read a book"},
    {"id":3,"task":"Write code"},
    {"id":4,"task":"Exercise"}
]

class Todo(BaseModel):
    """Model for a todo item"""
    task: str

@app.get("/")
async def root():
    """Root endpoint returning a welcome message"""
    return {"message": "Hello, World!"}

@app.get("/chat", tags=["chat"])
def chat():
    """Chat endpoint returning a greeting message"""
    return {"message": "Hello!"}

@app.get("/todos/{id}", tags=["todos"])
def get_todo(id: int):
    """Get a todo item by its ID"""
    for todo in all_todos:
        if todo['id']==id:
            return {'result':todo}

@app.get('/todos', tags=["todos"])
def get_todos():
    """Get all todo items"""
    return all_todos

@app.get("/todos/search/", tags=["Search task"])
def search_todos(query: str):
    """Search for todo items by task"""
    results = [todo for todo in all_todos if query.lower() in todo['task'].lower()]
    return {"results": results}

@app.post('/todos',tags=["Create new task"])
def create_todo(todo: Todo):
    """Create a new todo item"""
# def create_todo(todo):
    new_todo_id=max(todo['id'] for todo in all_todos)+1

    new_todo={
        "id":new_todo_id,
        "task":todo.task,
    }
    all_todos.append(new_todo)
    return new_todo
@app.delete('/todos/{id}',tags=["Delete a task"])
def delete_todo(id:int):
    """Delete a todo item by its ID"""
    for index,todo in enumerate(all_todos):
        if todo['id']==id:
            all_todos.pop(index)
            return {"message":"Todo deleted successfully"}
    return {"message":"Todo not found"}