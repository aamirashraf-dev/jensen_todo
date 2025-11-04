from fastapi import APIRouter
from schemas.todo import Todo
from services.file_service import read_db, write_db
from datetime import datetime, timezone

router = APIRouter()

@router.get("/todos", response_model=list[Todo])
def get_todos():
    todos = read_db()
    return [Todo(**todo) for todo in todos]

@router.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    todos = read_db()
    new_todo = Todo(
        id=len(todos) + 1,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todos.append(new_todo.model_dump())
    write_db(todos)
    return new_todo

