from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

all_todos=[
    {"id":1,"task":"Do laundry"},
    {"id":2,"task":"Read a book"},
    {"id":3,"task":"Write code"},
    {"id":4,"task":"Exercise"}
]

class TodoCreate(BaseModel):
    task: str

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/chat")
def chat():
    return {"message": "Hello!"}

@app.get("/todos/{id}")
def get_todo(id: int):
    for todo in all_todos:
        if todo['id']==id:
            return {'result':todo}
 
@app.get('/todos')
def get_todos(): 
    return all_todos


@app.post('/todos')
def create_todo(todo: TodoCreate):
# def create_todo(todo):
    new_todo_id=max(todo['id'] for todo in all_todos)+1

    new_todo={
        "id":new_todo_id,
        "task":todo.task,
    }
    all_todos.append(new_todo)
    return new_todo

@app.delete('/todos/{id}')
def delete_todo(id:int):
    for index,todo in enumerate(all_todos):
        if todo['id']==id:
            all_todos.pop(index)
            return {"message":"Todo deleted successfully"}
    return {"message":"Todo not found"}