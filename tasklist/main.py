from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from tasklist.models.task import Task
from tasklist.models.newtaskrequest import NewTaskRequest
from tasklist.models.updatetaskrequest import UpdateTaskRequest


app = FastAPI()


sqlite_file_name = "data/tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/tasks")
def add_task(new_task: NewTaskRequest, session: SessionDep) -> Task:
    """Add a new task with the following fields:
    - **title**: A title for the task
    - **description**: A description of the details of the task
    - **priority**: The priority of the task, ranging from 1 to 3
    - **due_date**: The date this task is due in ISO 8601 format

    Returns the Task on success.
    """

    task = Task(
        title=new_task.title,
        description=new_task.description,
        priority=new_task.priority,
        due_date=new_task.due_date,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks")
def get_tasks(
    session: SessionDep,
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
) -> List[Task]:
    """Get all tasks. Results can optionally be filtered by supplying:
    - **completed**: boolean, return only completed or uncompleted tasks
    - **priority**: return only tasks with a matching priority
    """

    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    if priority is not None:
        query = query.where(Task.priority == priority)

    return session.exec(query).all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep) -> Task:
    """Get a single task by its ID.
    - **task_id**: The ID of the task

    Returns a 404 Not Found error if a task with the given ID does not
    exist.
    """

    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int, update_task: UpdateTaskRequest, session: SessionDep
) -> Task:
    """Update a single task by its ID. **task_id** is required but all
    other parameters are optional. If not provided, the value will remain
    unchanged.
    - **task_id**: The ID of the task to update
    - **title**: An updated title for the task
    - **description**: An updated description of the task
    - **priority**: An updated priority of the task, ranging from 1 to 3
    - **due_date**: An updated due date in ISO 8601 format
    - **completed**: An updated completed flag for the task

    Returns a 404 Not Found error if a task with the given ID does not
    exist.
    """

    task = session.get(Task, task_id)

    # If the task ID is not found, return a 404 error
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    # Update each field of the task from the update request.
    # If the field in the update_task object is None (default value)
    # then the existing value from the task is used, meaning no change.
    task.title = update_task.title or task.title
    task.description = update_task.description or task.title
    task.priority = update_task.priority or task.priority
    task.due_date = update_task.due_date or task.due_date
    task.completed = update_task.completed or task.completed

    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    """Delete a single task by its ID.
    - **task_id**: The ID of the task to delete

    Returns a message indicating success, or a 404 Not Found error
    if a task with the given ID does not exist.
    """

    task = session.get(Task, task_id)
    # If the task ID is not found, return a 404 error
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    session.delete(session.get(Task, task_id))
    session.commit()
    return {"message": "Task deleted successfully."}
