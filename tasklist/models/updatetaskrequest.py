from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UpdateTaskRequest(BaseModel):
    """Models the fields required to update a Task."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
