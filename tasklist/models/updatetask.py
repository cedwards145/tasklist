from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
