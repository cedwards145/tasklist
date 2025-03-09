from datetime import datetime
from pydantic import BaseModel, Field


class NewTaskRequest(BaseModel):
    """Models the fields required to create a new Task."""

    title: str
    description: str
    priority: int = Field(ge=1, le=3)
    due_date: datetime
