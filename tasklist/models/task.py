from datetime import datetime
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: int = Field(ge=1, le=3)
    due_date: datetime
    completed: bool = Field(default=False)
