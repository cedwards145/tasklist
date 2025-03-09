from datetime import datetime
from pydantic import BaseModel


class NewTaskRequest(BaseModel):
    """Models the fields required to create a new Task."""
    title: str
    description: str
    priority: int
    due_date: datetime
