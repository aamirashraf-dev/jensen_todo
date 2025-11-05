from fastapi import FastAPI
from app.routers import todos

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"message": "OK"}

app.include_router(todos.router)