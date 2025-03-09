from datetime import datetime
from pydantic import BaseModel


class NewTask(BaseModel):
    title: str
    description: str
    priority: int
    due_date: datetime
