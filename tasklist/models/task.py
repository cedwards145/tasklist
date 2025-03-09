from datetime import datetime
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    due_date: datetime
    completed: bool = False
