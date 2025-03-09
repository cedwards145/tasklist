from typing import Annotated, List, Union
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from tasklist.models.task import Task 
from tasklist.models.newtaskrequest import NewTaskRequest
from tasklist.models.updatetaskrequest import UpdateTaskRequest


app = FastAPI()


sqlite_file_name = "tasks.sqlite3"
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
    task = Task(
        title=new_task.title,
        description=new_task.description,
        priority=new_task.priority,
        due_date=new_task.due_date
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
 

@app.get("/tasks")
def get_tasks(session: SessionDep, completed: Union[bool, None] = None, priority: Union[int, None] = None) -> List[Task]:
    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    if priority is not None:
        query = query.where(Task.priority == priority)
    
    return session.exec(query).all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep) -> Task:
    task =  session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task
    

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_task: UpdateTaskRequest, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
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
    session.delete(session.get(Task, task_id))
    session.commit()
    return { "message": "Task deleted successfully." }
