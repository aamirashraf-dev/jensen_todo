from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.todo import Todo
from app.services.file_service import read_db, write_db

router = APIRouter()


@router.get("/todos", response_model=List[Todo])
def get_todos():
    todos = read_db()
    return [Todo(**todo) for todo in todos]


@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    todos = read_db()

    # Assignment 4: improved ID generation
    new_id = max((t["id"] for t in todos), default=0) + 1

    new_todo = Todo(
        id=new_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todos.append(new_todo.model_dump())
    write_db(todos)
    return new_todo


@router.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    todos = read_db()
    for t in todos:
        if t["id"] == todo_id:
            return Todo(**t)
    raise HTTPException(status_code=404, detail="Todo not found")


@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    todos = read_db()
    for index, t in enumerate(todos):
        if t["id"] == todo_id:
            # keep same id, update rest
            todos[index] = updated_todo.model_dump()
            todos[index]["id"] = todo_id
            write_db(todos)
            return Todo(**todos[index])
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todos = read_db()
    for t in todos:
        if t["id"] == todo_id:
            todos.remove(t)
            write_db(todos)
            return {"message": f"Todo {todo_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")