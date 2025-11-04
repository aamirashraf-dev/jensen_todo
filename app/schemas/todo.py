from datetime import datetime
from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: int = Field(..., description="The ID of the todo")
    title: str = Field(..., description="The title of the todo", min_length=1, max_length=100)
    description: str = Field(..., description="The description of the todo")
    completed: bool = Field(..., description="Whether the todo is completed")